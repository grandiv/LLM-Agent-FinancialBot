"""
Test LLM-powered search result formatting
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
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore
from core.mcp_manager import MCPManager

# Sample structured data (like what _extract_search_data returns)
SAMPLE_DATA = [
    {
        "title": "Daftar Harga iPhone 17, iPhone 17 Pro, iPhone 17 Pro Max, dan iPhone Air di Indonesia",
        "url": "https://www.liputan6.com/tekno/read/6179112/daftar-harga-iphone-17-iphone-17-pro-iphone-17-pro-max-dan-iphone-air-di-indonesia",
        "content": "Harga iPhone 17 Pro Max di Indonesia: iPhone 17 Pro Max 256GB Rp 25.999.000, iPhone 17 Pro Max 512GB Rp 29.999.000, iPhone 17 Pro Max 1TB Rp 35.999.000"
    },
    {
        "title": "iPhone 17 Pro Max Harga Di Indonesia",
        "url": "https://www.gsmarena.id/harga-apple-iphone-17-pro-max",
        "content": "Harga Resmi iPhone 17 Pro Max di Indonesia: Harga untuk varian 256GB dipatok Rp 26.999.000, varian 512GB Rp 31.499.000, dan varian 1TB Rp 37.999.000"
    },
    {
        "title": "Spesifikasi dan Harga iPhone 17 Pro Max Terbaru",
        "url": "https://www.kompas.com/tekno/iphone-17-pro-max",
        "content": "Pre-order iPhone 17 Pro Max dibuka dengan harga mulai Rp 27.499.000 untuk variant 256GB. iPhone 17 Pro Max hadir dengan chip A19 Pro dan kamera 48MP."
    }
]

print("=" * 60)
print("Testing LLM-Powered Search Formatting")
print("=" * 60)

# Initialize components
api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")

llm = LLMAgent(api_key, model)
db = DatabaseManager(":memory:")  # In-memory for testing
mcp = MCPManager()

bot_core = FinancialBotCore(llm, db, mcp)

print("\n📊 Input Data:")
print(f"Item: iPhone 17 Pro Max")
print(f"Sources: {len(SAMPLE_DATA)}")
print("\n⚙️ Sending to LLM for intelligent formatting...\n")

# Test the LLM formatting
result = bot_core._format_search_with_llm("iPhone 17 Pro Max", SAMPLE_DATA)

print("=" * 60)
print("✨ LLM-Formatted Output:")
print("=" * 60)
print(result)
print("=" * 60)
