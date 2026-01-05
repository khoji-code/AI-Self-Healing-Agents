"""
Working Healing Agent using fixed Qwen client
"""
from typing import Dict, Any, Optional
import asyncio
import json
from datetime import datetime
import time
from .base_agent import BaseAgent
from ..api.working_qwen_client import WorkingQwenClient, QwenConfig

class WorkingHealingAgent(BaseAgent):
    """AI-powered healing agent with working Qwen client"""
    
    def __init__(self,
                 agent_id: str = "master_healer",
                 config: Optional[Dict[str, Any]] = None,
                 qwen_config: Optional[QwenConfig] = None):
        
        super().__init__(agent_id, "healer", config)
        
        # Initialize working Qwen client
        self.qwen = WorkingQwenClient(qwen_config)
        
        # Healing expertise
        self.expertise = {
            "common_issues": [
                "API connection failures",
                "Memory leaks",
                "Database timeouts",
                "Network latency",
                "Authentication errors"
            ]
        }
        
        # Track healing operations
        self.healing_operations = []
        
        print(f"⚕️  Working Healing Agent Activated: {self.agent_id}")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process healing requests"""
        request_type = task.get("type", "heal_agent")
        
        if request_type == "heal_agent":
            return await self.heal_agent(task)
        elif request_type == "diagnose_system":
            return await self.diagnose_system(task)
        elif request_type == "generate_code":
            return await self.generate_code(task)
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    async def heal_agent(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Heal a specific agent"""
        target_agent = task.get("target_agent")
        issue_description = task.get("issue", "Unknown issue")
        
        print(f"🔧 Healing {target_agent} - Issue: {issue_description}")
        
        # Use Qwen for diagnosis
        diagnosis = await self._ai_diagnose(issue_description, task.get("metrics", {}))
        
        # Generate healing plan
        healing_plan = await self._generate_healing_plan(diagnosis, target_agent)
        
        # Execute healing
        healing_result = await self._execute_healing(healing_plan, target_agent)
        
        # Record operation
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
            "message": f"Healing completed for {target_agent}"
        }
    
    async def _ai_diagnose(self,
                          issue: str,
                          metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Use Qwen to diagnose issues"""
        
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
    
    async def generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code using Qwen"""
        requirements = task.get("requirements", "")
        language = task.get("language", "python")
        
        prompt = f"""
        Generate {language} code with these requirements:
        {requirements}
        
        Return only the code.
        """
        
        try:
            code = await self.qwen.generate(
                prompt=prompt,
                system_prompt=f"You are a senior {language} developer.",
                max_tokens=1000
            )
            
            return {
                "success": True,
                "code": code,
                "language": language
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Code generation failed: {str(e)}"
            }