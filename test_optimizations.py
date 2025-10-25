"""
Test script to verify all optimizations work correctly
"""

import asyncio
import time
import sys
import codecs
import os
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

load_dotenv()

from core.llm_agent import LLMAgent
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore
from core.mcp_manager import MCPManager

async def test_optimizations():
    """Test all optimizations"""
    print("=" * 80)
    print("PERFORMANCE OPTIMIZATION TEST SUITE")
    print("=" * 80)

    # Initialize
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")

    llm = LLMAgent(api_key, model)
    db = DatabaseManager("test_optim.db")
    mcp = MCPManager()

    bot_core = FinancialBotCore(llm, db, mcp)

    test_cases = [
        ("Simple intent extraction", "aku dapat gaji 5 juta"),
        ("Balance check", "berapa saldo aku?"),
        ("Price search", "berapa harga iPhone 15 Pro?"),
    ]

    print("\n📊 Running Performance Tests...\n")

    for test_name, message in test_cases:
        print(f"\n{'=' * 80}")
        print(f"TEST: {test_name}")
        print(f"Message: {message}")
        print(f"{'=' * 80}")

        start_time = time.time()

        try:
            response = await bot_core.process_message("test_user", "Test User", message)

            elapsed = time.time() - start_time

            print(f"\n⏱️  Response Time: {elapsed:.2f}s")
            print(f"\n📤 Response Preview:")
            if isinstance(response, str):
                print(response[:300] + ("..." if len(response) > 300 else ""))
            else:
                print(response)

            # Performance targets
            if "saldo" in message.lower():
                target = 1.5
            elif "harga" in message.lower():
                target = 13.0
            else:
                target = 1.2

            if elapsed <= target:
                print(f"✅ PASS - Within target ({target}s)")
            else:
                print(f"⚠️  SLOW - Exceeded target ({target}s) by {elapsed - target:.2f}s")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 80}")
    print("✅ All tests completed!")
    print(f"{'=' * 80}\n")

    # Cleanup
    os.remove("test_optim.db")

if __name__ == "__main__":
    asyncio.run(test_optimizations())
