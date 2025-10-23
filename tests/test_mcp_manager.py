"""
Tests untuk MCP Manager
"""

import pytest
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from core.mcp_manager import MCPManager


@pytest.fixture
def mcp_manager(tmp_path):
    """Fixture untuk MCPManager dengan temporary directory"""
    export_dir = tmp_path / "exports"
    reminders_file = tmp_path / "reminders.json"
    return MCPManager(str(export_dir), str(reminders_file))


@pytest.fixture
def sample_transactions():
    """Sample transaction data"""
    return [
        {
            'id': 1,
            'type': 'income',
            'amount': 5000000,
            'category': 'Gaji',
            'description': 'Gaji bulanan',
            'date': '2025-01-15'
        },
        {
            'id': 2,
            'type': 'expense',
            'amount': 500000,
            'category': 'Makanan',
            'description': 'Belanja bulanan',
            'date': '2025-01-16'
        },
        {
            'id': 3,
            'type': 'expense',
            'amount': 200000,
            'category': 'Transport',
            'description': 'Bensin',
            'date': '2025-01-17'
        }
    ]


@pytest.fixture
def sample_balance():
    """Sample balance data"""
    return {
        'income': 5000000,
        'expense': 700000,
        'balance': 4300000
    }


@pytest.fixture
def sample_category_report():
    """Sample category report"""
    return {
        'Gaji': {'income': 5000000, 'expense': 0},
        'Makanan': {'income': 0, 'expense': 500000},
        'Transport': {'income': 0, 'expense': 200000}
    }


# ============================================================================
# FILE SYSTEM MCP TESTS
# ============================================================================

def test_export_to_csv_success(mcp_manager, sample_transactions, sample_balance):
    """Test ekspor ke CSV berhasil"""
    result = mcp_manager.export_to_csv("test_user", sample_transactions, sample_balance)

    assert result["success"] == True
    assert "file_path" in result
    assert result["row_count"] == 3
    assert Path(result["file_path"]).exists()
    assert result["filename"].endswith(".csv")


def test_export_to_csv_empty_transactions(mcp_manager, sample_balance):
    """Test ekspor CSV dengan transaksi kosong"""
    result = mcp_manager.export_to_csv("test_user", [], sample_balance)

    assert result["success"] == False
    assert "Tidak ada transaksi" in result["message"]


def test_export_to_excel_success(mcp_manager, sample_transactions, sample_balance, sample_category_report):
    """Test ekspor ke Excel berhasil"""
    result = mcp_manager.export_to_excel(
        "test_user",
        sample_transactions,
        sample_balance,
        sample_category_report
    )

    assert result["success"] == True
    assert "file_path" in result
    assert result["row_count"] == 3
    assert Path(result["file_path"]).exists()
    assert result["filename"].endswith(".xlsx")
    assert "3 sheet" in result["message"]


def test_export_to_excel_empty_transactions(mcp_manager, sample_balance, sample_category_report):
    """Test ekspor Excel dengan transaksi kosong"""
    result = mcp_manager.export_to_excel("test_user", [], sample_balance, sample_category_report)

    assert result["success"] == False
    assert "Tidak ada transaksi" in result["message"]


# ============================================================================
# WEB SEARCH MCP TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_search_price_found(mcp_manager):
    """Test pencarian harga untuk item yang ditemukan"""
    result = await mcp_manager.search_price("laptop")

    assert result["success"] == True
    assert "price_range" in result
    assert "min" in result["price_range"]
    assert "max" in result["price_range"]
    assert "avg" in result["price_range"]
    assert result["item"] == "laptop"


@pytest.mark.asyncio
async def test_search_price_not_found(mcp_manager):
    """Test pencarian harga untuk item yang tidak ditemukan"""
    result = await mcp_manager.search_price("random_item_xyz")

    assert result["success"] == False
    assert "tidak menemukan" in result["message"].lower()


@pytest.mark.asyncio
async def test_search_price_partial_match(mcp_manager):
    """Test pencarian harga dengan partial match"""
    result = await mcp_manager.search_price("iPhone 15")

    assert result["success"] == True
    assert "price_range" in result


