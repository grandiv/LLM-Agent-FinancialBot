"""
Integration tests untuk Financial Bot
Testing end-to-end flow dengan mock LLM
"""

import os
import tempfile
import sys
import pytest
from unittest.mock import Mock, AsyncMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.llm_agent import LLMAgent
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore

class TestIntegration:
    """Integration tests untuk bot workflow"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown test fixtures"""
        # Setup
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

        yield

        # Teardown
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

    @pytest.mark.asyncio
    async def test_record_income_flow(self):
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
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "aku dapat gaji 5 juta"
        )

        # Assertions
        assert "Pemasukan dicatat" in response
        assert "5,000,000" in response

        # Verify database
        balance = self.database.get_user_balance(self.user_id)
        assert balance['income'] == 5000000
        assert balance['balance'] == 5000000

    @pytest.mark.asyncio
    async def test_record_expense_flow(self):
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
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "habis 50rb buat makan"
        )

        # Assertions
        assert "Pengeluaran dicatat" in response
        assert "50,000" in response

        # Verify database
        balance = self.database.get_user_balance(self.user_id)
        assert balance['expense'] == 50000
        assert balance['balance'] == -50000

    @pytest.mark.asyncio
    async def test_check_balance_flow(self):
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
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "berapa saldo aku?"
        )

        # Assertions
        assert "Ringkasan Keuangan" in response
        assert "5,000,000" in response  # Income
        assert "200,000" in response    # Expense
        assert "4,800,000" in response  # Balance

    @pytest.mark.asyncio
    async def test_budget_advice_flow(self):
        """Test 4: End-to-end flow untuk budget advice"""
        # Add balance
        self.database.add_transaction(self.user_id, self.username, "income", 5000000, "Gaji", "")

        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "budget_advice",
            "response_text": "Berikut saran anggaran..."
        }

        # Process message
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "kasih saran budget dong"
        )

        # Assertions
        assert "Saran Anggaran" in response
        assert "Dana Darurat" in response
        assert "Tabungan" in response

    @pytest.mark.asyncio
    async def test_purchase_analysis_affordable(self):
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
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "aku mau beli laptop 2 juta"
        )

        # Assertions
        assert "Analisis Pembelian" in response
        assert "laptop" in response
        assert "2,000,000" in response

    @pytest.mark.asyncio
    async def test_purchase_analysis_not_affordable(self):
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
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "aku mau beli laptop 5 juta"
        )

        # Assertions
        assert "Belum mampu" in response
        assert "Alternatif" in response

    @pytest.mark.asyncio
    async def test_casual_chat_flow(self):
        """Test 7: Casual chat flow"""
        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "casual_chat",
            "response_text": "Halo! Ada yang bisa saya bantu?"
        }

        # Process message
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "halo"
        )

        # Assertions
        assert response == "Halo! Ada yang bisa saya bantu?"

    @pytest.mark.asyncio
    async def test_help_flow(self):
        """Test 8: Help command flow"""
        # Mock LLM response
        self.mock_llm.process_message.return_value = {
            "intent": "help",
            "response_text": "Bantuan..."
        }

        # Process message
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "help"
        )

        # Assertions
        assert "FinancialBot" in response
        assert "Mencatat pemasukan" in response
        assert "Mencatat pengeluaran" in response

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test 9: Error handling ketika LLM gagal"""
        # Mock LLM error
        self.mock_llm.process_message.return_value = {
            "intent": "error",
            "response_text": "Maaf, ada kesalahan.",
            "error": "API timeout"
        }

        # Process message
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "test message"
        )

        # Should return error message
        assert "Maaf" in response

    @pytest.mark.asyncio
    async def test_negative_balance_warning(self):
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
        response = await self.bot_core.process_message(
            self.user_id,
            self.username,
            "habis 100rb"
        )

        # Should show negative balance warning
        assert "negatif" in response.lower()
