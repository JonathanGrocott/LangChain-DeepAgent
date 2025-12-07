"""MCP Client wrapper for Deep Agents

Connects to MCP servers and exposes their tools as LangChain-compatible tools.
"""

from typing import List, Dict, Any, Callable
from langchain_core.tools import Tool
from src.config import settings
from src.utils import get_logger
from .servers import HighByteMockServer, TeradataMockServer, SQLServerMockServer, BaseMCPServer

logger = get_logger(__name__)


class MCPClient:
    """
    MCP Client that manages connections to multiple MCP servers
    and exposes their tools to Deep Agents.
    """
    
    def __init__(self):
        self._servers: Dict[str, BaseMCPServer] = {}
        self._tools: List[Tool] = []
        self._initialize_servers()
    
    def _initialize_servers(self) -> None:
        """Initialize all enabled MCP servers"""
        logger.info("initializing_mcp_servers")
        
        # Initialize HighByte if enabled
        if settings.mcp_highbyte_enabled:
            server = HighByteMockServer()
            self._servers["highbyte"] = server
            logger.info("highbyte_server_initialized", tools=len(server.list_tools()))
        
        # Initialize Teradata if enabled
        if settings.mcp_teradata_enabled:
            server = TeradataMockServer()
            self._servers["teradata"] = server
            logger.info("teradata_server_initialized", tools=len(server.list_tools()))
        
        # Initialize SQL Server if enabled
        if settings.mcp_sqlserver_enabled:
            server = SQLServerMockServer()
            self._servers["sqlserver"] = server
            logger.info("sqlserver_server_initialized", tools=len(server.list_tools()))
        
        # Convert MCP tools to LangChain tools
        self._create_langchain_tools()
        
        logger.info(
            "mcp_client_ready",
            servers=len(self._servers),
            total_tools=len(self._tools)
        )
    
    def _create_langchain_tools(self) -> None:
        """Convert MCP server tools to LangChain Tool objects"""
        for server_name, server in self._servers.items():
            for tool_def in server.list_tools():
                # Create a wrapper function for this tool
                langchain_tool = self._create_tool_wrapper(
                    server=server,
                    tool_name=tool_def["name"],
                    tool_description=tool_def["description"]
                )
                self._tools.append(langchain_tool)
    
    def _create_tool_wrapper(
        self,
        server: BaseMCPServer,
        tool_name: str,
        tool_description: str
    ) -> Tool:
        """
        Create a LangChain Tool wrapper for an MCP tool.
        
        Args:
            server: The MCP server instance
            tool_name: Name of the tool
            tool_description: Description of the tool
            
        Returns:
            LangChain Tool object
        """
        def tool_func(input_str: str) -> str:
            """Execute the MCP tool and return result as string"""
            try:
                # Parse input - LangChain may pass JSON string or plain string
                import json
                try:
                    kwargs = json.loads(input_str) if input_str else {}
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, treat as empty args
                    kwargs = {}
                
                logger.info(
                    "mcp_tool_called",
                    server=server.server_name,
                    tool=tool_name,
                    args=kwargs
                )
                
                result = server.call_tool(tool_name, kwargs)
                
                if result.get("success"):
                    # Return data as formatted string
                    return str(result["data"])
                else:
                    error_msg = f"Error: {result.get('error', 'Unknown error')}"
                    logger.error(
                        "mcp_tool_error",
                        server=server.server_name,
                        tool=tool_name,
                        error=result.get("error")
                    )
                    return error_msg
                    
            except Exception as e:
                error_msg = f"Exception calling {tool_name}: {str(e)}"
                logger.error(
                    "mcp_tool_exception",
                    server=server.server_name,
                    tool=tool_name,
                    exception=str(e)
                )
                return error_msg
        
        # Create LangChain Tool
        return Tool(
            name=tool_name,
            description=tool_description,
            func=tool_func
        )
    
    def get_all_tools(self) -> List[Tool]:
        """Get all MCP tools as LangChain Tool objects"""
        return self._tools
    
    def get_tools_for_server(self, server_name: str) -> List[Tool]:
        """
        Get tools for a specific server.
        
        Args:
            server_name: Name of the server (e.g., 'highbyte', 'teradata', 'sqlserver')
            
        Returns:
            List of LangChain Tools for that server
        """
        if server_name not in self._servers:
            logger.warning("unknown_server_requested", server=server_name)
            return []
        
        server = self._servers[server_name]
        server_tool_names = [tool["name"] for tool in server.list_tools()]
        
        return [
            tool for tool in self._tools
            if tool.name in server_tool_names
        ]
    
    def get_tools_by_names(self, tool_names: List[str]) -> List[Tool]:
        """
        Get specific tools by name.
        
        Args:
            tool_names: List of tool names to retrieve
            
        Returns:
            List of matching LangChain Tools
        """
        return [
            tool for tool in self._tools
            if tool.name in tool_names
        ]
    
    def list_available_servers(self) -> List[str]:
        """List all available server names"""
        return list(self._servers.keys())
    
    def get_server_info(self, server_name: str) -> Dict[str, Any]:
        """Get information about a specific server"""
        if server_name not in self._servers:
            return {"error": f"Server '{server_name}' not found"}
        
        return self._servers[server_name].get_server_info()
    
    def get_all_tool_names(self) -> List[str]:
        """Get list of all available tool names"""
        return [tool.name for tool in self._tools]


# Global MCP client instance
_mcp_client: MCPClient = None


def get_mcp_client() -> MCPClient:
    """
    Get or create the global MCP client instance.
    
    Returns:
        MCPClient instance
    """
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client