# ============================================================================
# DATABASE TOOLS MCP TESTS
# ============================================================================

def test_analyze_spending_trends_success(mcp_manager, sample_transactions):
    """Test analisis tren dengan data transaksi"""
    result = mcp_manager.analyze_spending_trends(sample_transactions)

    assert result["success"] == True
    assert "report" in result
    assert "Analisis Tren" in result["report"]
    assert "Top 5 Kategori" in result["report"]


def test_analyze_spending_trends_empty(mcp_manager):
    """Test analisis tren tanpa data"""
    result = mcp_manager.analyze_spending_trends([])

    assert result["success"] == False
    assert "Tidak ada data" in result["message"]


# ============================================================================
# CALENDAR/REMINDER MCP TESTS
# ============================================================================

def test_add_reminder_success(mcp_manager):
    """Test menambah reminder berhasil"""
    result = mcp_manager.add_reminder(
        "test_user",
        "Bayar listrik",
        "2025-02-01",
        "Tagihan"
    )

    assert result["success"] == True
    assert "reminder_id" in result
    assert "Bayar listrik" in result["message"]


def test_add_reminder_day_only(mcp_manager):
    """Test menambah reminder dengan tanggal saja (DD)"""
    result = mcp_manager.add_reminder(
        "test_user",
        "Bayar internet",
        "5",
        "Tagihan"
    )

    assert result["success"] == True
    assert "reminder_id" in result


def test_add_reminder_invalid_date(mcp_manager):
    """Test menambah reminder dengan tanggal tidak valid"""
    result = mcp_manager.add_reminder(
        "test_user",
        "Test reminder",
        "invalid-date",
        "Tagihan"
    )

    assert result["success"] == False
    assert "Format tanggal tidak valid" in result["message"]


def test_get_reminders_empty(mcp_manager):
    """Test ambil reminder ketika belum ada"""
    result = mcp_manager.get_reminders("test_user")

    assert result["success"] == True
    assert len(result["reminders"]) == 0
    assert "Belum ada reminder" in result["message"]


def test_get_reminders_with_data(mcp_manager):
    """Test ambil reminder dengan data"""
    # Add some reminders
    mcp_manager.add_reminder("test_user", "Reminder 1", "2025-02-01", "Tagihan")
    mcp_manager.add_reminder("test_user", "Reminder 2", "2025-02-05", "Tagihan")

    result = mcp_manager.get_reminders("test_user")

    assert result["success"] == True
    assert len(result["reminders"]) == 2


def test_complete_reminder_success(mcp_manager):
    """Test tandai reminder selesai"""
    # Add reminder
    add_result = mcp_manager.add_reminder("test_user", "Test reminder", "2025-02-01", "Tagihan")
    reminder_id = add_result["reminder_id"]

    # Complete it
    result = mcp_manager.complete_reminder("test_user", reminder_id)

    assert result["success"] == True
    assert "ditandai selesai" in result["message"]


def test_complete_reminder_not_found(mcp_manager):
    """Test tandai reminder yang tidak ada"""
    result = mcp_manager.complete_reminder("test_user", 999)

    assert result["success"] == False
    assert "tidak ditemukan" in result["message"]


def test_reminder_isolation_between_users(mcp_manager):
    """Test reminder terisolasi per user"""
    # Add reminder untuk user1
    mcp_manager.add_reminder("user1", "User 1 reminder", "2025-02-01", "Tagihan")

    # Add reminder untuk user2
    mcp_manager.add_reminder("user2", "User 2 reminder", "2025-02-01", "Tagihan")

    # Check user1 reminders
    result1 = mcp_manager.get_reminders("user1")
    assert len(result1["reminders"]) == 1
    assert "User 1 reminder" in result1["message"]

    # Check user2 reminders
    result2 = mcp_manager.get_reminders("user2")
    assert len(result2["reminders"]) == 1
    assert "User 2 reminder" in result2["message"]
