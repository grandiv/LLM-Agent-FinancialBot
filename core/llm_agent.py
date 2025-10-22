"""
LLM Agent menggunakan Ollama (OpenAI-compatible) untuk natural language understanding
"""

import os
import json
import logging
from typing import Dict, List, Optional

import httpx

from .prompts import SYSTEM_PROMPT, FUNCTION_TOOLS, get_user_context_prompt, ERROR_RESPONSES

logger = logging.getLogger(__name__)


class LLMAgent:
    """Agent yang menggunakan LLM untuk memahami intent pengguna"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize LLM Agent dengan Ollama lokal

        Args:
            api_key: Optional override API key (Ollama tidak membutuhkan real key)
            model: Model yang akan digunakan (default: llama3.1:8b)
            base_url: Optional override base URL untuk Ollama server
        """

        raw_base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        # Ensure base URL always points to /v1 for OpenAI-compatible routes
        normalized = raw_base_url.rstrip("/")
        if not normalized.endswith("/v1"):
            normalized = f"{normalized}/v1"
        self.base_url = normalized

        resolved_api_key = api_key or os.getenv("OLLAMA_API_KEY", "ollama")
        headers = {"Authorization": f"Bearer {resolved_api_key}"} if resolved_api_key else {}
        self.client = httpx.Client(base_url=self.base_url, headers=headers, timeout=60.0)

        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.conversation_history: Dict[str, List[Dict]] = {}  # user_id -> messages
        self.max_history = 5  # Simpan 5 message terakhir untuk konteks

    def _get_conversation_history(self, user_id: str) -> List[Dict]:
        """Ambil riwayat percakapan user"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]

    def _add_to_history(self, user_id: str, role: str, content: str):
        """Tambahkan message ke riwayat percakapan"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []

        self.conversation_history[user_id].append({
            "role": role,
            "content": content
        })

        # Keep only last N messages untuk menghemat token
        if len(self.conversation_history[user_id]) > self.max_history * 2:  # *2 karena user + assistant
            self.conversation_history[user_id] = self.conversation_history[user_id][-(self.max_history * 2):]

    def _build_messages(self, user_message: str, user_context: str, conversation_history: List[Dict]) -> List[Dict]:
        """Build messages array untuk API call"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + user_context}
        ]

        # Tambahkan conversation history (exclude system messages)
        for msg in conversation_history[-(self.max_history * 2):]:
            if msg["role"] != "system":
                messages.append(msg)

        # Tambahkan user message saat ini
        messages.append({"role": "user", "content": user_message})

        return messages

    def process_message(self, user_id: str, username: str, message: str,
                       balance_data: Optional[Dict] = None,
                       recent_transactions: Optional[List] = None) -> Dict:
        """
        Proses pesan dari user menggunakan LLM

        Args:
            user_id: ID pengguna
            username: Username pengguna
            message: Pesan dari pengguna
            balance_data: Data saldo user (income, expense, balance)
            recent_transactions: Transaksi terakhir user

        Returns:
            Dict dengan intent dan extracted data
        """
        try:
            # Build user context
            if balance_data is None:
                balance_data = {'income': 0, 'expense': 0, 'balance': 0}
            if recent_transactions is None:
                recent_transactions = []

            user_context = get_user_context_prompt(balance_data, recent_transactions)

            # Get conversation history
            history = self._get_conversation_history(user_id)

            # Build messages
            messages = self._build_messages(message, user_context, history)

            # Call local Ollama API
            logger.info(f"Calling Ollama model for user {user_id}")

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000,
            }

            use_function_calling = False
            response_data: Optional[Dict] = None

            # Try function-calling mode first
            try:
                fc_payload = {**payload, "tools": FUNCTION_TOOLS, "tool_choice": "auto"}
                resp = self.client.post("/chat/completions", json=fc_payload)
                resp.raise_for_status()
                response_data = resp.json()
                use_function_calling = True
                logger.info("Using function calling mode")
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in (400, 404):
                    logger.info("Function calling not supported, retrying without tools")
                else:
                    raise

            # Fallback to standard JSON mode if needed
            if response_data is None:
                resp = self.client.post("/chat/completions", json=payload)
                resp.raise_for_status()
                response_data = resp.json()
                use_function_calling = False

            # Parse response
            choices = response_data.get("choices", [])
            if not choices:
                raise ValueError("No choices returned from Ollama")

            response_message = choices[0].get("message", {})

            # Add to conversation history
            self._add_to_history(user_id, "user", message)

            # Parse based on response type
            tool_calls = response_message.get("tool_calls") or []

            if use_function_calling and tool_calls:
                # Function calling mode
                tool_call = tool_calls[0]
                function_args_raw = tool_call.get("function", {}).get("arguments", "{}")
                function_args = json.loads(function_args_raw)
                result = self._validate_function_response(function_args)
            else:
                # JSON mode - parse content as JSON
                try:
                    response_text = response_message.get("content") or "{}"

                    # DeepSeek R1 models may include <think> tags, extract JSON from content
                    # Remove think tags if present
                    if "<think>" in response_text and "</think>" in response_text:
                        # Extract content after </think>
                        response_text = response_text.split("</think>")[-1].strip()

                    # Find JSON object in the response (handle case where there's extra text)
                    start_idx = response_text.find("{")
                    end_idx = response_text.rfind("}") + 1

                    if start_idx != -1 and end_idx > start_idx:
                        json_str = response_text[start_idx:end_idx]
                        function_args = json.loads(json_str)
                        result = self._validate_function_response(function_args)
                    else:
                        # No JSON found, treat as casual chat
                        result = {
                            "intent": "casual_chat",
                            "response_text": response_text
                        }

                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parsing failed: {e}, content: {response_text[:200]}")
                    # Fallback if JSON parsing fails
                    result = {
                        "intent": "casual_chat",
                        "response_text": response_message.content or "Maaf, saya kurang mengerti."
                    }

            # Add assistant response to history
            if "response_text" in result:
                self._add_to_history(user_id, "assistant", result["response_text"])

            logger.info(f"Successfully processed message with intent: {result.get('intent')}")
            return result

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return {
                "intent": "error",
                "response_text": ERROR_RESPONSES["api_error"],
                "error": str(e)
            }

    def _validate_function_response(self, function_args: Dict) -> Dict:
        """Validasi dan bersihkan response dari function calling"""
        result = {
            "intent": function_args.get("intent", "casual_chat"),
            "response_text": function_args.get("response_text", "")
        }

        # Tambahkan field opsional jika ada
        if "amount" in function_args and function_args["amount"]:
            result["amount"] = float(function_args["amount"])

        if "category" in function_args and function_args["category"]:
            result["category"] = function_args["category"]

        if "description" in function_args and function_args["description"]:
            result["description"] = function_args["description"]

        if "item_name" in function_args and function_args["item_name"]:
            result["item_name"] = function_args["item_name"]

        if "transaction_id" in function_args and function_args["transaction_id"]:
            result["transaction_id"] = int(function_args["transaction_id"])

        return result

    def clear_history(self, user_id: str):
        """Hapus riwayat percakapan user"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
            logger.info(f"Cleared conversation history for user {user_id}")

    def get_history_length(self, user_id: str) -> int:
        """Dapatkan panjang riwayat percakapan user"""
        return len(self._get_conversation_history(user_id))
