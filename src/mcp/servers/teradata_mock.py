"""Mock Teradata Analytics Database MCP Server

Simulates analytical queries for production metrics and quality trends.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List
import random
from .base_server import BaseMCPServer


class TeradataMockServer(BaseMCPServer):
    """
    Mock Teradata server providing simulated analytics database.
    
    Simulates:
    - Production metrics aggregation
    - Quality trend analysis
    - SQL query execution
    """
    
    def __init__(self):
        super().__init__(
            server_name="teradata-mock",
            description="Mock Teradata Analytics Database for production metrics"
        )
    
    def _register_tools(self) -> None:
        """Register Teradata-specific tools"""
        
        # Tool 1: Execute analytical query
        self.register_tool(
            name="teradata_execute_query",
            description="Execute an analytical SQL query",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of rows to return",
                        "default": 100
                    }
                },
                "required": ["query"]
            },
            handler=self._execute_query
        )
        
        # Tool 2: Get production metrics
        self.register_tool(
            name="teradata_get_production_metrics",
            description="Get aggregated production metrics for a date range",
            input_schema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD)"
                    },
                    "product_line": {
                        "type": "string",
                        "description": "Optional product line filter",
                        "default": None
                    }
                },
                "required": ["start_date", "end_date"]
            },
            handler=self._get_production_metrics
        )
        
        # Tool 3: Analyze quality trends
        self.register_tool(
            name="teradata_analyze_quality_trends",
            description="Analyze quality metrics and trends over time",
            input_schema={
                "type": "object",
                "properties": {
                    "product_line": {
                        "type": "string",
                        "description": "Product line to analyze"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to analyze",
                        "default": 30
                    }
                },
                "required": ["product_line"]
            },
            handler=self._analyze_quality_trends
        )
    
    def _execute_query(self, query: str, limit: int = 100) -> Dict[str, Any]:
        """Simulate SQL query execution"""
        # Simple query simulation - in reality would parse and execute
        query_lower = query.lower()
        
        if "production" in query_lower or "output" in query_lower:
            columns = ["date", "product_line", "units_produced", "target_units", "efficiency"]
            rows = self._generate_production_rows(limit)
        elif "quality" in query_lower or "defect" in query_lower:
            columns = ["date", "product_line", "total_units", "defects", "defect_rate"]
            rows = self._generate_quality_rows(limit)
        else:
            columns = ["id", "value", "timestamp"]
            rows = [[i, random.randint(0, 1000), datetime.now().isoformat()] for i in range(min(limit, 10))]
        
        return {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "execution_time_ms": random.randint(50, 500)
        }
    
    def _get_production_metrics(
        self,
        start_date: str,
        end_date: str,
        product_line: str = None
    ) -> Dict[str, Any]:
        """Get aggregated production metrics"""
        # Parse dates
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end_dt - start_dt).days + 1
        
        product_lines = [product_line] if product_line else ["Line-A", "Line-B", "Line-C"]
        
        metrics = []
        for pl in product_lines:
            total_units = random.randint(10000, 50000) * days
            target_units = total_units + random.randint(-5000, 5000)
            efficiency = (total_units / target_units * 100) if target_units > 0 else 0
            
            metrics.append({
                "product_line": pl,
                "total_units_produced": total_units,
                "target_units": target_units,
                "efficiency_percent": round(efficiency, 2),
                "average_daily_output": round(total_units / days, 2),
                "downtime_hours": round(random.uniform(5, 50), 2),
                "oee": round(random.uniform(75, 95), 2)  # Overall Equipment Effectiveness
            })
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
            "product_lines": metrics,
            "total_production": sum(m["total_units_produced"] for m in metrics)
        }
    
    def _analyze_quality_trends(self, product_line: str, days: int = 30) -> Dict[str, Any]:
        """Analyze quality trends"""
        # Generate daily quality data
        daily_data = []
        current_date = datetime.now() - timedelta(days=days)
        
        base_defect_rate = random.uniform(0.5, 2.5)
        
        for i in range(days):
            defect_rate = base_defect_rate + random.uniform(-0.5, 0.5)
            defect_rate = max(0.1, defect_rate)  # Keep positive
            
            total_units = random.randint(800, 1500)
            defects = int(total_units * (defect_rate / 100))
            
            daily_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "total_units": total_units,
                "defects": defects,
                "defect_rate_percent": round(defect_rate, 2)
            })
            
            current_date += timedelta(days=1)
        
        avg_defect_rate = sum(d["defect_rate_percent"] for d in daily_data) / len(daily_data)
        
        # Trend analysis
        recent_avg = sum(d["defect_rate_percent"] for d in daily_data[-7:]) / 7
        trend = "improving" if recent_avg < avg_defect_rate else "worsening"
        
        return {
            "product_line": product_line,
            "analysis_period_days": days,
            "daily_data": daily_data,
            "average_defect_rate": round(avg_defect_rate, 2),
            "recent_7day_average": round(recent_avg, 2),
            "trend": trend,
            "total_defects": sum(d["defects"] for d in daily_data),
            "total_units": sum(d["total_units"] for d in daily_data)
        }
    
    def _generate_production_rows(self, limit: int) -> List[List[Any]]:
        """Generate simulated production data rows"""
        rows = []
        current_date = datetime.now()
        
        for i in range(min(limit, 30)):
            date_str = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            product_line = random.choice(["Line-A", "Line-B", "Line-C"])
            units = random.randint(800, 1500)
            target = random.randint(900, 1400)
            efficiency = round((units / target * 100) if target > 0 else 0, 2)
            
            rows.append([date_str, product_line, units, target, efficiency])
        
        return rows
    
    def _generate_quality_rows(self, limit: int) -> List[List[Any]]:
        """Generate simulated quality data rows"""
        rows = []
        current_date = datetime.now()
        
        for i in range(min(limit, 30)):
            date_str = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            product_line = random.choice(["Line-A", "Line-B", "Line-C"])
            total = random.randint(800, 1500)
            defects = random.randint(5, 30)
            defect_rate = round((defects / total * 100), 2)
            
            rows.append([date_str, product_line, total, defects, defect_rate])
        
        return rows
