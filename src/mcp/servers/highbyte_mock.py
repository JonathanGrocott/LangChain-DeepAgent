"""Mock HighByte Intelligence Hub MCP Server

Simulates real-time OPC-UA data and time-series queries for manufacturing equipment.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import random
from .base_server import BaseMCPServer


class HighByteMockServer(BaseMCPServer):
    """
    Mock HighByte server providing simulated OPC-UA data.
    
    Simulates:
    - Real-time tag data (temperature, pressure, speed, etc.)
    - Time-series historical data
    - Equipment status
    """
    
    def __init__(self):
        super().__init__(
            server_name="highbyte-mock",
            description="Mock HighByte Intelligence Hub for OPC-UA data simulation"
        )
        
        # Simulated equipment and tags
        self._equipment = {
            "CNC-Machine-1": ["Temperature", "Speed", "Vibration", "Status"],
            "CNC-Machine-2": ["Temperature", "Speed", "Vibration", "Status"],
            "CNC-Machine-3": ["Temperature", "Speed", "Vibration", "Status"],
            "Conveyor-A": ["Speed", "Load", "Status"],
            "Conveyor-B": ["Speed", "Load", "Status"],
            "Press-1": ["Force", "Temperature", "CycleCount", "Status"],
        }
    
    def _register_tools(self) -> None:
        """Register HighByte-specific tools"""
        
        # Tool 1: Get real-time data
        self.register_tool(
            name="highbyte_get_realtime_data",
            description="Get current real-time value for an OPC-UA tag",
            input_schema={
                "type": "object",
                "properties": {
                    "equipment_id": {
                        "type": "string",
                        "description": "Equipment identifier (e.g., 'CNC-Machine-1')"
                    },
                    "tag_name": {
                        "type": "string",
                        "description": "Tag name (e.g., 'Temperature', 'Speed')"
                    }
                },
                "required": ["equipment_id", "tag_name"]
            },
            handler=self._get_realtime_data
        )
        
        # Tool 2: Query time-series data
        self.register_tool(
            name="highbyte_query_timeseries",
            description="Query historical time-series data for a tag",
            input_schema={
                "type": "object",
                "properties": {
                    "equipment_id": {"type": "string"},
                    "tag_name": {"type": "string"},
                    "start_time": {
                        "type": "string",
                        "description": "ISO format datetime (e.g., '2024-12-07T10:00:00')"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "ISO format datetime"
                    },
                    "interval_seconds": {
                        "type": "integer",
                        "description": "Data point interval in seconds",
                        "default": 60
                    }
                },
                "required": ["equipment_id", "tag_name", "start_time", "end_time"]
            },
            handler=self._query_timeseries
        )
        
        # Tool 3: Get equipment status
        self.register_tool(
            name="highbyte_get_equipment_status",
            description="Get current status and health of equipment",
            input_schema={
                "type": "object",
                "properties": {
                    "equipment_id": {"type": "string"}
                },
                "required": ["equipment_id"]
            },
            handler=self._get_equipment_status
        )
        
        # Tool 4: List available equipment
        self.register_tool(
            name="highbyte_list_equipment",
            description="List all available equipment and their tags",
            input_schema={
                "type": "object",
                "properties": {}
            },
            handler=self._list_equipment
        )
    
    def _get_realtime_data(self, equipment_id: str, tag_name: str) -> Dict[str, Any]:
        """Simulate real-time tag data"""
        if equipment_id not in self._equipment:
            raise ValueError(f"Unknown equipment: {equipment_id}")
        
        if tag_name not in self._equipment[equipment_id]:
            raise ValueError(f"Unknown tag '{tag_name}' for equipment '{equipment_id}'")
        
        # Generate simulated value based on tag type
        value = self._generate_tag_value(tag_name)
        
        return {
            "equipment_id": equipment_id,
            "tag_name": tag_name,
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "quality": "Good",
            "unit": self._get_tag_unit(tag_name)
        }
    
    def _query_timeseries(
        self,
        equipment_id: str,
        tag_name: str,
        start_time: str,
        end_time: str,
        interval_seconds: int = 60
    ) -> List[Dict[str, Any]]:
        """Simulate time-series historical data"""
        if equipment_id not in self._equipment:
            raise ValueError(f"Unknown equipment: {equipment_id}")
        
        if tag_name not in self._equipment[equipment_id]:
            raise ValueError(f"Unknown tag '{tag_name}' for equipment '{equipment_id}'")
        
        # Parse timestamps
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
        
        # Generate data points
        data_points = []
        current_time = start_dt
        
        while current_time <= end_dt:
            value = self._generate_tag_value(tag_name)
            data_points.append({
                "timestamp": current_time.isoformat(),
                "value": value,
                "quality": "Good"
            })
            current_time += timedelta(seconds=interval_seconds)
        
        return {
            "equipment_id": equipment_id,
            "tag_name": tag_name,
            "start_time": start_time,
            "end_time": end_time,
            "interval_seconds": interval_seconds,
            "data_points": data_points,
            "count": len(data_points)
        }
    
    def _get_equipment_status(self, equipment_id: str) -> Dict[str, Any]:
        """Get equipment status and health"""
        if equipment_id not in self._equipment:
            raise ValueError(f"Unknown equipment: {equipment_id}")
        
        # Simulate status
        statuses = ["Running", "Running", "Running", "Idle", "Maintenance"]
        status = random.choice(statuses)
        
        health_score = random.uniform(75, 100) if status == "Running" else random.uniform(50, 90)
        
        return {
            "equipment_id": equipment_id,
            "status": status,
            "health_score": round(health_score, 2),
            "uptime_hours": round(random.uniform(100, 5000), 2),
            "last_maintenance": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
            "alerts": [] if status == "Running" else ["Minor vibration detected"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _list_equipment(self) -> Dict[str, Any]:
        """List all available equipment"""
        return {
            "equipment": [
                {
                    "id": eq_id,
                    "tags": tags,
                    "tag_count": len(tags)
                }
                for eq_id, tags in self._equipment.items()
            ],
            "total_equipment": len(self._equipment)
        }
    
    def _generate_tag_value(self, tag_name: str) -> float:
        """Generate simulated value for a tag"""
        base_values = {
            "Temperature": (65.0, 85.0),
            "Speed": (1200.0, 2400.0),
            "Vibration": (0.1, 1.5),
            "Load": (20.0, 80.0),
            "Force": (5000.0, 15000.0),
            "CycleCount": (100.0, 1000.0),
            "Status": (0.0, 1.0),
        }
        
        if tag_name in base_values:
            min_val, max_val = base_values[tag_name]
            return round(random.uniform(min_val, max_val), 2)
        
        return round(random.uniform(0.0, 100.0), 2)
    
    def _get_tag_unit(self, tag_name: str) -> str:
        """Get unit for a tag"""
        units = {
            "Temperature": "°F",
            "Speed": "RPM",
            "Vibration": "mm/s",
            "Load": "%",
            "Force": "lbs",
            "CycleCount": "cycles",
            "Status": "boolean",
        }
        return units.get(tag_name, "units")
