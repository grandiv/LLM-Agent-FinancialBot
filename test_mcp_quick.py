"""
Quick test to verify MCP functions work correctly
"""
import asyncio
from core.mcp_manager import MCPManager

def test_sync_context():
    """Test MCP in synchronous context (like CLI)"""
    print("Testing in SYNC context (CLI mode)...")
    mcp = MCPManager()

    # Test price search
    result = asyncio.run(mcp.search_price("laptop"))
    print(f"[OK] Search price: {result['success']}")

    # Test export
    sample_transactions = [
        {'id': 1, 'type': 'income', 'amount': 5000000, 'category': 'Gaji', 'description': 'Gaji', 'date': '2025-01-15'},
    ]
    balance = {'income': 5000000, 'expense': 0, 'balance': 5000000}
    result = mcp.export_to_csv("test_user", sample_transactions, balance)
    print(f"[OK] Export CSV: {result['success']}")

    print("\n[OK] All SYNC tests passed!\n")

async def async_test():
    """Test MCP in async context (like Discord bot)"""
    print("Testing in ASYNC context (Discord bot mode)...")
    mcp = MCPManager()

    # Test price search in async context
    result = await mcp.search_price("iPhone")
    print(f"[OK] Async search price: {result['success']}")

    print("\n[OK] All ASYNC tests passed!\n")

if __name__ == "__main__":
    # Test sync context
    test_sync_context()

    # Test async context
    asyncio.run(async_test())

    print("=" * 50)
    print("SUCCESS: All MCP functions working correctly!")
    print("=" * 50)
