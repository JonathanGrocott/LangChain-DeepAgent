"""MCP (Model Context Protocol) package - Client and server implementations"""

from .servers import (
    BaseMCPServer,
    MCPTool,
    MCPTransportType,
    HighByteMockServer,
    TeradataMockServer,
    SQLServerMockServer,
)

# Client requires LangChain, import conditionally
try:
    from .client import MCPClient, get_mcp_client
    __all__ = [
        "MCPClient",
        "get_mcp_client",
        "BaseMCPServer",
        "MCPTool",
        "MCPTransportType",
        "HighByteMockServer",
        "TeradataMockServer",
        "SQLServerMockServer",
    ]
except ImportError:
    # LangChain not installed, only export servers
    __all__ = [
        "BaseMCPServer",
        "MCPTool",
        "MCPTransportType",
        "HighByteMockServer",
        "TeradataMockServer",
        "SQLServerMockServer",
    ]

