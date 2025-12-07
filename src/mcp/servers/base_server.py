"""Base MCP Server abstraction for mock manufacturing data sources"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class MCPTransportType(Enum):
    """Supported MCP transport types"""
    STDIO = "stdio"
    SSE = "sse"
    HTTP = "http"


@dataclass
class MCPTool:
    """Definition of an MCP tool"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable


class BaseMCPServer(ABC):
    """
    Abstract base class for MCP servers.
    
    Provides common interface for all MCP mock servers regardless of transport type.
    Each server implements specific manufacturing data source logic.
    """
    
    def __init__(self, server_name: str, description: str):
        self.server_name = server_name
        self.description = description
        self._tools: Dict[str, MCPTool] = {}
        self._register_tools()
    
    @abstractmethod
    def _register_tools(self) -> None:
        """Register all tools this server provides. Must be implemented by subclasses."""
        pass
    
    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable
    ) -> None:
        """
        Register a tool with the server.
        
        Args:
            name: Tool name (e.g., "get_realtime_data")
            description: Human-readable description
            input_schema: JSON schema for tool inputs
            handler: Function that implements the tool
        """
        tool = MCPTool(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=handler
        )
        self._tools[name] = tool
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools.
        
        Returns:
            List of tool definitions in MCP format
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in self._tools.values()
        ]
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with given arguments.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments as dict
            
        Returns:
            Tool result as dict
            
        Raises:
            ValueError: If tool doesn't exist
        """
        if tool_name not in self._tools:
            raise ValueError(
                f"Unknown tool: {tool_name}. Available: {list(self._tools.keys())}"
            )
        
        tool = self._tools[tool_name]
        
        try:
            result = tool.handler(**arguments)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server metadata"""
        return {
            "name": self.server_name,
            "description": self.description,
            "tools": [tool.name for tool in self._tools.values()],
            "protocol_version": "1.0"
        }
