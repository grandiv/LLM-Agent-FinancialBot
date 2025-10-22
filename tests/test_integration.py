"""
Integration tests untuk Financial Bot
Testing end-to-end flow dengan mock LLM
"""

import os
import unittest
import tempfile
import sys
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.llm_agent import LLMAgent
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore

class TestIntegration(unittest.TestCase):
    """Integration tests untuk bot workflow"""

    def setUp(self):
        """Setup test fixtures"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.database = DatabaseManager(self.temp_db.name)

        # Create mock LLM agent
        self.mock_llm = Mock(spec=LLMAgent)

        # Create bot core
        self.bot_core = FinancialBotCore(self.mock_llm, self.database)

        self.user_id = "test_user_123"
        self.username = "Test User"

    def tearDown(self):
        """Cleanup"""
        # Close database connection first (Windows fix)
        self.database = None
        self.bot_core = None
        import gc
        gc.collect()

        # Small delay for Windows to release file handle
        import time
        time.sleep(0.1)

        if os.path.exists(self.temp_db.name):
            try:
                os.unlink(self.temp_db.name)
            except PermissionError:
                pass  # Ignore if file still locked on Windows

    def test_record_income_flow(self):
        """Test 1: End-to-end flow untuk record income"""
        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "record_income",
            "amount": 5000000,
            "category": "Gaji",
            "description": "gaji bulanan",
            "response_text": "Pemasukan dicatat!"
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "aku dapat gaji 5 juta"
        )

        # Assertions
        self.assertIn("Pemasukan dicatat", response)
        self.assertIn("5,000,000", response)

        # Verify database
        balance = self.database.get_user_balance(self.user_id)
        self.assertEqual(balance['income'], 5000000)
        self.assertEqual(balance['balance'], 5000000)

    def test_record_expense_flow(self):
        """Test 2: End-to-end flow untuk record expense"""
        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "record_expense",
            "amount": 50000,
            "category": "Makanan",
            "description": "makan siang",
            "response_text": "Pengeluaran dicatat!"
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "habis 50rb buat makan"
        )

        # Assertions
        self.assertIn("Pengeluaran dicatat", response)
        self.assertIn("50,000", response)

        # Verify database
        balance = self.database.get_user_balance(self.user_id)
        self.assertEqual(balance['expense'], 50000)
        self.assertEqual(balance['balance'], -50000)

    def test_check_balance_flow(self):
        """Test 3: End-to-end flow untuk check balance"""
        # Add some transactions first
        self.database.add_transaction(self.user_id, self.username, "income", 5000000, "Gaji", "")
        self.database.add_transaction(self.user_id, self.username, "expense", 200000, "Makanan", "")

        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "check_balance",
            "response_text": "Cek saldo..."
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "berapa saldo aku?"
        )

        # Assertions
        self.assertIn("Ringkasan Keuangan", response)
        self.assertIn("5,000,000", response)  # Income
        self.assertIn("200,000", response)    # Expense
        self.assertIn("4,800,000", response)  # Balance

    def test_budget_advice_flow(self):
        """Test 4: End-to-end flow untuk budget advice"""
        # Add balance
        self.database.add_transaction(self.user_id, self.username, "income", 5000000, "Gaji", "")

        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "budget_advice",
            "response_text": "Berikut saran anggaran..."
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "kasih saran budget dong"
        )

        # Assertions
        self.assertIn("Saran Anggaran", response)
        self.assertIn("Dana Darurat", response)
        self.assertIn("Tabungan", response)

    def test_purchase_analysis_affordable(self):
        """Test 5: Purchase analysis untuk barang yang affordable"""
        # Add balance
        self.database.add_transaction(self.user_id, self.username, "income", 10000000, "Gaji", "")

        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "purchase_analysis",
            "amount": 2000000,
            "item_name": "laptop",
            "response_text": "Analisis pembelian laptop..."
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "aku mau beli laptop 2 juta"
        )

        # Assertions
        self.assertIn("Analisis Pembelian", response)
        self.assertIn("laptop", response)
        self.assertIn("2,000,000", response)

    def test_purchase_analysis_not_affordable(self):
        """Test 6: Purchase analysis untuk barang yang tidak affordable"""
        # Add small balance
        self.database.add_transaction(self.user_id, self.username, "income", 1000000, "Gaji", "")

        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "purchase_analysis",
            "amount": 5000000,
            "item_name": "laptop",
            "response_text": "Analisis pembelian laptop..."
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "aku mau beli laptop 5 juta"
        )

        # Assertions
        self.assertIn("Belum mampu", response)
        self.assertIn("Alternatif", response)

    def test_casual_chat_flow(self):
        """Test 7: Casual chat flow"""
        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "casual_chat",
            "response_text": "Halo! Ada yang bisa saya bantu?"
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "halo"
        )

        # Assertions
        self.assertEqual(response, "Halo! Ada yang bisa saya bantu?")

    def test_help_flow(self):
        """Test 8: Help command flow"""
        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "help",
            "response_text": "Bantuan..."
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "help"
        )

        # Assertions
        self.assertIn("FinancialBot", response)
        self.assertIn("Mencatat pemasukan", response)
        self.assertIn("Mencatat pengeluaran", response)

    def test_error_handling(self):
        """Test 9: Error handling ketika LLM gagal"""
        # Mock LLM error
        self.mock_llm.process_message.return_value = {
            "intent": "error",
            "response_text": "Maaf, ada kesalahan.",
            "error": "API timeout"
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "test message"
        )

        # Should return error message
        self.assertIn("Maaf", response)

    def test_negative_balance_warning(self):
        """Test 10: Warning muncul ketika balance negatif"""
        # Add expense without income
        self.mock_llm.process_message.return_value = {
            "intent": "record_expense",
            "amount": 100000,
            "category": "Makanan",
            "description": "makan",
            "response_text": "Pengeluaran dicatat!"
        }

        # Process message
        response = self.bot_core.process_message(
            self.user_id,
            self.username,
            "habis 100rb"
        )

        # Should show negative balance warning
        self.assertIn("negatif", response.lower())

if __name__ == '__main__':
    unittest.main()
