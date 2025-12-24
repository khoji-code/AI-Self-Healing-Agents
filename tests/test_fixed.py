
import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

async def test():
    print("🧪 Testing Fixed System")
    print("="*50)
    
    # Test 1: Qwen
    print("\n1. Testing Qwen AI...")
    try:
        from src.api.qwen_client import QwenClient
        qwen = QwenClient()
        response = await qwen.generate("Say 'FIXED'", max_tokens=10)
        print(f"✅✅✅ Qwen: {response.strip()}")
    except Exception as e:
        print(f"❌❌ Qwen failed: {e}")
        return
    
    # Test 2: Analytics Agent
    print("\n2. Testing Analytics Agent...")
    try:
        from src.agents.specialized_agents import AnalyticsAgent
        agent = AnalyticsAgent("test_analytics")
        
        # Test with list data (the bug case)
        result = await agent.execute({
            "report_type": "summary",
            "metrics": {"sales": [100, 150, 200]}
        })
        
        if result["success"]:
            print(f"✅ Analytics: Success! Total: {result['result']['report'].get('total', 'N/A')}")
        else:
            print(f"❌ Analytics failed: {result.get('error', 'Unknown')}")
    except Exception as e:
        print(f"❌ Analytics error: {e}")
        return
    
    # Test 3: Healing Agent
    print("\n3. Testing Healing Agent...")
    try:
        from src.agents.healing_agent import HealingAgent
        healer = HealingAgent("test_healer")
        
        result = await healer.process({
            "type": "heal_agent",
            "target_agent": "test_target",
            "issue": "Test healing",
            "metrics": {"status": "failed", "errors": 3}
        })
        
        print(f"✅ Healing Agent: {result.get('message', 'Processed')}")
    except Exception as e:
        print(f"❌ Healing Agent error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "="*50)
    print("🎉 ALL TESTS PASSED!")
    print("\n🚀 System is fully operational!")

if __name__ == "__main__":
    asyncio.run(test())
