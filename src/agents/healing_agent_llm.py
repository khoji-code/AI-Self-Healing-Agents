"""
Healing Agent with LLM-Agnostic Architecture
"""
from typing import Dict, Any, Optional
import asyncio
import json
from datetime import datetime
import time
from .base_agent import BaseAgent
from ..api.llm_provider import LLMFactory, LLMConfig

class LLMHealingAgent(BaseAgent):
    """AI-powered healing agent with LLM abstraction"""
    
    def __init__(self,
                 agent_id: str = "master_healer",
                 config: Optional[Dict[str, Any]] = None,
                 llm_config: Optional[LLMConfig] = None):
        
        super().__init__(agent_id, "healer", config)
        
        # Initialize LLM
        if llm_config:
            self.llm = LLMFactory.create_client(llm_config)
        else:
            self.llm = LLMFactory.from_env()
        
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
        
        print(f"⚕️  LLM Healing Agent Activated: {self.agent_id}")
        print(f"🤖 Using LLM: {self.llm.__class__.__name__}")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process healing requests with LLM abstraction"""
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
        """Heal a specific agent using LLM"""
        target_agent = task.get("target_agent")
        issue_description = task.get("issue", "Unknown issue")
        
        print(f"🔧 Healing {target_agent} - Issue: {issue_description}")
        
        # Use LLM for diagnosis
        diagnosis = await self._llm_diagnose(issue_description, task.get("metrics", {}))
        
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
            "llm_used": self.llm.__class__.__name__,
            "timestamp": datetime.now().isoformat()
        }
        
        self.healing_operations.append(operation)
        
        return {
            "success": True,
            "operation": operation,
            "message": f"Healing completed for {target_agent}"
        }
    
    async def _llm_diagnose(self,
                           issue: str,
                           metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Use abstracted LLM to diagnose issues"""
        
        prompt = f"""
        DIAGNOSE SYSTEM ISSUE
        
        Issue: {issue}
        Metrics: {json.dumps(metrics, indent=2)}
        
        Provide:
        1. Root cause analysis
        2. Severity level
        3. Recommended actions
        
        Return as JSON.
        """
        
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are an expert system diagnostician.",
                max_tokens=300
            )
            
            try:
                return json.loads(response)
            except:
                return {"analysis": response, "parsed": False}
                
        except Exception as e:
            return {
                "error": f"LLM diagnosis failed: {str(e)}",
                "fallback_diagnosis": {
                    "root_cause": "Unknown - requires investigation",
                    "severity": "High"
                }
            }
    
    async def _generate_healing_plan(self,
                                   diagnosis: Dict[str, Any],
                                   target_agent: str) -> Dict[str, Any]:
        """Generate healing plan using LLM"""
        
        prompt = f"""
        CREATE HEALING PLAN
        
        For Agent: {target_agent}
        Diagnosis: {json.dumps(diagnosis, indent=2)}
        
        Create a step-by-step healing plan.
        """
        
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are a senior SRE creating healing procedures.",
                max_tokens=400
            )
            
            return {
                "plan": response,
                "generated_by": self.llm.__class__.__name__,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "fallback_plan": {
                    "steps": ["Restart agent", "Verify configuration", "Check dependencies"],
                    "error": str(e)
                }
            }
    
    async def _execute_healing(self,
                             plan: Dict[str, Any],
                             target_agent: str) -> Dict[str, Any]:
        """Execute healing plan"""
        await asyncio.sleep(0.5)  # Simulate healing
        
        return {
            "executed": True,
            "target_agent": target_agent,
            "plan_applied": True,
            "simulation": True
        }
    
    async def generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code using LLM"""
        requirements = task.get("requirements", "")
        language = task.get("language", "python")
        
        prompt = f"""
        Generate {language} code with these requirements:
        {requirements}
        
        Return only the code.
        """
        
        try:
            code = await self.llm.generate(
                prompt=prompt,
                system_prompt=f"You are a senior {language} developer.",
                max_tokens=1000
            )
            
            return {
                "success": True,
                "code": code,
                "language": language,
                "llm_used": self.llm.__class__.__name__
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Code generation failed: {str(e)}"
            }