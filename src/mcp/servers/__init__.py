"""MCP Servers package"""

from .base_server import BaseMCPServer, MCPTool, MCPTransportType
from .highbyte_mock import HighByteMockServer
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
from .teradata_mock import TeradataMockServer
from .sqlserver_mock import SQLServerMockServer

__all__ = [
    # Base classes
    "BaseMCPServer",
    "MCPTool",
    "MCPTransportType",
    # HighByte (real MCP client)
    "HighByteServer",
    "HighByteConfig",
    "HighByteServerError",
    "HighByteConnectionError",
    "HighByteServerManager",
    "DiscoveredTool",
    "create_highbyte_client",
    "test_connection",
    # Mock servers
    "HighByteMockServer",
    "TeradataMockServer",
    "SQLServerMockServer",
]
