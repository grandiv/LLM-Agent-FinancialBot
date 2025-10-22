"""
Quick test to verify bot functionality
"""

import os
import sys
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from core.llm_agent import LLMAgent
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore

load_dotenv()

def test_bot():
    """Test bot with a simple message"""
    print("🔧 Testing FinancialBot...")
    print(f"📦 Model: {os.getenv('OLLAMA_MODEL', 'llama3.1:8b')}")

    # Initialize components
    db = DatabaseManager("test_quick.db")
    api_key = os.getenv("OLLAMA_API_KEY")
    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    llm_agent = LLMAgent(api_key=api_key, model=model, base_url=base_url)
    bot_core = FinancialBotCore(llm_agent, db)

    print("✅ Bot initialized\n")

    # Test message
    test_message = "aku dapat gaji 5 juta"
    print(f"📤 Testing message: '{test_message}'")
    print("⏳ Processing...\n")

    try:
        response = bot_core.process_message("test_user", "Test User", test_message)
        print("✅ SUCCESS!\n")
        print("📥 Bot Response:")
        print("-" * 50)
        print(response)
        print("-" * 50)

        # Check balance
        print("\n📊 Verifying database...")
        balance = db.get_user_balance("test_user")
        print(f"Income: Rp {balance['income']:,.0f}")
        print(f"Expense: Rp {balance['expense']:,.0f}")
        print(f"Balance: Rp {balance['balance']:,.0f}")

        if balance['income'] == 5000000:
            print("\n✅ All tests PASSED! Bot is working correctly! 🎉")
        else:
            print(f"\n⚠️ Warning: Expected income 5,000,000 but got {balance['income']}")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    # Cleanup
    if os.path.exists("test_quick.db"):
        os.remove("test_quick.db")

if __name__ == "__main__":
    test_bot()
