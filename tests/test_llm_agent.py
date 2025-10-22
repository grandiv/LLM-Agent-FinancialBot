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
        """Test 5: Process message dengan function calling berhasil"""
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock response dengan function call
        mock_tool_call = Mock()
        mock_tool_call.function.arguments = '{"intent": "record_income", "amount": 5000000, "category": "Gaji", "response_text": "Pemasukan dicatat!"}'

        mock_message = Mock()
        mock_message.tool_calls = [mock_tool_call]
        mock_message.content = None

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
        """Test 6: Process message tanpa function calling (casual chat)"""
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        # Mock response tanpa function call
        mock_message = Mock()
        mock_message.tool_calls = None
        mock_message.content = "Halo! Ada yang bisa saya bantu?"

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

if __name__ == '__main__':
    unittest.main()
