"""Tests for HighByte MCP Server Client"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.servers.highbyte_server import (
    HighByteServer,
    HighByteConfig,
    HighByteServerError,
    HighByteConnectionError,
    HighByteServerManager,
    DiscoveredTool,
    create_highbyte_client,
    test_connection,
)


class TestHighByteConfig:
    """Tests for HighByteConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = HighByteConfig()
        
        assert config.url == "http://localhost:45345/mcp"
        assert config.bearer_token is None
        assert config.timeout == 30.0
        assert config.sse_read_timeout == 300.0
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = HighByteConfig(
            url="http://custom:8080/mcp",
            bearer_token="test-token",
            timeout=60.0,
            sse_read_timeout=600.0
        )
        
        assert config.url == "http://custom:8080/mcp"
        assert config.bearer_token == "test-token"
        assert config.timeout == 60.0
        assert config.sse_read_timeout == 600.0
    
    def test_headers_without_token(self):
        """Test headers generation without bearer token."""
        config = HighByteConfig()
        
        assert config.headers == {}
    
    def test_headers_with_token(self):
        """Test headers generation with bearer token."""
        config = HighByteConfig(bearer_token="my-secret-token")
        
        assert config.headers == {"Authorization": "Bearer my-secret-token"}


class TestHighByteServer:
    """Tests for HighByteServer."""
    
    def test_server_initialization(self):
        """Test server initialization with default config."""
        server = HighByteServer()
        
        assert server.server_name == "highbyte"
        assert "HighByte" in server.description
        assert not server.is_connected
        assert server.tools == {}
    
    def test_server_initialization_with_config(self):
        """Test server initialization with custom config."""
        config = HighByteConfig(
            url="http://test:1234/mcp",
            bearer_token="token123"
        )
        server = HighByteServer(config)
        
        assert server.config.url == "http://test:1234/mcp"
        assert server.config.bearer_token == "token123"
    
    def test_list_tools_empty(self):
        """Test list_tools when no tools discovered."""
        server = HighByteServer()
        
        assert server.list_tools() == []
    
    def test_get_server_info(self):
        """Test get_server_info returns correct metadata."""
        config = HighByteConfig(url="http://test:5000/mcp")
        server = HighByteServer(config)
        
        info = server.get_server_info()
        
        assert info["name"] == "highbyte"
        assert info["url"] == "http://test:5000/mcp"
        assert info["is_connected"] is False
        assert info["tools"] == []
        assert info["protocol_version"] == "1.0"


class TestDiscoveredTool:
    """Tests for DiscoveredTool dataclass."""
    
    def test_tool_creation(self):
        """Test creating a discovered tool."""
        tool = DiscoveredTool(
            name="get_tag_value",
            description="Get value of a tag",
            input_schema={
                "type": "object",
                "properties": {
                    "tag_id": {"type": "string"}
                },
                "required": ["tag_id"]
            }
        )
        
        assert tool.name == "get_tag_value"
        assert tool.description == "Get value of a tag"
        assert "tag_id" in tool.input_schema["properties"]


class TestHighByteServerManager:
    """Tests for HighByteServerManager."""
    
    def test_manager_initialization(self):
        """Test manager initialization."""
        manager = HighByteServerManager()
        
        assert manager.config.url == "http://localhost:45345/mcp"
        assert manager._server is None
    
    def test_manager_with_custom_config(self):
        """Test manager initialization with custom config."""
        config = HighByteConfig(
            url="http://custom:9999/mcp",
            bearer_token="manager-token"
        )
        manager = HighByteServerManager(config)
        
        assert manager.config.url == "http://custom:9999/mcp"
        assert manager.config.bearer_token == "manager-token"


@pytest.mark.asyncio
class TestHighByteServerAsync:
    """Async tests for HighByteServer."""
    
    async def test_call_tool_unknown_tool(self):
        """Test calling unknown tool raises ValueError."""
        server = HighByteServer()
        
        with pytest.raises(ValueError, match="Unknown tool"):
            await server.call_tool("unknown_tool", {})
    
    @patch("src.mcp.servers.highbyte_server.streamablehttp_client")
    async def test_discover_tools_success(self, mock_client):
        """Test successful tool discovery."""
        # Create mock tool
        mock_tool = MagicMock()
        mock_tool.name = "test_tool"
        mock_tool.description = "A test tool"
        mock_tool.inputSchema = {"type": "object", "properties": {}}
        
        # Create mock session
        mock_session = AsyncMock()
        mock_session.initialize = AsyncMock()
        mock_session.list_tools = AsyncMock(return_value=MagicMock(tools=[mock_tool]))
        
        # Create mock context manager for session
        mock_session_ctx = MagicMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
        
        # Create mock get_session_id callback
        mock_get_session_id = MagicMock(return_value="test-session-123")
        
        # Create mock streams
        mock_read_stream = MagicMock()
        mock_write_stream = MagicMock()
        
        # Create mock context manager for client
        mock_client_ctx = MagicMock()
        mock_client_ctx.__aenter__ = AsyncMock(
            return_value=(mock_read_stream, mock_write_stream, mock_get_session_id)
        )
        mock_client_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_client.return_value = mock_client_ctx
        
        # Patch ClientSession
        with patch("src.mcp.servers.highbyte_server.ClientSession") as mock_client_session:
            mock_client_session.return_value = mock_session_ctx
            
            server = HighByteServer()
            tools = await server.discover_tools()
            
            assert len(tools) == 1
            assert tools[0].name == "test_tool"
            assert tools[0].description == "A test tool"
            assert server.is_connected


@pytest.mark.asyncio
class TestHighByteHelperFunctions:
    """Tests for helper functions."""
    
    @patch("src.mcp.servers.highbyte_server.HighByteServer")
    async def test_create_highbyte_client(self, mock_server_class):
        """Test create_highbyte_client helper function."""
        mock_server = MagicMock()
        mock_server.discover_tools = AsyncMock()
        mock_server_class.return_value = mock_server
        
        result = await create_highbyte_client(
            url="http://test:1234/mcp",
            bearer_token="test-token",
            timeout=45.0
        )
        
        assert result == mock_server
        mock_server.discover_tools.assert_called_once()
    
    @patch("src.mcp.servers.highbyte_server.HighByteServer")
    async def test_test_connection_success(self, mock_server_class):
        """Test test_connection returns True on success."""
        mock_server = MagicMock()
        mock_server.discover_tools = AsyncMock()
        mock_server.is_connected = True
        mock_server_class.return_value = mock_server
        
        result = await test_connection(url="http://test:1234/mcp")
        
        assert result is True
    
    @patch("src.mcp.servers.highbyte_server.HighByteServer")
    async def test_test_connection_failure(self, mock_server_class):
        """Test test_connection returns False on failure."""
        mock_server = MagicMock()
        mock_server.discover_tools = AsyncMock(
            side_effect=HighByteConnectionError("Connection failed")
        )
        mock_server_class.return_value = mock_server
        
        result = await test_connection(url="http://test:1234/mcp")
        
        assert result is False
