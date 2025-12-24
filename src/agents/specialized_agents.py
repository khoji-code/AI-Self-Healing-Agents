
from typing import Dict, Any, Optional
import asyncio
import random
import time
from datetime import datetime
from .base_agent import BaseAgent

class DataProcessorAgent(BaseAgent):
    """Data processing agent with self-healing capabilities"""
    
    def __init__(self, agent_id: str = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id or "data_processor", "data_processor", config)
        self.data_cache = {}
        self.processed_count = 0
        
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process data with error simulation"""
        
        operation = task.get("operation", "process")
        data = task.get("data", {})
        
        # Simulate occasional failure (for healing demonstration)
        if random.random() < 0.15:  # 15% chance of failure
            raise Exception(f"Data processing failed: Simulated error in {operation}")
        
        await asyncio.sleep(0.1)  # Simulate processing time
        
        if operation == "transform":
            result = self._transform_data(data)
        elif operation == "validate":
            result = self._validate_data(data)
        elif operation == "analyze":
            result = self._analyze_data(data)
        elif operation == "clean":
            result = self._clean_data(data)
        else:
            result = {"error": f"Unknown operation: {operation}"}
        
        self.processed_count += 1
        
        return {
            "operation": operation,
            "result": result,
            "processed_by": self.agent_id,
            "total_processed": self.processed_count
        }
    
    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: str(v).upper() if isinstance(v, str) else v for k, v in data.items()}
    
    def _validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        required = ["id", "timestamp"]
        missing = [f for f in required if f not in data]
        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "data_type": type(data).__name__
        }
    
    def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(data, dict):
            return {
                "field_count": len(data),
                "value_types": {k: type(v).__name__ for k, v in data.items()},
                "has_nested": any(isinstance(v, (dict, list)) for v in data.values())
            }
        return {"error": "Invalid data format"}
    
    def _clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Simple cleaning: remove null values
        return {k: v for k, v in data.items() if v is not None}

class APIGatewayAgent(BaseAgent):
    """API Gateway agent with rate limiting and error handling"""
    
    def __init__(self, agent_id: str = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id or "api_gateway", "api_gateway", config)
        self.request_count = 0
        self.rate_limits = {}
        
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process API requests"""
        
        endpoint = task.get("endpoint", "/")
        method = task.get("method", "GET")
        payload = task.get("payload", {})
        
        self.request_count += 1
        
        # Check rate limiting
        client_id = task.get("client_id", "default")
        if client_id in self.rate_limits:
            if self.rate_limits[client_id] > 10:  # 10 requests limit
                raise Exception(f"Rate limit exceeded for client: {client_id}")
            self.rate_limits[client_id] += 1
        else:
            self.rate_limits[client_id] = 1
        
        # Simulate processing
        await asyncio.sleep(0.05)
        
        # Simulate occasional timeout
        if random.random() < 0.08:  # 8% chance of timeout
            raise Exception("API Gateway timeout: Backend service unavailable")
        
        return {
            "endpoint": endpoint,
            "method": method,
            "status": "success",
            "request_id": f"req_{self.request_count:06d}",
            "client_id": client_id,
            "response": {
                "message": f"Processed {method} {endpoint}",
                "timestamp": datetime.now().isoformat(),
                "data": payload if method == "POST" else None
            }
        }

class AnalyticsAgent(BaseAgent):
    """Analytics and monitoring agent"""
    
    def __init__(self, agent_id: str = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id or "analytics", "analytics", config)
        self.metrics_history = []
        
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analytics and reports"""
        
        report_type = task.get("report_type", "summary")
        metrics = task.get("metrics", {})
        timeframe = task.get("timeframe", "recent")
        
        if report_type == "summary":
            result = self._generate_summary(metrics)
        elif report_type == "trend":
            result = self._analyze_trends(metrics)
        elif report_type == "anomaly":
            result = self._detect_anomalies(metrics)
        elif report_type == "forecast":
            result = self._generate_forecast(metrics)
        else:
            result = {"error": f"Unknown report type: {report_type}"}
        
        # Store in history
        self.metrics_history.append({
            "report_type": report_type,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "report_type": report_type,
            "report": result,
            "generated_by": self.agent_id,
            "timeframe": timeframe
        }
    
    def _generate_summary(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        # Check if metrics values are numeric
        numeric_values = []
        for value in metrics.values():
            if isinstance(value, (int, float)):
                numeric_values.append(value)
            elif isinstance(value, list):
                # If it's a list, sum the list
                numeric_values.append(sum(v for v in value if isinstance(v, (int, float))))
        
        total = sum(numeric_values) if numeric_values else 0
        count = len(numeric_values)
        
        return {
            "total": total,
            "average": total / count if count > 0 else 0,
            "count": count,
            "max": max(numeric_values) if numeric_values else 0,
            "min": min(numeric_values) if numeric_values else 0,
            "timestamp": datetime.now().isoformat(),
            "note": f"Processed {count} numeric values from {len(metrics)} metrics"
        }
    
    def _analyze_trends(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        values = list(metrics.values()) if metrics else []
        
        if len(values) > 1:
            trend = "increasing" if values[-1] > values[0] else "decreasing"
            change_pct = ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0
        else:
            trend = "stable"
            change_pct = 0
        
        return {
            "trend": trend,
            "change_percentage": change_pct,
            "data_points": len(values),
            "volatility": np.std(values) if len(values) > 1 else 0
        }
    
    def _detect_anomalies(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        values = list(metrics.values()) if metrics else []
        
        if len(values) > 2:
            mean = np.mean(values)
            std = np.std(values)
            anomalies = [v for v in values if abs(v - mean) > 2 * std]
        else:
            anomalies = []
        
        return {
            "anomalies_detected": len(anomalies),
            "anomaly_values": anomalies,
            "threshold": "2 standard deviations"
        }
    
    def _generate_forecast(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        values = list(metrics.values()) if metrics else []
        
        if len(values) > 3:
            # Simple linear forecast
            x = np.arange(len(values))
            coef = np.polyfit(x, values, 1)
            next_value = coef[0] * len(values) + coef[1]
        else:
            next_value = values[-1] if values else 0
        
        return {
            "next_period_forecast": next_value,
            "confidence": "medium" if len(values) > 5 else "low",
            "based_on_points": len(values)
        }