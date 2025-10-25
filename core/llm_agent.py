"""
LLM Agent menggunakan OpenRouter API untuk natural language understanding
"""

import os
import json
import logging
from typing import Dict, List, Optional
from openai import OpenAI
from .prompts import SYSTEM_PROMPT, get_user_context_prompt, ERROR_RESPONSES

logger = logging.getLogger(__name__)

class LLMAgent:
    """Agent yang menggunakan LLM untuk memahami intent pengguna"""

    def __init__(self, api_key: str, model: str = "anthropic/claude-3-haiku"):
        """
        Initialize LLM Agent dengan OpenRouter

        Args:
            api_key: OpenRouter API key
            model: Model yang akan digunakan (default: claude-3-haiku)
        """
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = model
        self.conversation_history: Dict[str, List[Dict]] = {}  # user_id -> messages
        self.conversation_context: Dict[str, Dict] = {}  # user_id -> context entities
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

            # Build context hint and inject into message
            context_hint = self._build_context_hint(user_id)
            message_with_context = message + context_hint if context_hint else message

            # Build messages
            messages = self._build_messages(message_with_context, user_context, history)

            # Call OpenRouter API with JSON mode
            logger.info(f"Calling OpenRouter API (JSON mode) for user {user_id}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},  # Guaranteed JSON response
                temperature=0.3,  # Lower temperature for consistent intent extraction
                max_tokens=800  # Reduced from 1500 (JSON is concise)
            )

            # Parse response
            response_message = response.choices[0].message

            # Add to conversation history
            self._add_to_history(user_id, "user", message)

            # Parse JSON response
            try:
                response_text = response_message.content or "{}"

                # DeepSeek R1 models may include <think> tags, extract JSON from content
                if "<think>" in response_text and "</think>" in response_text:
                    response_text = response_text.split("</think>")[-1].strip()

                # Parse JSON (guaranteed to be valid with json_object mode)
                function_args = json.loads(response_text)
                result = self._validate_function_response(function_args)

            except json.JSONDecodeError as e:
                logger.warning(f"JSON parsing failed: {e}, content: {response_text[:200]}")
                # Fallback if JSON parsing fails (rare with json_object mode)
                result = {
                    "intent": "casual_chat",
                    "response_text": "Maaf, saya kurang mengerti. Bisa dijelaskan lagi?"
                }

            # Extract and store entities to context
            self._extract_and_store_entities(user_id, result)

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

    # ============================================================================
    # CONTEXT TRACKING METHODS (NEW)
    # ============================================================================

    def _get_context(self, user_id: str, key: str, default=None):
        """
        Ambil entity dari conversation context

        Args:
            user_id: ID pengguna
            key: Context key (e.g., 'last_searched_item', 'last_mentioned_amount')
            default: Default value jika tidak ditemukan

        Returns:
            Context value atau default
        """
        if user_id not in self.conversation_context:
            return default
        return self.conversation_context[user_id].get(key, default)

    def _update_context(self, user_id: str, key: str, value):
        """
        Simpan entity ke conversation context

        Args:
            user_id: ID pengguna
            key: Context key
            value: Context value
        """
        if user_id not in self.conversation_context:
            self.conversation_context[user_id] = {}

        self.conversation_context[user_id][key] = value
        logger.debug(f"Updated context for user {user_id}: {key} = {value}")

    def _clear_context(self, user_id: str):
        """Hapus semua context entities untuk user"""
        if user_id in self.conversation_context:
            self.conversation_context[user_id] = {}
            logger.info(f"Cleared conversation context for user {user_id}")

    def _build_context_hint(self, user_id: str) -> str:
        """
        Build context hint string untuk disisipkan ke user message

        Returns:
            String berisi context hints (kosong jika tidak ada context)
        """
        context = self.conversation_context.get(user_id, {})
        if not context:
            return ""

        hints = []

        # Last searched item
        if "last_searched_item" in context:
            item_data = context["last_searched_item"]
            item_name = item_data.get("name", "")
            price = item_data.get("price", 0)
            if item_name:
                hint = f"Barang terakhir dicari: {item_name}"
                if price > 0:
                    hint += f" (harga: Rp {price:,.0f})"
                hints.append(hint)

        # Last mentioned amount
        if "last_mentioned_amount" in context:
            amount = context["last_mentioned_amount"]
            hints.append(f"Jumlah terakhir disebutkan: Rp {amount:,.0f}")

        # Last transaction ID
        if "last_transaction_id" in context:
            trans_id = context["last_transaction_id"]
            hints.append(f"Transaksi terakhir: ID #{trans_id}")

        # Pending action
        if "pending_action" in context:
            action = context["pending_action"]
            hints.append(f"Aksi tertunda: {action}")

        if hints:
            return "\n[KONTEKS PERCAKAPAN: " + " | ".join(hints) + "]"
        return ""

    def _extract_and_store_entities(self, user_id: str, result: Dict):
        """
        Extract entities dari LLM result dan simpan ke context

        Args:
            user_id: ID pengguna
            result: Result dari LLM processing
        """
        intent = result.get("intent")

        # Store last mentioned amount
        if "amount" in result and result["amount"]:
            self._update_context(user_id, "last_mentioned_amount", result["amount"])

        # Store last searched/mentioned item
        if "item_name" in result and result["item_name"]:
            item_data = {"name": result["item_name"]}
            if "amount" in result:
                item_data["price"] = result["amount"]
            self._update_context(user_id, "last_searched_item", item_data)

        # Store transaction ID
        if "transaction_id" in result and result["transaction_id"]:
            self._update_context(user_id, "last_transaction_id", result["transaction_id"])

        # Store pending action based on intent
        if intent == "search_price":
            self._update_context(user_id, "pending_action", "considering_purchase")
        elif intent == "purchase_analysis":
            self._update_context(user_id, "pending_action", "analyzing_purchase")
        elif intent in ["record_income", "record_expense"]:
            # Clear pending action after recording
            if "pending_action" in self.conversation_context.get(user_id, {}):
                del self.conversation_context[user_id]["pending_action"]
