"""
Unit tests untuk LLM Agent
"""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.llm_agent import LLMAgent

class TestLLMAgent(unittest.TestCase):
    """Test cases untuk LLM Agent functionality"""

    def setUp(self):
        """Setup test fixtures"""
        self.api_key = "test_api_key"
        self.model = "test_model"

    @patch('core.llm_agent.OpenAI')
    def test_agent_initialization(self, mock_openai):
        """Test 1: Agent dapat diinisialisasi dengan benar"""
        agent = LLMAgent(self.api_key, self.model)

        self.assertIsNotNone(agent)
        self.assertEqual(agent.model, self.model)
        self.assertEqual(agent.max_history, 5)
        mock_openai.assert_called_once()

    @patch('core.llm_agent.OpenAI')
    def test_conversation_history_management(self, mock_openai):
        """Test 2: Conversation history dapat dikelola dengan benar"""
        agent = LLMAgent(self.api_key, self.model)

        user_id = "test_user_123"

        # Initially empty
        history = agent._get_conversation_history(user_id)
        self.assertEqual(len(history), 0)

        # Add messages
        agent._add_to_history(user_id, "user", "Test message 1")
        agent._add_to_history(user_id, "assistant", "Response 1")

        history = agent._get_conversation_history(user_id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["role"], "assistant")

    @patch('core.llm_agent.OpenAI')
    def test_history_limit_enforcement(self, mock_openai):
        """Test 3: History tidak melebihi max_history limit"""
        agent = LLMAgent(self.api_key, self.model)
        agent.max_history = 2  # Set small limit for testing

        user_id = "test_user_123"

        # Add many messages
        for i in range(10):
            agent._add_to_history(user_id, "user", f"Message {i}")
            agent._add_to_history(user_id, "assistant", f"Response {i}")

        history = agent._get_conversation_history(user_id)

        # Should only keep last max_history * 2 messages
        self.assertLessEqual(len(history), agent.max_history * 2)

    @patch('core.llm_agent.OpenAI')
    def test_clear_history(self, mock_openai):
        """Test 4: Clear history menghapus semua riwayat user"""
        agent = LLMAgent(self.api_key, self.model)

        user_id = "test_user_123"

        # Add some history
        agent._add_to_history(user_id, "user", "Test")
        agent._add_to_history(user_id, "assistant", "Response")

        # Clear history
        agent.clear_history(user_id)

        history = agent._get_conversation_history(user_id)
        self.assertEqual(len(history), 0)

    @patch('core.llm_agent.OpenAI')
    def test_process_message_with_function_call(self, mock_openai):
        """Test 5: Process message dengan JSON mode berhasil"""
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock response dengan JSON content (JSON mode)
        mock_message = Mock()
        mock_message.content = '{"intent": "record_income", "amount": 5000000, "category": "Gaji", "response_text": "Pemasukan dicatat!"}'

        mock_choice = Mock()
        mock_choice.message = mock_message

        mock_response = Mock()
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_response

        agent = LLMAgent(self.api_key, self.model)

        # Process message
        result = agent.process_message(
            user_id="test_user",
            username="Test User",
            message="aku dapat gaji 5 juta",
            balance_data={'income': 0, 'expense': 0, 'balance': 0},
            recent_transactions=[]
        )

        # Assertions
        self.assertEqual(result['intent'], 'record_income')
        self.assertEqual(result['amount'], 5000000)
        self.assertEqual(result['category'], 'Gaji')
        self.assertIn('response_text', result)

    @patch('core.llm_agent.OpenAI')
    def test_process_message_without_function_call(self, mock_openai):
        """Test 6: Process message dengan JSON mode (casual chat)"""
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock response dengan JSON content (casual chat)
        mock_message = Mock()
        mock_message.content = '{"intent": "casual_chat", "response_text": "Halo! Ada yang bisa saya bantu?"}'

        mock_choice = Mock()
        mock_choice.message = mock_message

        mock_response = Mock()
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_response

        agent = LLMAgent(self.api_key, self.model)

        # Process message
        result = agent.process_message(
            user_id="test_user",
            username="Test User",
            message="halo",
            balance_data={'income': 0, 'expense': 0, 'balance': 0},
            recent_transactions=[]
        )

        # Assertions
        self.assertEqual(result['intent'], 'casual_chat')
        self.assertIn('response_text', result)
        self.assertEqual(result['response_text'], "Halo! Ada yang bisa saya bantu?")

    @patch('core.llm_agent.OpenAI')
    def test_process_message_api_error(self, mock_openai):
        """Test 7: Handle API error dengan graceful"""
        # Mock OpenAI client dengan error
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_client.chat.completions.create.side_effect = Exception("API Error")

        agent = LLMAgent(self.api_key, self.model)

        # Process message
        result = agent.process_message(
            user_id="test_user",
            username="Test User",
            message="test message",
            balance_data={'income': 0, 'expense': 0, 'balance': 0},
            recent_transactions=[]
        )

        # Should return error intent
        self.assertEqual(result['intent'], 'error')
        self.assertIn('response_text', result)
        self.assertIn('error', result)

    @patch('core.llm_agent.OpenAI')
    def test_validate_function_response(self, mock_openai):
        """Test 8: Validasi function response membersihkan data dengan benar"""
        agent = LLMAgent(self.api_key, self.model)

        # Test dengan data lengkap
        function_args = {
            "intent": "record_expense",
            "amount": "50000",
            "category": "Makanan",
            "description": "makan siang",
            "response_text": "Pengeluaran dicatat!"
        }

        result = agent._validate_function_response(function_args)

        self.assertEqual(result['intent'], 'record_expense')
        self.assertEqual(result['amount'], 50000.0)  # Converted to float
        self.assertEqual(result['category'], 'Makanan')
        self.assertEqual(result['description'], 'makan siang')
        self.assertIn('response_text', result)

    @patch('core.llm_agent.OpenAI')
    def test_multiple_users_isolation(self, mock_openai):
        """Test 9: History dari multiple users terisolasi dengan benar"""
        agent = LLMAgent(self.api_key, self.model)

        user1 = "user_1"
        user2 = "user_2"

        # Add history untuk user1
        agent._add_to_history(user1, "user", "Message from user 1")

        # Add history untuk user2
        agent._add_to_history(user2, "user", "Message from user 2")

        # Check isolation
        history1 = agent._get_conversation_history(user1)
        history2 = agent._get_conversation_history(user2)

        self.assertEqual(len(history1), 1)
        self.assertEqual(len(history2), 1)
        self.assertNotEqual(history1[0]['content'], history2[0]['content'])

    # ============================================================================
    # CONTEXT TRACKING TESTS (NEW)
    # ============================================================================

    @patch('core.llm_agent.OpenAI')
    def test_context_tracking_basic(self, mock_openai):
        """Test 10: Context tracking dapat menyimpan dan mengambil entities"""
        agent = LLMAgent(self.api_key, self.model)
        user_id = "test_user_123"

        # Store context
        agent._update_context(user_id, "last_searched_item", {
            "name": "iPhone 15",
            "price": 15000000
        })

        # Retrieve context
        item_data = agent._get_context(user_id, "last_searched_item")

        self.assertIsNotNone(item_data)
        self.assertEqual(item_data["name"], "iPhone 15")
        self.assertEqual(item_data["price"], 15000000)

    @patch('core.llm_agent.OpenAI')
    def test_context_tracking_default_value(self, mock_openai):
        """Test 11: Context tracking mengembalikan default value jika tidak ada"""
        agent = LLMAgent(self.api_key, self.model)
        user_id = "test_user_123"

        # Get non-existent context
        result = agent._get_context(user_id, "nonexistent_key", default="default_value")

        self.assertEqual(result, "default_value")

    @patch('core.llm_agent.OpenAI')
    def test_context_hint_generation(self, mock_openai):
        """Test 12: Context hint string dibuat dengan benar"""
        agent = LLMAgent(self.api_key, self.model)
        user_id = "test_user_123"

        # Store multiple contexts
        agent._update_context(user_id, "last_searched_item", {
            "name": "laptop gaming",
            "price": 12000000
        })
        agent._update_context(user_id, "pending_action", "considering_purchase")

        # Build context hint
        hint = agent._build_context_hint(user_id)

        self.assertIsNotNone(hint)
        self.assertIn("laptop gaming", hint)
        self.assertIn("12,000,000", hint)
        self.assertIn("considering_purchase", hint)
        self.assertIn("[KONTEKS PERCAKAPAN:", hint)

    @patch('core.llm_agent.OpenAI')
    def test_context_clear(self, mock_openai):
        """Test 13: Clear context menghapus semua entities"""
        agent = LLMAgent(self.api_key, self.model)
        user_id = "test_user_123"

        # Store context
        agent._update_context(user_id, "last_searched_item", {"name": "iPhone", "price": 15000000})
        agent._update_context(user_id, "pending_action", "analyzing_purchase")

        # Clear context
        agent._clear_context(user_id)

        # Check cleared
        item = agent._get_context(user_id, "last_searched_item")
        action = agent._get_context(user_id, "pending_action")

        self.assertIsNone(item)
        self.assertIsNone(action)

    @patch('core.llm_agent.OpenAI')
    def test_extract_and_store_entities_search_price(self, mock_openai):
        """Test 14: Extract entities dari search_price intent"""
        agent = LLMAgent(self.api_key, self.model)
        user_id = "test_user_123"

        result = {
            "intent": "search_price",
            "item_name": "PS5",
            "amount": 8000000,
            "response_text": "Mencari harga PS5..."
        }

        agent._extract_and_store_entities(user_id, result)

        # Check stored entities
        last_item = agent._get_context(user_id, "last_searched_item")
        last_amount = agent._get_context(user_id, "last_mentioned_amount")
        pending_action = agent._get_context(user_id, "pending_action")

        self.assertEqual(last_item["name"], "PS5")
        self.assertEqual(last_item["price"], 8000000)
        self.assertEqual(last_amount, 8000000)
        self.assertEqual(pending_action, "considering_purchase")

    @patch('core.llm_agent.OpenAI')
    def test_extract_and_store_entities_record_expense(self, mock_openai):
        """Test 15: Extract entities dari record_expense clears pending_action"""
        agent = LLMAgent(self.api_key, self.model)
        user_id = "test_user_123"

        # Set pending action
        agent._update_context(user_id, "pending_action", "considering_purchase")

        result = {
            "intent": "record_expense",
            "amount": 50000,
            "category": "Makanan",
            "response_text": "Pengeluaran dicatat!"
        }

        agent._extract_and_store_entities(user_id, result)

        # Pending action should be cleared
        pending_action = agent._get_context(user_id, "pending_action")
        self.assertIsNone(pending_action)

    @patch('core.llm_agent.OpenAI')
    def test_multi_turn_context_injection(self, mock_openai):
        """Test 16: Context hint diinjeksi ke message pada multi-turn conversation"""
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock JSON response
        mock_message = Mock()
        mock_message.content = '{"intent": "record_expense", "amount": 15000000, "item_name": "iPhone 15", "response_text": "Oke!"}'

        mock_choice = Mock()
        mock_choice.message = mock_message

        mock_response = Mock()
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_response

        agent = LLMAgent(self.api_key, self.model)
        user_id = "test_user_123"

        # Turn 1: Store context manually (simulating search_price result)
        agent._update_context(user_id, "last_searched_item", {
            "name": "iPhone 15",
            "price": 15000000
        })

        # Turn 2: Process message with implicit reference
        result = agent.process_message(
            user_id=user_id,
            username="Test User",
            message="beli aja",
            balance_data={'income': 20000000, 'expense': 0, 'balance': 20000000},
            recent_transactions=[]
        )

        # Check that API was called
        self.assertTrue(mock_client.chat.completions.create.called)

        # Get the messages sent to API
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]['messages']

        # Find user message (should have context hint injected)
        user_message = None
        for msg in messages:
            if msg['role'] == 'user' and 'beli aja' in msg['content']:
                user_message = msg['content']
                break

        # Context hint should be in the message
        self.assertIsNotNone(user_message)
        self.assertIn("[KONTEKS PERCAKAPAN:", user_message)
        self.assertIn("iPhone 15", user_message)

    @patch('core.llm_agent.OpenAI')
    def test_context_isolation_between_users(self, mock_openai):
        """Test 17: Context terisolasi antar users"""
        agent = LLMAgent(self.api_key, self.model)

        user1 = "user_1"
        user2 = "user_2"

        # Store different contexts for each user
        agent._update_context(user1, "last_searched_item", {
            "name": "iPhone 15",
            "price": 15000000
        })

        agent._update_context(user2, "last_searched_item", {
            "name": "Samsung Galaxy",
            "price": 12000000
        })

        # Check isolation
        user1_item = agent._get_context(user1, "last_searched_item")
        user2_item = agent._get_context(user2, "last_searched_item")

        self.assertEqual(user1_item["name"], "iPhone 15")
        self.assertEqual(user2_item["name"], "Samsung Galaxy")
        self.assertNotEqual(user1_item["price"], user2_item["price"])

if __name__ == '__main__':
    unittest.main()
