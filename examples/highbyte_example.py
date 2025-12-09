#!/usr/bin/env python3
"""
Example: Using the HighByte MCP Server Client

This example demonstrates how to connect to a HighByte Intelligence Hub
MCP server and discover/call tools.

Prerequisites:
1. Install dependencies: pip install -r requirements.txt
2. Have a HighByte MCP server running at localhost:45345/mcp
3. Set the HIGHBYTE_MCP_BEARER_TOKEN environment variable if authentication is required

Usage:
    python examples/highbyte_example.py
"""

import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mcp.servers.highbyte_server import (
    HighByteServer,
    HighByteConfig,
    HighByteServerManager,
    create_highbyte_client,
    test_connection,
    HighByteConnectionError,
)


async def basic_example():
    """Basic example of connecting and discovering tools."""
    print("=" * 60)
    print("HighByte MCP Server - Basic Example")
    print("=" * 60)
    
    # Get configuration from environment or use defaults
    url = os.getenv("HIGHBYTE_MCP_URL", "http://localhost:45345/mcp")
    bearer_token = os.getenv("HIGHBYTE_MCP_BEARER_TOKEN")
    
    print(f"\nConnecting to: {url}")
    print(f"Authentication: {'Bearer token configured' if bearer_token else 'None'}")
    
    # Test connection first
    print("\nTesting connection...")
    is_connected = await test_connection(url=url, bearer_token=bearer_token)
    
    if not is_connected:
        print("❌ Failed to connect to HighByte server")
        print("\nTroubleshooting:")
        print("  1. Ensure the HighByte server is running")
        print("  2. Check the URL is correct")
        print("  3. Verify the bearer token if authentication is required")
        return
    
    print("✅ Connection successful!")
    
    # Create client and discover tools
    print("\nDiscovering tools...")
    
    try:
        client = await create_highbyte_client(
            url=url,
            bearer_token=bearer_token
        )
        
        print(f"\n📦 Server Info:")
        info = client.get_server_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        print(f"\n🔧 Discovered Tools ({len(client.tools)}):")
        for tool_name, tool in client.tools.items():
            print(f"\n  📌 {tool_name}")
            print(f"     Description: {tool.description[:80]}..." if len(tool.description) > 80 else f"     Description: {tool.description}")
            print(f"     Schema: {tool.input_schema}")
            
    except HighByteConnectionError as e:
        print(f"❌ Connection error: {e}")


async def manager_example():
    """Example using HighByteServerManager for cached connections."""
    print("\n" + "=" * 60)
    print("HighByte MCP Server - Manager Example")
    print("=" * 60)
    
    url = os.getenv("HIGHBYTE_MCP_URL", "http://localhost:45345/mcp")
    bearer_token = os.getenv("HIGHBYTE_MCP_BEARER_TOKEN")
    
    config = HighByteConfig(
        url=url,
        bearer_token=bearer_token
    )
    
    manager = HighByteServerManager(config)
    
    print("\nUsing ServerManager (with caching)...")
    
    try:
        # First call - will discover tools
        server = await manager.get_server()
        print(f"First call - Tools discovered: {len(server.tools)}")
        
        # Second call - will use cached server
        server = await manager.get_server()
        print(f"Second call - Tools from cache: {len(server.tools)}")
        
        # Force refresh
        tools = await manager.refresh_tools()
        print(f"Forced refresh - Tools discovered: {len(tools)}")
        
    except HighByteConnectionError as e:
        print(f"❌ Connection error: {e}")


async def tool_call_example():
    """Example of calling a tool on the HighByte server."""
    print("\n" + "=" * 60)
    print("HighByte MCP Server - Tool Call Example")
    print("=" * 60)
    
    url = os.getenv("HIGHBYTE_MCP_URL", "http://localhost:45345/mcp")
    bearer_token = os.getenv("HIGHBYTE_MCP_BEARER_TOKEN")
    
    try:
        client = await create_highbyte_client(
            url=url,
            bearer_token=bearer_token
        )
        
        if not client.tools:
            print("No tools available on the server")
            return
        
        # Get the first tool
        first_tool_name = list(client.tools.keys())[0]
        first_tool = client.tools[first_tool_name]
        
        print(f"\n🔧 Calling tool: {first_tool_name}")
        print(f"   Description: {first_tool.description}")
        print(f"   Input Schema: {first_tool.input_schema}")
        
        # For this example, we'll call with empty args
        # In a real scenario, you'd provide proper arguments
        print("\n   Note: This example uses empty arguments.")
        print("   Modify the code to provide proper arguments for your tool.")
        
        # Uncomment to actually call the tool:
        # result = await client.call_tool(first_tool_name, {})
        # print(f"\n   Result: {result}")
        
    except HighByteConnectionError as e:
        print(f"❌ Connection error: {e}")


async def main():
    """Run all examples."""
    print("\n🚀 HighByte MCP Server Examples")
    print("================================\n")
    
    # Run basic example
    await basic_example()
    
    # Run manager example
    await manager_example()
    
    # Run tool call example
    await tool_call_example()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
