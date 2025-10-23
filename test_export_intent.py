"""
Quick test to verify export intent is recognized correctly
"""
import os
from dotenv import load_dotenv
from core.llm_agent import LLMAgent
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore

load_dotenv()

# Initialize components
db = DatabaseManager("test_export.db")
llm = LLMAgent(os.getenv("OPENROUTER_API_KEY"), os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku"))
bot_core = FinancialBotCore(llm, db)

# Add some test transactions
db.add_transaction("test_user", "Test User", "income", 5000000, "Gaji", "Gaji bulanan")
db.add_transaction("test_user", "Test User", "expense", 100000, "Makanan", "Makan")

# Test messages
test_messages = [
    "ekspor laporan aku ke excel",
    "export ke csv dong",
    "tolong buatkan laporan dalam format excel",
]

print("Testing Export Intent Recognition")
print("=" * 60)

for msg in test_messages:
    print(f"\nUser: {msg}")

    # Process message
    result = llm.process_message("test_user", "Test User", msg,
                                 db.get_user_balance("test_user"),
                                 db.get_user_transactions("test_user", 3))

    intent = result.get("intent")
    print(f"Intent: {intent}")
    print(f"Response: {result.get('response_text', '')[:100]}...")

    if intent == "export_report":
        print("[OK] Export intent recognized!")
        format_type = result.get("format", "csv")
        print(f"Format: {format_type}")

        # Test actual export
        response = bot_core._handle_export_report("test_user", result)
        if isinstance(response, dict) and "file_path" in response:
            print(f"[OK] File created: {response['file_path']}")
        else:
            print("[ERROR] No file_path in response!")
            print(f"Response type: {type(response)}")
            print(f"Response: {response}")
    else:
        print(f"[FAIL] Wrong intent! Expected export_report, got {intent}")

print("\n" + "=" * 60)
print("Test complete!")

# Cleanup
os.remove("test_export.db")
