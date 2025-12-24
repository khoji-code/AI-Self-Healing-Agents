
from typing import Dict, Any, List, TypedDict, Optional
import asyncio
import time
from langgraph.graph import StateGraph, END

from ..agents.base_agent import BaseAgent
from ..agents.healing_agent import HealingAgent

class SystemState(TypedDict):
    agents: List[BaseAgent]
    healing_agent: HealingAgent
    task: Dict[str, Any]
    results: Dict[str, Any]
    errors: Dict[str, Any]
    step: str

class SimpleHealingGraph:
    """Simple healing graph without complex dependencies"""
    
    def __init__(self):
        self.graph = StateGraph(SystemState)
        self.graph.add_node("process", self.process_tasks)
        self.graph.add_node("heal", self.heal_agents)
        self.graph.set_entry_point("process")
        
        def route(state):
            return "heal" if state.get("errors") else END
        
        self.graph.add_conditional_edges("process", route, {"heal": "heal", END: END})
        self.graph.add_edge("heal", END)
        self.app = self.graph.compile()
    
    async def process_tasks(self, state: SystemState):
        """Process tasks with agents"""
        task = state["task"]
        agents = state["agents"]
        results = {}
        errors = {}
        
        for agent in agents:
            try:
                result = await agent.execute(task)
                results[agent.agent_id] = result
            except Exception as e:
                errors[agent.agent_id] = str(e)
        
        return {"results": results, "errors": errors, "step": "processed"}
    
    async def heal_agents(self, state: SystemState):
        """Heal agents with errors"""
        healing_agent = state["healing_agent"]
        errors = state.get("errors", {})
        
        healing_results = {}
        for agent_id in errors:
            healing_task = {
                "type": "heal_agent",
                "target_agent": agent_id,
                "issue": errors[agent_id]
            }
            try:
                result = await healing_agent.process(healing_task)
                healing_results[agent_id] = result
            except:
                pass
        
        return {"healing_results": healing_results, "step": "healed"}
    
    async def run(self, agents, healing_agent, task):
        """Run the graph"""
        initial_state = SystemState(
            agents=agents,
            healing_agent=healing_agent,
            task=task,
            results={},
            errors={},
            step="start"
        )
        return await self.app.ainvoke(initial_state)
