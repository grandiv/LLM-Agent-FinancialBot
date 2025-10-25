"""
Test Web Search MCP integration
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def test_web_search():
    print("\n" + "=" * 60)
    print("🧪 Testing Web Search MCP")
    print("=" * 60 + "\n")

    # Check if path is configured
    mcp_path = os.getenv("WEB_SEARCH_MCP_PATH")
    if not mcp_path:
        print("❌ WEB_SEARCH_MCP_PATH not set in .env")
        print("\nPlease add to .env:")
        print("WEB_SEARCH_MCP_PATH=C:/mcp-servers/web-search-mcp/dist/index.js")
        return False

    print(f"✅ MCP Path: {mcp_path}")

    # Check if file exists
    if not os.path.exists(mcp_path):
        print(f"❌ File not found: {mcp_path}")
        print("\nPlease:")
        print("1. Download web-search-mcp from: https://github.com/mrkrsl/web-search-mcp/releases")
        print("2. Extract to a permanent location")
        print("3. Run: npm install && npx playwright install && npm run build")
        print("4. Update WEB_SEARCH_MCP_PATH in .env")
        return False

    print(f"✅ File exists: {mcp_path}")
    print()

    # Import MCP components
    try:
        from core.mcp_manager import MCPManager
        print("✅ MCP Manager imported")
    except Exception as e:
        print(f"❌ Failed to import MCP Manager: {e}")
        return False

    # Create MCP manager
    mcp = MCPManager()
    print("✅ MCP Manager created")
    print()

    # Initialize MCP
    print("🔄 Initializing Web Search MCP...")
    print("   (This may take 10-30 seconds on first run)")
    try:
        await asyncio.wait_for(mcp.initialize_mcp(), timeout=60.0)
        print("✅ MCP initialized successfully!")
        print()
    except asyncio.TimeoutError:
        print("⏱️  MCP initialization timed out (60s)")
        print("   This may indicate:")
        print("   - Node.js not installed")
        print("   - Playwright browsers not installed")
        print("   - Incorrect path in .env")
        await mcp.mcp_client.cleanup()
        return False
    except Exception as e:
        print(f"❌ MCP initialization failed: {e}")
        print()
        import traceback
        traceback.print_exc()
        await mcp.mcp_client.cleanup()
        return False

    # Check connection
    if not mcp.mcp_client.is_connected("web-search"):
        print("⚠️  Web Search MCP not connected")
        print("   Bot will use database fallback")
        await mcp.mcp_client.cleanup()
        return False

    print("=" * 60)
    print("✅ Web Search MCP is CONNECTED!")
    print("=" * 60)
    print()

    # Test price search
    print("🔍 Testing price search for 'iPhone 15 Pro'...")
    print("   (Will use optimized query for official Apple retailers)")
    print()

    try:
        result = await mcp.search_price("iPhone 15 Pro")

        print("\n" + "=" * 60)
        print("📊 Search Result:")
        print("=" * 60)
        print(result.get("message", "No message"))
        print("=" * 60)
        print()

        if result.get("success"):
            source = result.get("source", "Unknown")
            print("✅ Price search SUCCESSFUL!")
            print(f"   Source: {source}")

            if "Web Search MCP" in source:
                print("   ✨ Using real-time web search!")
            elif "Database" in source:
                print("   ⚠️  Using database fallback (no prices found online)")

            print()
            return True
        else:
            print("⚠️  Search completed but returned no success")
            print(f"   Error: {result.get('message', 'Unknown')}")
            return False

    except Exception as e:
        print(f"❌ Error during price search: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Always cleanup MCP connections before exiting
        print("🧹 Cleaning up MCP connections...")
        await mcp.mcp_client.cleanup()
        print("✅ Cleanup complete")


async def main():
    """Run test"""
    print()
    print("=" * 60)
    print("🚀 Web Search MCP Integration Test")
    print("=" * 60)

    result = await test_web_search()

    print()
    print("=" * 60)
    print("📊 Test Result")
    print("=" * 60)

    if result:
        print("✅ TEST PASSED!")
        print()
        print("🎉 Your bot can now perform real-time price searches!")
        print("   • No API keys required")
        print("   • Unlimited searches")
        print("   • Bing + Brave + DuckDuckGo fallback")
        print()
        return 0
    else:
        print("❌ TEST FAILED")
        print()
        print("Please check:")
        print("1. Node.js installed (node --version)")
        print("2. Web Search MCP downloaded and built")
        print("3. WEB_SEARCH_MCP_PATH correct in .env")
        print("4. Playwright browsers installed (npx playwright install)")
        print()
        print("See WEB_SEARCH_MCP_SETUP.md for detailed instructions")
        print()
        return 1


if __name__ == "__main__":
    import sys
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
