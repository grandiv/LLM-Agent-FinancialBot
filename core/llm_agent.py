"""
LLM Agent menggunakan Ollama native API untuk natural language understanding
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
        Initialize LLM Agent dengan Ollama lokal menggunakan native API

        Args:
            api_key: Optional override API key (Ollama tidak membutuhkan key)
            model: Model yang akan digunakan (default: llama3.1:8b)
            base_url: Optional override base URL untuk Ollama server
        """

        # Use Ollama's native API endpoint (no /v1 prefix)
        raw_base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.base_url = raw_base_url.rstrip("/")

        # Ollama native API doesn't require authorization headers
        self.client = httpx.Client(base_url=self.base_url, timeout=120.0)

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
                       recent_transactions: Optional[List] = None,
                       last_price_search: Optional[Dict] = None) -> Dict:
        """
        Proses pesan dari user menggunakan Ollama native API dengan prompt engineering

        Args:
            user_id: ID pengguna
            username: Username pengguna
            message: Pesan dari pengguna
            balance_data: Data saldo user (income, expense, balance)
            recent_transactions: Transaksi terakhir user
            last_price_search: Hasil pencarian harga terakhir (untuk purchase intent)

        Returns:
            Dict dengan intent dan extracted data
        """
        try:
            # Build user context
            if balance_data is None:
                balance_data = {'income': 0, 'expense': 0, 'balance': 0}
            if recent_transactions is None:
                recent_transactions = []

            user_context = get_user_context_prompt(balance_data, recent_transactions, last_price_search)

            # Get conversation history
            history = self._get_conversation_history(user_id)

            # Build messages
            messages = self._build_messages(message, user_context, history)

            # Call Ollama native API at /api/chat
            logger.info(f"Calling Ollama native API ({self.model}) for user {user_id}")

            # Ollama native API payload format
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,  # We want complete response, not streaming
                "format": "json",  # FORCE JSON output mode
                "options": {
                    "temperature": 0.3,  # Lower temperature for better instruction following
                    "num_predict": 1000,  # Max tokens to generate
                }
            }

            # Make API call to Ollama's native /api/chat endpoint
            resp = self.client.post("/api/chat", json=payload)
            resp.raise_for_status()
            response_data = resp.json()

            # Ollama native response format: {"message": {"role": "assistant", "content": "..."}}
            if "message" not in response_data:
                raise ValueError("Invalid response format from Ollama")

            response_message = response_data["message"]
            response_text = response_message.get("content", "")

            # Add to conversation history
            self._add_to_history(user_id, "user", message)

            # Parse response using JSON extraction from prompt-engineered response
            try:
                # Handle thinking tags (for reasoning models)
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
                    logger.warning(f"No JSON found in response, treating as casual chat")
                    result = {
                        "intent": "casual_chat",
                        "response_text": response_text
                    }

            except json.JSONDecodeError as e:
                logger.warning(f"JSON parsing failed: {e}, content: {response_text[:200]}")
                # Fallback if JSON parsing fails
                result = {
                    "intent": "casual_chat",
                    "response_text": response_text or "Maaf, saya kurang mengerti."
                }

            # Add assistant response to history
            if "response_text" in result:
                self._add_to_history(user_id, "assistant", result["response_text"])

            logger.info(f"Successfully processed message with intent: {result.get('intent')}")
            return result

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Ollama: {e.response.status_code} - {e.response.text}", exc_info=True)
            return {
                "intent": "error",
                "response_text": ERROR_RESPONSES["api_error"],
                "error": f"HTTP {e.response.status_code}: {e.response.text}"
            }
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

        if "search_query" in function_args and function_args["search_query"]:
            result["search_query"] = function_args["search_query"]

        if "source_index" in function_args and function_args["source_index"] is not None:
            result["source_index"] = int(function_args["source_index"])

        if "transaction_id" in function_args and function_args["transaction_id"]:
            result["transaction_id"] = int(function_args["transaction_id"])

        # MCP-specific fields
        if "format" in function_args and function_args["format"]:
            result["format"] = function_args["format"]

        if "reminder_text" in function_args and function_args["reminder_text"]:
            result["reminder_text"] = function_args["reminder_text"]

        if "due_date" in function_args and function_args["due_date"]:
            result["due_date"] = function_args["due_date"]

        if "reminder_id" in function_args and function_args["reminder_id"]:
            result["reminder_id"] = int(function_args["reminder_id"])

        return result

    def clear_history(self, user_id: str):
        """Hapus riwayat percakapan user"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
            logger.info(f"Cleared conversation history for user {user_id}")

    def get_history_length(self, user_id: str) -> int:
        """Dapatkan panjang riwayat percakapan user"""
        return len(self._get_conversation_history(user_id))
