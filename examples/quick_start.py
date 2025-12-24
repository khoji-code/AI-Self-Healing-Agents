
import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

async def main():
    print("="*60)
    print("🚀 SELF-HEALING AGENTS - QUICK START")
    print("="*60)
    
    # Test Qwen AI
    print("\n1️⃣  Testing Qwen AI Connection......")
    try:
        from src.api.qwen_client import QwenClient
        qwen = QwenClient()
        response = await qwen.generate("Say 'SYSTEM READY'", max_tokens=10)
        print(f"   ✅✅✅ Qwen AI: {response.strip()}")
    except Exception as e:
        print(f"   ❌ Qwen failed: {e}")
        print("   💡 Check HF_TOKEN in .env file")
        return
    
    # Test Agent Creation
    print("\n2️⃣  Testing Agent System...")
    try:
        from src.agents.base_agent import BaseAgent
        
        class TestAgent(BaseAgent):
            async def process(self, task):
                return {"test": "passed"}
        
        agent = TestAgent("test_agent")
        result = await agent.execute({"action": "test"})
        print(f"   ✅ Agent System: {result['success']}")
    except Exception as e:
        print(f"   ❌ Agent system failed: {e}")
        return
    
    # Test Healing Agent
    print("\n3️⃣  Testing Self-Healing...")
    try:
        from src.agents.healing_agent import HealingAgent
        healer = HealingAgent("quick_healer")
        print(f"   ✅ Healing Agent: {healer.agent_id}")
    except Exception as e:
        print(f"   ❌ Healing agent failed: {e}")
        return
    
    print("\n" + "="*60)
    print("🎉 ALL SYSTEMS OPERATIONAL!")
    print("="*60)
    
    print("""
✅ VERIFICATION COMPLETE:
• Qwen AI: ✅ Connected & Responding
• Agent System: ✅ Creating & Executing
• Self-Healing: ✅ Ready

🚀 NEXT STEPS:
1. Run: python examples/simple_demo.py
2. Run: python examples/final_demo.py
3. Create custom agents: python examples/custom_agent.py
    """)

if __name__ == "__main__":
    asyncio.run(main())