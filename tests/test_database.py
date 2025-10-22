"""
Unit tests untuk Database Manager
"""

import os
import unittest
import tempfile
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """Test cases untuk Database Manager"""

    def setUp(self):
        """Setup test database"""
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = DatabaseManager(self.temp_db.name)

    def tearDown(self):
        """Cleanup test database"""
        # Close database connection first (Windows fix)
        self.db = None
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

    def test_database_initialization(self):
        """Test 1: Database dapat diinisialisasi dengan benar"""
        self.assertIsNotNone(self.db)
        self.assertTrue(os.path.exists(self.temp_db.name))

        # Check if tables exist
        categories = self.db.get_available_categories()
        self.assertGreater(len(categories), 0)

    def test_add_income_transaction(self):
        """Test 2: Dapat menambahkan transaksi pemasukan"""
        success = self.db.add_transaction(
            user_id="test_user_1",
            username="Test User",
            transaction_type="income",
            amount=5000000,
            category="Gaji",
            description="gaji bulanan"
        )

        self.assertTrue(success)

        # Verify balance
        balance = self.db.get_user_balance("test_user_1")
        self.assertEqual(balance['income'], 5000000)
        self.assertEqual(balance['expense'], 0)
        self.assertEqual(balance['balance'], 5000000)

    def test_add_expense_transaction(self):
        """Test 3: Dapat menambahkan transaksi pengeluaran"""
        success = self.db.add_transaction(
            user_id="test_user_1",
            username="Test User",
            transaction_type="expense",
            amount=50000,
            category="Makanan",
            description="makan siang"
        )

        self.assertTrue(success)

        # Verify balance
        balance = self.db.get_user_balance("test_user_1")
        self.assertEqual(balance['income'], 0)
        self.assertEqual(balance['expense'], 50000)
        self.assertEqual(balance['balance'], -50000)

    def test_get_user_balance_multiple_transactions(self):
        """Test 4: Balance calculation dengan multiple transaksi"""
        user_id = "test_user_1"

        # Add multiple transactions
        self.db.add_transaction(user_id, "Test", "income", 5000000, "Gaji", "gaji")
        self.db.add_transaction(user_id, "Test", "income", 1000000, "Freelance", "project")
        self.db.add_transaction(user_id, "Test", "expense", 200000, "Makanan", "groceries")
        self.db.add_transaction(user_id, "Test", "expense", 100000, "Transport", "bensin")

        balance = self.db.get_user_balance(user_id)

        self.assertEqual(balance['income'], 6000000)
        self.assertEqual(balance['expense'], 300000)
        self.assertEqual(balance['balance'], 5700000)

    def test_get_user_transactions(self):
        """Test 5: Dapat mengambil transaksi user dengan benar"""
        user_id = "test_user_1"

        # Add transactions
        self.db.add_transaction(user_id, "Test", "income", 5000000, "Gaji", "gaji")
        self.db.add_transaction(user_id, "Test", "expense", 50000, "Makanan", "makan")

        transactions = self.db.get_user_transactions(user_id, limit=10)

        self.assertEqual(len(transactions), 2)
        # Check both transaction types exist
        transaction_types = [t['type'] for t in transactions]
        self.assertIn('income', transaction_types)
        self.assertIn('expense', transaction_types)

    def test_user_isolation(self):
        """Test 6: Data user terisolasi dengan benar"""
        user1 = "user_1"
        user2 = "user_2"

        # Add transactions for user1
        self.db.add_transaction(user1, "User 1", "income", 1000000, "Gaji", "")

        # Add transactions for user2
        self.db.add_transaction(user2, "User 2", "income", 2000000, "Gaji", "")

        # Check isolation
        balance1 = self.db.get_user_balance(user1)
        balance2 = self.db.get_user_balance(user2)

        self.assertEqual(balance1['income'], 1000000)
        self.assertEqual(balance2['income'], 2000000)

        # Check transactions
        trans1 = self.db.get_user_transactions(user1)
        trans2 = self.db.get_user_transactions(user2)

        self.assertEqual(len(trans1), 1)
        self.assertEqual(len(trans2), 1)

    def test_delete_transaction(self):
        """Test 7: Dapat menghapus transaksi"""
        user_id = "test_user_1"

        # Add transaction
        self.db.add_transaction(user_id, "Test", "income", 1000000, "Gaji", "")

        # Get transaction ID
        transactions = self.db.get_user_transactions(user_id)
        self.assertEqual(len(transactions), 1)

        transaction_id = transactions[0]['id']

        # Delete transaction
        success = self.db.delete_transaction(user_id, transaction_id)
        self.assertTrue(success)

        # Verify deletion
        transactions_after = self.db.get_user_transactions(user_id)
        self.assertEqual(len(transactions_after), 0)

    def test_delete_wrong_user_transaction(self):
        """Test 8: Tidak bisa menghapus transaksi user lain"""
        user1 = "user_1"
        user2 = "user_2"

        # User1 adds transaction
        self.db.add_transaction(user1, "User 1", "income", 1000000, "Gaji", "")

        transactions = self.db.get_user_transactions(user1)
        transaction_id = transactions[0]['id']

        # User2 tries to delete
        success = self.db.delete_transaction(user2, transaction_id)
        self.assertFalse(success)

        # Transaction should still exist
        transactions_after = self.db.get_user_transactions(user1)
        self.assertEqual(len(transactions_after), 1)

    def test_get_category_report(self):
        """Test 9: Laporan kategori generated dengan benar"""
        user_id = "test_user_1"

        # Add various transactions
        self.db.add_transaction(user_id, "Test", "income", 5000000, "Gaji", "")
        self.db.add_transaction(user_id, "Test", "expense", 200000, "Makanan", "")
        self.db.add_transaction(user_id, "Test", "expense", 150000, "Makanan", "")
        self.db.add_transaction(user_id, "Test", "expense", 100000, "Transport", "")

        report = self.db.get_category_report(user_id)

        self.assertIn("Gaji", report)
        self.assertEqual(report["Gaji"]["income"], 5000000)

        self.assertIn("Makanan", report)
        self.assertEqual(report["Makanan"]["expense"], 350000)  # 200k + 150k

        self.assertIn("Transport", report)
        self.assertEqual(report["Transport"]["expense"], 100000)

if __name__ == '__main__':
    unittest.main()
