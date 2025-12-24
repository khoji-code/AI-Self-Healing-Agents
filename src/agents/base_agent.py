
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import uuid
import time
import asyncio
import json
from datetime import datetime

class BaseAgent(ABC):
    """Base class for all self-healing agents"""
    
    def __init__(self,
                 agent_id: str = None,
                 agent_type: str = "generic",
                 config: Optional[Dict[str, Any]] = None):
        
        self.agent_id = agent_id or f"{agent_type}_{uuid.uuid4().hex[:8]}"
        self.agent_type = agent_type
        self.config = config or {}
        
        self.status = "healthy"  # healthy, degraded, failed, healing
        self.error_count = 0
        self.start_time = time.time()
        self.last_active = time.time()
        
        # Performance tracking
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "average_response_time": 0.0,
            "total_errors": 0
        }
        
        # Memory for self-healing
        self.error_history = []
        self.healing_history = []
        
        print(f"🧠🧠🧠 Agent Created: {self.agent_id} ({self.agent_type})")
    
    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task - to be implemented by child classes"""
        pass
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with error handling and metrics"""
        start_time = time.time()
        self.last_active = time.time()
        self.metrics["total_requests"] += 1
        
        try:
            result = await self.process(task)
            self.metrics["successful_requests"] += 1
            
            # Update response time
            response_time = time.time() - start_time
            current_avg = self.metrics["average_response_time"]
            total_success = self.metrics["successful_requests"]
            self.metrics["average_response_time"] = (
                (current_avg * (total_success - 1) + response_time) / total_success
            )
            
            return {
                "success": True,
                "result": result,
                "agent_id": self.agent_id,
                "response_time": response_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.error_count += 1
            self.metrics["total_errors"] += 1
            error_data = {
                "error": str(e),
                "task": task,
                "timestamp": datetime.now().isoformat(),
                "agent_status": self.status
            }
            self.error_history.append(error_data)
            
            # Auto-update status based on errors
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
    
    async def heal(self, diagnosis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Self-heal the agent"""
        self.status = "healing"
        
        healing_action = {
            "action": "reset",
            "timestamp": datetime.now().isoformat(),
            "old_error_count": self.error_count,
            "diagnosis": diagnosis or {"reason": "preventive_healing"}
        }
        
        # Reset error count
        self.error_count = 0
        self.status = "healthy"
        self.healing_history.append(healing_action)
        
        return {
            "success": True,
            "healing_action": healing_action,
            "new_status": self.status,
            "agent_id": self.agent_id
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
            "last_active": datetime.fromtimestamp(self.last_active).isoformat(),
            "needs_healing": self.error_count > 3
        }
    
    async def check_health(self) -> Dict[str, Any]:
        """Health check"""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "healthy": self.status == "healthy",
            "error_count": self.error_count,
            "last_check": datetime.now().isoformat()
        }