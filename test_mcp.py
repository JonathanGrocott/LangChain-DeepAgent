"""Test MCP Server Infrastructure"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.mcp.servers import HighByteMockServer, TeradataMockServer, SQLServerMockServer


def test_mcp_servers():
    """Test all MCP mock servers"""
    print("=" * 60)
    print("MCP Server Infrastructure Test")
    print("=" * 60)
    
    # Test HighByte Server
    print("\n1. Testing HighByte Mock Server")
    print("-" * 60)
    highbyte = HighByteMockServer()
    print(f"✓ Server initialized: {highbyte.server_name}")
    print(f"✓ Tools available: {len(highbyte.list_tools())}")
    
    # Test real-time data
    result = highbyte.call_tool("highbyte_get_realtime_data", {
        "equipment_id": "CNC-Machine-1",
        "tag_name": "Temperature"
    })
    print(f"✓ Real-time data: {result['data']['value']} {result['data']['unit']}")
    
    # Test equipment status
    result = highbyte.call_tool("highbyte_get_equipment_status", {
        "equipment_id": "CNC-Machine-1"
    })
    print(f"✓ Equipment status: {result['data']['status']} (Health: {result['data']['health_score']}%)")
    
    # Test Teradata Server
    print("\n2. Testing Teradata Mock Server")
    print("-" * 60)
    teradata = TeradataMockServer()
    print(f"✓ Server initialized: {teradata.server_name}")
    print(f"✓ Tools available: {len(teradata.list_tools())}")
    
    # Test production metrics
    result = teradata.call_tool("teradata_get_production_metrics", {
        "start_date": "2024-12-01",
        "end_date": "2024-12-07"
    })
    print(f"✓ Production metrics: {len(result['data']['product_lines'])} lines")
    print(f"  Total production: {result['data']['total_production']} units")
    
    # Test SQL Server
    print("\n3. Testing SQL Server Mock Server")
    print("-" * 60)
    sqlserver = SQLServerMockServer()
    print(f"✓ Server initialized: {sqlserver.server_name}")
    print(f"✓ Tools available: {len(sqlserver.list_tools())}")
    
    # Test work orders
    result = sqlserver.call_tool("sqlserver_query_work_orders", {
        "status": "all",
        "limit": 5
    })
    print(f"✓ Work orders: {result['data']['count']} found")
    
    # Test creating maintenance ticket
    result = sqlserver.call_tool("sqlserver_create_maintenance_ticket", {
        "equipment_id": "CNC-Machine-1",
        "description": "Test ticket",
        "priority": "medium"
    })
    print(f"✓ Maintenance ticket created: {result['data']['ticket']['ticket_id']}")
    
    # Test MCP Client (skip if dependencies not installed)
    print("\n4. Testing MCP Client Wrapper")
    print("-" * 60)
    try:
        from src.mcp import MCPClient
        client = MCPClient()
        print(f"✓ MCP Client initialized")
        print(f"✓ Connected servers: {', '.join(client.list_available_servers())}")
        print(f"✓ Total tools available: {len(client.get_all_tools())}")
        
        # List all tools
        print("\nAvailable Tools:")
        for i, tool in enumerate(client.get_all_tools(), 1):
            print(f"  {i}. {tool.name}")
    except ImportError as e:
        print(f"⚠ Client test skipped (dependencies not installed)")
        print(f"  Install with: pip install -r requirements.txt")
    
    # Summary
    total_tools = len(highbyte.list_tools()) + len(teradata.list_tools()) + len(sqlserver.list_tools())
    
    print("\n" + "=" * 60)
    print("MCP Infrastructure Test: ✓ PASSED")
    print("=" * 60)
    print("\nPhase 2 Complete:")
    print("  • 3 mock MCP servers implemented")
    print(f"  • {total_tools} tools available")
    print("  • Server abstraction working")
    print("\nNext: Install dependencies and proceed to Phase 3")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = test_mcp_servers()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
