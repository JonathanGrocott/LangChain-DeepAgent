"""Mock SQL Server Transactional Database MCP Server

Simulates transactional queries for work orders, inventory, and maintenance tickets.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import random
from .base_server import BaseMCPServer


class SQLServerMockServer(BaseMCPServer):
    """
    Mock SQL Server providing simulated transactional database.
    
    Simulates:
    - Work order management
    - Inventory tracking
    - Maintenance ticket creation
    """
    
    def __init__(self):
        super().__init__(
            server_name="sqlserver-mock",
            description="Mock SQL Server for transactional data"
        )
        
        # In-memory "database" for demonstration
        self._work_orders = []
        self._maintenance_tickets = []
        self._next_ticket_id = 1000
    
    def _register_tools(self) -> None:
        """Register SQL Server-specific tools"""
        
        # Tool 1: Query work orders
        self.register_tool(
            name="sqlserver_query_work_orders",
            description="Query work orders with optional filters",
            input_schema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status (open, in_progress, completed, all)",
                        "default": "all"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Filter by priority (low, medium, high, critical)",
                        "default": None
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 50
                    }
                },
                "required": []
            },
            handler=self._query_work_orders
        )
        
        # Tool 2: Get inventory levels
        self.register_tool(
            name="sqlserver_get_inventory_levels",
            description="Get current inventory levels for parts and materials",
            input_schema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Warehouse location",
                        "default": None
                    },
                    "low_stock_only": {
                        "type": "boolean",
                        "description": "Only return items with low stock",
                        "default": False
                    }
                },
                "required": []
            },
            handler=self._get_inventory_levels
        )
        
        # Tool 3: Create maintenance ticket
        self.register_tool(
            name="sqlserver_create_maintenance_ticket",
            description="Create a new maintenance ticket for equipment",
            input_schema={
                "type": "object",
                "properties": {
                    "equipment_id": {
                        "type": "string",
                        "description": "Equipment identifier"
                    },
                    "description": {
                        "type": "string",
                        "description": "Issue description"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Priority level (low, medium, high, critical)",
                        "default": "medium"
                    }
                },
                "required": ["equipment_id", "description"]
            },
            handler=self._create_maintenance_ticket
        )
        
        # Tool 4: Get maintenance history
        self.register_tool(
            name="sqlserver_get_maintenance_history",
            description="Get maintenance history for equipment",
            input_schema={
                "type": "object",
                "properties": {
                    "equipment_id": {
                        "type": "string",
                        "description": "Equipment identifier"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to look back",
                        "default": 90
                    }
                },
                "required": ["equipment_id"]
            },
            handler=self._get_maintenance_history
        )
    
    def _query_work_orders(
        self,
        status: str = "all",
        priority: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """Query work orders"""
        # Generate simulated work orders
        work_orders = []
        statuses = ["open", "in_progress", "completed"]
        priorities = ["low", "medium", "high", "critical"]
        
        for i in range(min(limit, 20)):
            wo_status = random.choice(statuses)
            wo_priority = random.choice(priorities)
            
            # Apply filters
            if status != "all" and wo_status != status:
                continue
            if priority and wo_priority != priority:
                continue
            
            work_order = {
                "id": f"WO-{10000 + i}",
                "equipment_id": random.choice([
                    "CNC-Machine-1", "CNC-Machine-2", "Press-1", "Conveyor-A"
                ]),
                "description": random.choice([
                    "Routine maintenance",
                    "Tool replacement",
                    "Calibration check",
                    "Software update",
                    "Belt replacement"
                ]),
                "status": wo_status,
                "priority": wo_priority,
                "created_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "assigned_to": random.choice(["Tech-A", "Tech-B", "Tech-C", None]),
                "estimated_hours": random.randint(1, 8)
            }
            work_orders.append(work_order)
        
        return {
            "work_orders": work_orders,
            "count": len(work_orders),
            "filters": {
                "status": status,
                "priority": priority
            }
        }
    
    def _get_inventory_levels(
        self,
        location: Optional[str] = None,
        low_stock_only: bool = False
    ) -> Dict[str, Any]:
        """Get inventory levels"""
        locations = [location] if location else ["Warehouse-A", "Warehouse-B"]
        
        inventory_items = []
        parts = [
            ("Bearing-6205", 50, 20),
            ("Belt-V-100", 30, 10),
            ("Filter-Air-Standard", 100, 25),
            ("Lubricant-5W30", 200, 50),
            ("Seal-O-Ring-25mm", 500, 100),
            ("Sensor-Temp-K-Type", 40, 15),
        ]
        
        for loc in locations:
            for part_num, reorder_qty, min_qty in parts:
                current_qty = random.randint(0, reorder_qty * 2)
                is_low_stock = current_qty <= min_qty
                
                if low_stock_only and not is_low_stock:
                    continue
                
                inventory_items.append({
                    "part_number": part_num,
                    "location": loc,
                    "quantity_on_hand": current_qty,
                    "minimum_quantity": min_qty,
                    "reorder_quantity": reorder_qty,
                    "low_stock": is_low_stock,
                    "unit_cost": round(random.uniform(5.0, 500.0), 2),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return {
            "inventory_items": inventory_items,
            "count": len(inventory_items),
            "low_stock_count": sum(1 for item in inventory_items if item["low_stock"]),
            "locations": locations
        }
    
    def _create_maintenance_ticket(
        self,
        equipment_id: str,
        description: str,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """Create maintenance ticket"""
        ticket_id = f"MT-{self._next_ticket_id}"
        self._next_ticket_id += 1
        
        ticket = {
            "ticket_id": ticket_id,
            "equipment_id": equipment_id,
            "description": description,
            "priority": priority,
            "status": "open",
            "created_date": datetime.now().isoformat(),
            "created_by": "system",
            "assigned_to": None,
            "estimated_resolution": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        self._maintenance_tickets.append(ticket)
        
        return {
            "success": True,
            "ticket": ticket,
            "message": f"Maintenance ticket {ticket_id} created successfully"
        }
    
    def _get_maintenance_history(
        self,
        equipment_id: str,
        days: int = 90
    ) -> Dict[str, Any]:
        """Get maintenance history for equipment"""
        # Generate simulated history
        history = []
        num_events = random.randint(3, 10)
        
        for i in range(num_events):
            event_date = datetime.now() - timedelta(days=random.randint(1, days))
            
            history.append({
                "ticket_id": f"MT-{random.randint(1000, 9999)}",
                "equipment_id": equipment_id,
                "date": event_date.strftime("%Y-%m-%d"),
                "type": random.choice([
                    "Preventive Maintenance",
                    "Corrective Maintenance",
                    "Inspection",
                    "Repair",
                    "Calibration"
                ]),
                "description": random.choice([
                    "Routine lubrication",
                    "Replaced worn bearings",
                    "Calibrated sensors",
                    "Software update",
                    "Belt tension adjustment"
                ]),
                "technician": random.choice(["Tech-A", "Tech-B", "Tech-C"]),
                "hours_spent": random.randint(1, 6),
                "parts_used": random.randint(0, 5),
                "cost": round(random.uniform(50, 500), 2)
            })
        
        # Sort by date descending
        history.sort(key=lambda x: x["date"], reverse=True)
        
        return {
            "equipment_id": equipment_id,
            "history": history,
            "count": len(history),
            "date_range_days": days,
            "total_maintenance_cost": sum(h["cost"] for h in history),
            "total_hours": sum(h["hours_spent"] for h in history)
        }
