
from typing import Dict, Any, Optional, List
import asyncio
import json
from datetime import datetime
from .base_agent import BaseAgent
from ..api.qwen_client import QwenClient
import time

class HealingAgent(BaseAgent):
    """AI-powered healing agent for the multi-agent system"""
    
    def __init__(self,
                 agent_id: str = "master_healer",
                 config: Optional[Dict[str, Any]] = None):
        
        super().__init__(agent_id, "healer", config)
        
        # Initialize Qwen AI
        self.qwen = QwenClient()
        
        # Healing expertise database
        self.expertise = {
            "common_issues": [
                "API connection failures",
                "Memory leaks",
                "Database timeouts",
                "Network latency",
                "Authentication errors",
                "Rate limiting",
                "Data corruption",
                "Configuration errors"
            ],
            "healing_strategies": {
                "immediate": ["Restart", "Circuit breaker", "Fallback", "Retry with backoff"],
                "diagnostic": ["Log analysis", "Metrics review", "Dependency check", "Resource monitoring"],
                "preventive": ["Auto-scaling", "Health checks", "Circuit breaking", "Rate limiting"]
            }
        }
        
        # Track healing operations
        self.healing_operations = []
        
        print(f"⚕️  Healing Agent Activated: {self.agent_id}")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process healing requests"""
        request_type = task.get("type", "heal_agent")
        
        if request_type == "heal_agent":
            return await self.heal_agent(task)
        elif request_type == "diagnose_system":
            return await self.diagnose_system(task)
        elif request_type == "preventive_check":
            return await self.preventive_check(task)
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    async def heal_agent(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Heal a specific agent"""
        target_agent = task.get("target_agent")
        issue_description = task.get("issue", "Unknown issue")
        agent_metrics = task.get("metrics", {})
        
        print(f"🔧 Healing Agent {target_agent} - Issue: {issue_description}")
        
        # Step 1: Diagnose with Qwen
        diagnosis = await self._ai_diagnose(issue_description, agent_metrics)
        
        # Step 2: Generate healing plan
        healing_plan = await self._generate_healing_plan(diagnosis, target_agent)
        
        # Step 3: Execute healing (simulated - in real system would communicate with agent)
        healing_result = await self._execute_healing(healing_plan, target_agent)
        
        # Record the operation
        operation = {
            "operation_id": f"heal_{int(time.time())}",
            "target_agent": target_agent,
            "issue": issue_description,
            "diagnosis": diagnosis,
            "healing_plan": healing_plan,
            "result": healing_result,
            "timestamp": datetime.now().isoformat(),
            "healer_id": self.agent_id
        }
        
        self.healing_operations.append(operation)
        
        return {
            "success": True,
            "operation": operation,
            "message": f"Healing initiated for {target_agent}"
        }
    
    async def _ai_diagnose(self,
                          issue: str,
                          metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Use Qwen AI to diagnose issues"""
        
        prompt = f"""
        DIAGNOSE SYSTEM ISSUE
        
        Issue Description: {issue}
        
        Agent Metrics:
        {json.dumps(metrics, indent=2)}
        
        Analyze and provide:
        1. Root cause analysis
        2. Severity level (Critical/High/Medium/Low)
        3. Immediate impact
        4. Recommended diagnostic steps
        
        Return as structured JSON.
        """
        
        try:
            response = await self.qwen.generate(
                prompt=prompt,
                system_prompt="You are an expert system diagnostician with 20 years of experience.",
                max_tokens=400
            )
            
            # Parse the response
            try:
                diagnosis = json.loads(response)
            except:
                diagnosis = {"ai_analysis": response, "parsed": False}
            
            return diagnosis
            
        except Exception as e:
            return {
                "error": f"AI diagnosis failed: {str(e)}",
                "fallback_diagnosis": {
                    "root_cause": "Unknown - requires manual investigation",
                    "severity": "High",
                    "immediate_actions": ["Check logs", "Restart service", "Verify dependencies"]
                }
            }
    
    async def _generate_healing_plan(self,
                                   diagnosis: Dict[str, Any],
                                   target_agent: str) -> Dict[str, Any]:
        """Generate AI-powered healing plan"""
        
        prompt = f"""
        CREATE HEALING PLAN
        
        For Agent: {target_agent}
        
        Diagnosis:
        {json.dumps(diagnosis, indent=2)}
        
        Create a detailed healing plan with:
        1. Step-by-step procedure
        2. Expected timeline
        3. Success criteria
        4. Rollback procedure
        5. Verification steps
        
        Be specific and actionable.
        """
        
        try:
            response = await self.qwen.generate(
                prompt=prompt,
                system_prompt="You are a senior SRE creating production healing procedures.",
                max_tokens=500
            )
            
            return {
                "plan": response,
                "generated_by": "qwen_ai",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "fallback_plan": {
                    "steps": ["Restart the agent", "Clear cache", "Verify configuration"],
                    "rollback": "Restore from last known good state"
                },
                "error": str(e)
            }
    
    async def _execute_healing(self,
                             plan: Dict[str, Any],
                             target_agent: str) -> Dict[str, Any]:
        """Execute healing plan (simulated)"""
        
        # In a real system, this would communicate with the target agent
        # For now, we simulate the healing
        
        await asyncio.sleep(1)  # Simulate healing time
        
        return {
        "executed": True,
        "target_agent": target_agent,
        "execution_time": 1.0,
        "status": "healing_applied",
        "simulation": True,
        "message": f"Healing plan executed for {target_agent}",
        "timestamp": time.time()
        }
    
    async def diagnose_system(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """System-wide diagnosis"""
        
        system_metrics = task.get("system_metrics", {})
        agents_status = task.get("agents_status", [])
        
        prompt = f"""
        SYSTEM-WIDE DIAGNOSIS
        
        System Metrics:
        {json.dumps(system_metrics, indent=2)}
        
        Agents Status:
        {json.dumps(agents_status, indent=2)}
        
        Analyze overall system health and identify:
        1. Critical issues
        2. Performance bottlenecks  
        3. Resource constraints
        4. Recommendations
        
        Provide actionable insights.
        """
        
        try:
            analysis = await self.qwen.generate(
                prompt=prompt,
                system_prompt="You are a system architect analyzing distributed systems.",
                max_tokens=600
            )
            
            return {
                "system_analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "analyzed_agents": len(agents_status)
            }
            
        except Exception as e:
            return {"error": f"System diagnosis failed: {str(e)}"}
    
    async def preventive_check(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Preventive health check"""
        
        agents = task.get("agents", [])
        
        recommendations = []
        
        for agent in agents:
            if agent.get("error_count", 0) > 2:
                rec = await self._generate_preventive_recommendation(agent)
                recommendations.append(rec)
        
        return {
            "preventive_check": True,
            "agents_checked": len(agents),
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_preventive_recommendation(self,
                                                agent: Dict[str, Any]) -> Dict[str, Any]:
        """Generate preventive recommendation"""
        
        prompt = f"""
        PREVENTIVE RECOMMENDATION
        
        Agent: {agent.get('agent_id', 'Unknown')}
        Error Count: {agent.get('error_count', 0)}
        Status: {agent.get('status', 'unknown')}
        
        Suggest preventive measures to avoid future failures.
        """
        
        try:
            recommendation = await self.qwen.generate(
                prompt=prompt,
                max_tokens=200
            )
            
            return {
                "agent_id": agent.get('agent_id'),
                "recommendation": recommendation,
                "priority": "medium" if agent.get('error_count', 0) > 3 else "low"
            }
            
        except Exception as e:
            return {
                "agent_id": agent.get('agent_id'),
                "recommendation": "Monitor closely and implement circuit breaker",
                "fallback": True
            }
    
    def get_healing_stats(self) -> Dict[str, Any]:
        """Get healing statistics"""
        return {
            "total_operations": len(self.healing_operations),
            "successful_healings": len([op for op in self.healing_operations 
                                       if op.get("result", {}).get("executed", False)]),
            "recent_operations": self.healing_operations[-5:] if self.healing_operations else [],
            "expertise_areas": list(self.expertise["common_issues"])
        }
