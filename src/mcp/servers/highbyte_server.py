"""HighByte Intelligence Hub MCP Client

Connects to a real HighByte MCP server via streamable-http transport.
Discovers and exposes tools from the remote MCP server.
"""

import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

logger = logging.getLogger(__name__)


@dataclass
class HighByteConfig:
    """Configuration for HighByte MCP server connection."""
    
    url: str = "http://localhost:45345/mcp"
    bearer_token: Optional[str] = None
    timeout: float = 30.0
    sse_read_timeout: float = 300.0  # 5 minutes for SSE
    
    @property
    def headers(self) -> Dict[str, str]:
        """Build request headers including authorization."""
        headers = {}
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        return headers


@dataclass
class DiscoveredTool:
    """Represents a tool discovered from the HighByte MCP server."""
    
    name: str
    description: str
    input_schema: Dict[str, Any]


class HighByteServerError(Exception):
    """Exception raised for HighByte server errors."""
    pass


class HighByteConnectionError(HighByteServerError):
    """Exception raised when connection to HighByte fails."""
    pass


class HighByteServer:
    """
    HighByte MCP Server Client.
    
    Connects to a HighByte Intelligence Hub MCP server via streamable-http
    transport and exposes discovered tools for use in the agent system.
    
    Features:
    - Streamable HTTP transport with SSE support
    - Bearer token authentication
    - Automatic tool discovery
    - Session management
    
    Example:
        config = HighByteConfig(
            url="http://localhost:45345/mcp",
            bearer_token="your-token-here"
        )
        server = HighByteServer(config)
        
        # Discover tools
        tools = await server.discover_tools()
        
        # Call a tool
        result = await server.call_tool("get_tag_value", {"tag_id": "some-tag"})
    """
    
    def __init__(self, config: Optional[HighByteConfig] = None):
        """
        Initialize HighByte server client.
        
        Args:
            config: Configuration for the HighByte server connection.
                   If not provided, uses default localhost configuration.
        """
        self.config = config or HighByteConfig()
        self._discovered_tools: Dict[str, DiscoveredTool] = {}
        self._session: Optional[ClientSession] = None
        self._is_connected: bool = False
        
    @property
    def server_name(self) -> str:
        """Server identifier."""
        return "highbyte"
    
    @property
    def description(self) -> str:
        """Server description."""
        return "HighByte Intelligence Hub MCP Server"
    
    @property
    def is_connected(self) -> bool:
        """Check if connected to the server."""
        return self._is_connected
    
    @property
    def tools(self) -> Dict[str, DiscoveredTool]:
        """Get discovered tools."""
        return self._discovered_tools.copy()
    
    async def discover_tools(self) -> List[DiscoveredTool]:
        """
        Connect to the HighByte server and discover available tools.
        
        Returns:
            List of discovered tools from the MCP server.
            
        Raises:
            HighByteConnectionError: If connection to the server fails.
            HighByteServerError: If tool discovery fails.
        """
        logger.info(
            "discovering_highbyte_tools",
            extra={"url": self.config.url}
        )
        
        try:
            async with streamablehttp_client(
                url=self.config.url,
                headers=self.config.headers,
                timeout=self.config.timeout,
                sse_read_timeout=self.config.sse_read_timeout,
            ) as (read_stream, write_stream, get_session_id):
                async with ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # Get session ID for logging
                    session_id = get_session_id()
                    logger.info(
                        "highbyte_session_established",
                        extra={"session_id": session_id}
                    )
                    
                    # List available tools
                    tools_response = await session.list_tools()
                    
                    # Process discovered tools
                    self._discovered_tools.clear()
                    for tool in tools_response.tools:
                        discovered_tool = DiscoveredTool(
                            name=tool.name,
                            description=tool.description or "",
                            input_schema=tool.inputSchema if hasattr(tool, 'inputSchema') else {}
                        )
                        self._discovered_tools[tool.name] = discovered_tool
                    
                    self._is_connected = True
                    logger.info(
                        "highbyte_tools_discovered",
                        extra={"tool_count": len(self._discovered_tools)}
                    )
                    
                    return list(self._discovered_tools.values())
                    
        except httpx.ConnectError as e:
            logger.error(
                "highbyte_connection_failed",
                extra={"url": self.config.url, "error": str(e)}
            )
            raise HighByteConnectionError(
                f"Failed to connect to HighByte server at {self.config.url}: {e}"
            ) from e
        except httpx.TimeoutException as e:
            logger.error(
                "highbyte_connection_timeout",
                extra={"url": self.config.url, "error": str(e)}
            )
            raise HighByteConnectionError(
                f"Connection to HighByte server timed out: {e}"
            ) from e
        except Exception as e:
            logger.error(
                "highbyte_discovery_error",
                extra={"url": self.config.url, "error": str(e)}
            )
            raise HighByteServerError(
                f"Failed to discover tools from HighByte server: {e}"
            ) from e
    
    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a tool on the HighByte server.
        
        Args:
            tool_name: Name of the tool to call.
            arguments: Arguments to pass to the tool.
            
        Returns:
            Tool execution result.
            
        Raises:
            ValueError: If the tool is not found.
            HighByteConnectionError: If connection fails.
            HighByteServerError: If tool execution fails.
        """
        if tool_name not in self._discovered_tools:
            raise ValueError(
                f"Unknown tool: {tool_name}. "
                f"Available tools: {list(self._discovered_tools.keys())}. "
                "Call discover_tools() first to refresh the tool list."
            )
        
        logger.info(
            "highbyte_tool_call",
            extra={"tool": tool_name, "arguments": arguments}
        )
        
        try:
            async with streamablehttp_client(
                url=self.config.url,
                headers=self.config.headers,
                timeout=self.config.timeout,
                sse_read_timeout=self.config.sse_read_timeout,
            ) as (read_stream, write_stream, get_session_id):
                async with ClientSession(read_stream, write_stream) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # Call the tool
                    result = await session.call_tool(tool_name, arguments)
                    
                    # Process the result
                    response_data = {
                        "success": True,
                        "content": []
                    }
                    
                    for content_item in result.content:
                        if content_item.type == "text":
                            response_data["content"].append({
                                "type": "text",
                                "text": content_item.text
                            })
                        elif content_item.type == "image":
                            response_data["content"].append({
                                "type": "image",
                                "data": content_item.data,
                                "mimeType": content_item.mimeType
                            })
                        elif content_item.type == "resource":
                            response_data["content"].append({
                                "type": "resource",
                                "uri": str(content_item.resource.uri),
                                "text": getattr(content_item.resource, 'text', None)
                            })
                    
                    logger.info(
                        "highbyte_tool_success",
                        extra={"tool": tool_name}
                    )
                    
                    return response_data
                    
        except httpx.ConnectError as e:
            logger.error(
                "highbyte_tool_connection_failed",
                extra={"tool": tool_name, "error": str(e)}
            )
            raise HighByteConnectionError(
                f"Failed to connect to HighByte server: {e}"
            ) from e
        except Exception as e:
            logger.error(
                "highbyte_tool_error",
                extra={"tool": tool_name, "error": str(e)}
            )
            raise HighByteServerError(
                f"Failed to execute tool {tool_name}: {e}"
            ) from e
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all discovered tools in MCP format.
        
        Returns:
            List of tool definitions.
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in self._discovered_tools.values()
        ]
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server metadata."""
        return {
            "name": self.server_name,
            "description": self.description,
            "url": self.config.url,
            "is_connected": self._is_connected,
            "tools": list(self._discovered_tools.keys()),
            "protocol_version": "1.0"
        }


