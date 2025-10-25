"""
MCP Client Manager - Handles connections to MCP servers
"""

import os
import asyncio
import logging
from typing import Dict, Optional, List, Any
from contextlib import AsyncExitStack

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logging.warning("MCP SDK not installed. Run: pip install mcp")

logger = logging.getLogger(__name__)

# Suppress noisy MCP protocol warnings (debug logs on stdout)
logging.getLogger('mcp.client.stdio').setLevel(logging.CRITICAL)


class MCPClientManager:
    """Manages connections to MCP servers"""

    def __init__(self):
        """Initialize MCP client manager"""
        if not MCP_AVAILABLE:
            logger.error("MCP SDK is not available!")
            self.enabled = False
            return

        self.enabled = True
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        self.initialized = False
        self.available_tools: Dict[str, List[str]] = {}  # Store tool names per server

        logger.info("MCP Client Manager initialized")

    async def initialize(self):
        """Connect to all configured MCP servers"""
        if not self.enabled:
            logger.warning("MCP is disabled (SDK not installed)")
            return False

        if self.initialized:
            logger.info("MCP servers already initialized")
            return True

        try:
            # Connect to Web Search MCP (no API keys required!)
            web_search_path = os.getenv("WEB_SEARCH_MCP_PATH")

            if web_search_path:
                await self.connect_web_search(web_search_path)
            else:
                logger.warning("WEB_SEARCH_MCP_PATH not found, skipping Web Search MCP")
                logger.info("To enable: Set WEB_SEARCH_MCP_PATH to the dist/index.js path")

            self.initialized = True
            logger.info("MCP initialization complete")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize MCP servers: {e}", exc_info=True)
            return False

    async def connect_web_search(self, mcp_path: str):
        """
        Connect to Web Search MCP server (mrkrsl/web-search-mcp)

        Uses Bing, Brave, and DuckDuckGo search engines with automatic fallback.
        No API keys required!

        Args:
            mcp_path: Path to the web-search-mcp dist/index.js file
        """
        try:
            logger.info(f"Connecting to Web Search MCP at: {mcp_path}")

            # Optional environment variables for web-search-mcp
            env_vars = {
                "MAX_CONTENT_LENGTH": os.getenv("WEB_SEARCH_MAX_CONTENT_LENGTH", "50000"),
                "DEFAULT_TIMEOUT": os.getenv("WEB_SEARCH_TIMEOUT", "6000"),
                "MAX_BROWSERS": os.getenv("WEB_SEARCH_MAX_BROWSERS", "3"),
                "ENABLE_RELEVANCE_CHECKING": os.getenv("WEB_SEARCH_RELEVANCE_CHECK", "true"),
                "RELEVANCE_THRESHOLD": os.getenv("WEB_SEARCH_RELEVANCE_THRESHOLD", "0.3")
            }

            # Configure server
            server_params = StdioServerParameters(
                command="node",
                args=[mcp_path],
                env=env_vars
            )

            # Connect to server
            read, write = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )

            # Create session
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )

            # Initialize session (with timeout)
            try:
                await asyncio.wait_for(session.initialize(), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Web Search MCP timed out during initialization (30s)")
                raise

            # Store session
            self.sessions["web-search"] = session

            # List available tools
            tools_result = await session.list_tools()
            tool_names = [tool.name for tool in tools_result.tools]
            self.available_tools["web-search"] = tool_names

            logger.info(f"Connected to Web Search MCP")
            logger.info(f"   {len(tool_names)} tools available: {', '.join(tool_names)}")
            logger.info(f"   Search engines: Bing -> Brave -> DuckDuckGo (automatic fallback)")

        except Exception as e:
            error_msg = f"Failed to connect to Web Search MCP: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool on an MCP server

        Args:
            server_name: Name of the MCP server
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool result
        """
        if not self.enabled:
            raise RuntimeError("MCP is not enabled")

        session = self.sessions.get(server_name)
        if not session:
            available = list(self.sessions.keys())
            raise ValueError(
                f"Not connected to '{server_name}' MCP server. "
                f"Available servers: {available}"
            )

        try:
            logger.debug(f"Calling {server_name}.{tool_name} with args: {arguments}")
            result = await session.call_tool(tool_name, arguments)
            return result

        except Exception as e:
            logger.error(f"Error calling {server_name}.{tool_name}: {e}", exc_info=True)
            raise

    async def web_search(self, query: str, limit: int = 5, include_content: bool = False) -> Dict[str, Any]:
        """
        Perform web search using Web Search MCP

        Uses Bing -> Brave -> DuckDuckGo automatic fallback.
        No API keys required!

        Args:
            query: Search query
            limit: Number of results (1-10, default: 5)
            include_content: Extract full page content (slower but more detailed)

        Returns:
            Search results with titles, URLs, snippets, and optional content
        """
        if not self.enabled:
            raise RuntimeError("MCP is not enabled")

        # Check if connected
        if "web-search" not in self.sessions:
            raise RuntimeError("Not connected to Web Search MCP server")

        # Choose tool based on whether we need content
        if include_content:
            tool_name = "full-web-search"
        else:
            tool_name = "get-web-search-summaries"

        logger.debug(f"Using Web Search MCP tool: {tool_name}")

        result = await self.call_tool(
            server_name="web-search",
            tool_name=tool_name,
            arguments={
                "query": query,
                "limit": min(limit, 10)  # Max 10 results
            }
        )

        return result

    async def get_webpage_content(self, url: str, max_length: int = 50000) -> Dict[str, Any]:
        """
        Extract content from a specific webpage using Web Search MCP

        Args:
            url: Target webpage URL
            max_length: Maximum content length in characters

        Returns:
            Webpage content and metadata
        """
        if not self.enabled:
            raise RuntimeError("MCP is not enabled")

        if "web-search" not in self.sessions:
            raise RuntimeError("Not connected to Web Search MCP server")

        result = await self.call_tool(
            server_name="web-search",
            tool_name="get-single-web-page-content",
            arguments={
                "url": url,
                "maxContentLength": max_length
            }
        )

        return result

    async def cleanup(self):
        """Clean up MCP connections"""
        if not self.enabled:
            return

        try:
            logger.info("Cleaning up MCP connections...")
            await self.exit_stack.aclose()
            self.sessions.clear()
            self.initialized = False
            logger.info("MCP cleanup complete")

        except Exception as e:
            logger.error(f"Error during MCP cleanup: {e}", exc_info=True)

    def is_connected(self, server_name: str) -> bool:
        """Check if connected to a specific MCP server"""
        return server_name in self.sessions

    def get_available_servers(self) -> List[str]:
        """Get list of connected MCP servers"""
        return list(self.sessions.keys())
