"""
Test the new formatted search results
"""

import asyncio
import logging
import os
import sys
import codecs
from dotenv import load_dotenv
from core.mcp_manager import MCPManager

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_formatted_search():
    """Test formatted web search"""

    print("=" * 60)
    print("Testing Formatted Web Search Results")
    print("=" * 60)

    # Initialize MCP Manager
    web_search_mcp_path = os.getenv("WEB_SEARCH_MCP_PATH", "C:\\Projects\\web-search-mcp-v0.3.2\\dist\\index.js")
    mcp = MCPManager(web_search_mcp_path=web_search_mcp_path)

    # Test search
    item = "iPhone 15 Pro"
    print(f"\n🔍 Searching for: {item}\n")
    print("Please wait 10-15 seconds...\n")

    try:
        result = await mcp.search_price(item, limit=3)

        if result['success']:
            print(result['message'])
        else:
            print(f"❌ Search failed: {result['message']}")

    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Search error: {e}", exc_info=True)

    print(f"\n{'=' * 60}")
    print("✅ Test completed!")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    asyncio.run(test_formatted_search())
