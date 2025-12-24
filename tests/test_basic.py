
import pytest
import asyncio

@pytest.mark.asyncio
async def test_imports():
    """Test that all modules import correctly"""
    from src.api.qwen_client import QwenClient
    from src.agents.base_agent import BaseAgent
    from src.agents.healing_agent import HealingAgent
    from src.agents.specialized_agents import DataProcessorAgent
    
    assert True  # If we get here, imports work

@pytest.mark.asyncio
async def test_agent_creation():
    """Test creating a basic agent"""
    from src.agents.base_agent import BaseAgent
    
    class TestAgent(BaseAgent):
        async def process(self, task):
            return {"test": "passed"}
    
    agent = TestAgent("test_agent")
    assert agent.agent_id == "test_agent"
    assert agent.agent_type == "generic"