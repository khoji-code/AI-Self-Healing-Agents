"""
Baseline Agent WITHOUT Self-Healing Capability
"""
from typing import Dict, Any, Optional
import asyncio
import time
from datetime import datetime
import uuid

class BaselineAgent:
    """Agent without self-healing capabilities - for comparison"""
    
    def __init__(self,
                 agent_id: str = None,
                 agent_type: str = "baseline"):
        
        self.agent_id = agent_id or f"baseline_{uuid.uuid4().hex[:8]}"
        self.agent_type = agent_type
        
        # Basic tracking (no healing)
        self.status = "healthy"
        self.error_count = 0
        self.start_time = time.time()
        
        # Performance tracking
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_errors": 0
        }
        
        print(f"📊 Baseline Agent Created: {self.agent_id}")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process task - to be implemented by child classes"""
        raise NotImplementedError("Child classes must implement process()")
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute without healing capabilities"""
        start_time = time.time()
        self.metrics["total_requests"] += 1
        
        try:
            result = await self.process(task)
            self.metrics["successful_requests"] += 1
            
            return {
                "success": True,
                "result": result,
                "agent_id": self.agent_id,
                "response_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.error_count += 1
            self.metrics["failed_requests"] += 1
            self.metrics["total_errors"] += 1
            
            # No healing - just increment errors
            if self.error_count > 10:
                self.status = "failed"
            elif self.error_count > 3:
                self.status = "degraded"
            
            return {
                "success": False,
                "error": str(e),
                "agent_id": self.agent_id,
                "error_count": self.error_count,
                "status": self.status,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics"""
        uptime = time.time() - self.start_time
        
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status,
            "uptime_seconds": uptime,
            "error_count": self.error_count,
            "metrics": self.metrics,
            "requires_restart": self.error_count > 5
        }