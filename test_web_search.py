"""
Test script for web-search-mcp integration
"""

import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from core.mcp_manager import MCPManager

# Fix Windows encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_web_search():
    """Test web search MCP integration"""

    print("=" * 60)
    print("Testing Web Search MCP Integration")
    print("=" * 60)

    # Initialize MCP Manager
    web_search_mcp_path = os.getenv("WEB_SEARCH_MCP_PATH", "C:\\Projects\\web-search-mcp-v0.3.2\\dist\\index.js")
    print(f"\n📍 Web Search MCP Path: {web_search_mcp_path}")

    mcp = MCPManager(web_search_mcp_path=web_search_mcp_path)
    print("✅ MCP Manager initialized\n")

    # Test cases
    test_items = [
        "iPhone 15 Pro",
        "laptop gaming",
        "PS5"
    ]

    for item in test_items:
        print(f"\n{'=' * 60}")
        print(f"🔍 Searching for: {item}")
        print(f"{'=' * 60}\n")

        try:
            result = await mcp.search_price(item, limit=3)

            if result['success']:
                print("✅ Search successful!")
                print(f"\nResults:\n{result['message']}")
            else:
                print(f"❌ Search failed: {result['message']}")

        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Search error for {item}: {e}", exc_info=True)

        print("\nWaiting 2 seconds before next search...")
        await asyncio.sleep(2)

    print(f"\n{'=' * 60}")
    print("✅ All tests completed!")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    asyncio.run(test_web_search())