class HighByteServerManager:
    """
    Manager for HighByte server connections.
    
    Provides lifecycle management and tool caching for the HighByte
    MCP server connection.
    """
    
    def __init__(self, config: Optional[HighByteConfig] = None):
        self.config = config or HighByteConfig()
        self._server: Optional[HighByteServer] = None
        self._last_discovery: Optional[float] = None
        self._cache_ttl: float = 300.0  # 5 minutes cache TTL
    
    async def get_server(self, refresh: bool = False) -> HighByteServer:
        """
        Get the HighByte server instance, initializing if needed.
        
        Args:
            refresh: Force refresh of tool discovery.
            
        Returns:
            Configured HighByteServer instance.
        """
        if self._server is None:
            self._server = HighByteServer(self.config)
        
        # Check if we need to refresh tools
        import time
        current_time = time.time()
        needs_refresh = (
            refresh
            or not self._server.is_connected
            or self._last_discovery is None
            or (current_time - self._last_discovery) > self._cache_ttl
        )
        
        if needs_refresh:
            await self._server.discover_tools()
            self._last_discovery = current_time
        
        return self._server
    
    async def refresh_tools(self) -> List[DiscoveredTool]:
        """Force refresh of discovered tools."""
        server = await self.get_server(refresh=True)
        return list(server.tools.values())


# Convenience functions for simple usage

async def create_highbyte_client(
    url: str = "http://localhost:45345/mcp",
    bearer_token: Optional[str] = None,
    timeout: float = 30.0
) -> HighByteServer:
    """
    Create and initialize a HighByte server client.
    
    Args:
        url: HighByte MCP server URL.
        bearer_token: Optional bearer token for authentication.
        timeout: Connection timeout in seconds.
        
    Returns:
        Initialized HighByteServer instance with discovered tools.
    """
    config = HighByteConfig(
        url=url,
        bearer_token=bearer_token,
        timeout=timeout
    )
    server = HighByteServer(config)
    await server.discover_tools()
    return server


async def test_connection(
    url: str = "http://localhost:45345/mcp",
    bearer_token: Optional[str] = None
) -> bool:
    """
    Test connection to HighByte server.
    
    Args:
        url: HighByte MCP server URL.
        bearer_token: Optional bearer token for authentication.
        
    Returns:
        True if connection successful, False otherwise.
    """
    try:
        config = HighByteConfig(url=url, bearer_token=bearer_token)
        server = HighByteServer(config)
        await server.discover_tools()
        return server.is_connected
    except (HighByteConnectionError, HighByteServerError):
        return False
