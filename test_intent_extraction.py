"""
Test that LLM extracts exact item names for search_price intent
"""

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

print("=" * 60)
print("Testing Intent Extraction for search_price")
print("=" * 60)

# Initialize LLM
api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
llm = LLMAgent(api_key, model)

# Test messages
test_cases = [
    "berapa harga iPhone 17 Pro Max?",
    "cek harga PS6",
    "harga Samsung Galaxy S25 Ultra berapa?",
]

for message in test_cases:
    print(f"\n{'=' * 60}")
    print(f"User: {message}")
    print(f"{'=' * 60}")

    # Process message
    result = llm.process_message(
        user_id="test_user",
        username="Test User",
        message=message,
        balance_data={'income': 0, 'expense': 0, 'balance': 0},
        recent_transactions=[]
    )

    print(f"Intent: {result.get('intent')}")
    print(f"Item Name: {result.get('item_name')}")
    print(f"Response: {result.get('response_text', '')[:100]}...")

    # Check if item name is exact
    if result.get('intent') == 'search_price':
        item_name = result.get('item_name', '')
        if 'iPhone 17 Pro Max' in message and item_name == 'iPhone 17 Pro Max':
            print("✅ CORRECT - Exact item name extracted!")
        elif 'PS6' in message and item_name == 'PS6':
            print("✅ CORRECT - Exact item name extracted!")
        elif 'Samsung Galaxy S25 Ultra' in message and item_name == 'Samsung Galaxy S25 Ultra':
            print("✅ CORRECT - Exact item name extracted!")
        else:
            print(f"❌ WRONG - Expected exact match, got: {item_name}")

print(f"\n{'=' * 60}")
print("Test Complete!")
print(f"{'=' * 60}")
