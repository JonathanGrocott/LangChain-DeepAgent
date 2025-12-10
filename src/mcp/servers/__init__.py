"""MCP Servers package"""

from .base_server import BaseMCPServer, MCPTool, MCPTransportType
from .highbyte_mock import HighByteMockServer
from .teradata_mock import TeradataMockServer
from .sqlserver_mock import SQLServerMockServer

# Optional: Real MCP client (requires 'mcp' package)
# Wrap in try/except to allow usage without the mcp package installed
try:
    from .highbyte_server import (
        HighByteServer,
        HighByteConfig,
        HighByteServerError,
        HighByteConnectionError,
        HighByteServerManager,
        DiscoveredTool,
        create_highbyte_client,
        test_connection,
    )
    _HAS_MCP = True
except ImportError:
    _HAS_MCP = False
    # Define placeholder classes for type hints when mcp not installed
    HighByteServer = None
    HighByteConfig = None
    HighByteServerError = None
    HighByteConnectionError = None
    HighByteServerManager = None
    DiscoveredTool = None
    create_highbyte_client = None
    test_connection = None

__all__ = [
    # Base classes
    "BaseMCPServer",
    "MCPTool",
    "MCPTransportType",
    # Mock servers
    "HighByteMockServer",
    "TeradataMockServer",
    "SQLServerMockServer",
    # HighByte (real MCP client) - requires 'mcp' package
    "HighByteServer",
    "HighByteConfig",
    "HighByteServerError",
    "HighByteConnectionError",
    "HighByteServerManager",
    "DiscoveredTool",
    "create_highbyte_client",
    "test_connection",
    "_HAS_MCP",
]
