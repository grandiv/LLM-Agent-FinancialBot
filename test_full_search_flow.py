"""
Debug the full search flow to see where iPhone 17 becomes iPhone 15
"""

import sys
import codecs
import os
import asyncio
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

print("=" * 80)
print("DEBUGGING: Full Search Flow for iPhone 17 Pro Max")
print("=" * 80)

# Initialize components
api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")

llm = LLMAgent(api_key, model)
db = DatabaseManager("test_debug.db")  # Use file database for debugging
mcp = MCPManager()

bot_core = FinancialBotCore(llm, db, mcp)

user_message = "berapa harga iPhone 17 Pro Max?"

print(f"\n📝 Step 1: User Message")
print(f"   Input: {user_message}")

# Step 2: LLM Intent Extraction
print(f"\n🤖 Step 2: LLM Intent Extraction")
llm_result = llm.process_message(
    user_id="debug_user",
    username="Debug User",
    message=user_message,
    balance_data={'income': 0, 'expense': 0, 'balance': 0},
    recent_transactions=[]
)

print(f"   Intent: {llm_result.get('intent')}")
print(f"   Item Name: {llm_result.get('item_name')}")
print(f"   Response Text: {llm_result.get('response_text', '')[:100]}...")

# Check if item_name is correct
item_name = llm_result.get('item_name', '')
if item_name != "iPhone 17 Pro Max":
    print(f"\n❌ PROBLEM FOUND AT STEP 2!")
    print(f"   Expected: 'iPhone 17 Pro Max'")
    print(f"   Got: '{item_name}'")
    print(f"   → LLM is changing the item name!")
else:
    print(f"\n✅ Step 2 OK - Item name is correct")

# Step 3: Web Search (via bot_core handler)
print(f"\n🌐 Step 3: Processing through bot_core")
response = bot_core.process_message(
    user_id="debug_user",
    username="Debug User",
    message=user_message
)

print(f"\n📤 Final Response Preview:")
print(f"{response[:500]}...")

print(f"\n{'=' * 80}")
print("Analysis:")
print("=" * 80)

if "iPhone 15" in response:
    print("❌ PROBLEM: Response mentions iPhone 15!")
    print("   Possible causes:")
    print("   1. LLM's response_text is overriding the search results")
    print("   2. Web search is not finding iPhone 17 data")
    print("   3. LLM formatter is using its own knowledge")
elif "iPhone 17" in response:
    print("✅ SUCCESS: Response correctly mentions iPhone 17!")
else:
    print("⚠️  UNCLEAR: Neither iPhone 15 nor 17 mentioned")

print(f"{'=' * 80}")
