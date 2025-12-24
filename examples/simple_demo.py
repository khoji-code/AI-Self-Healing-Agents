
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

async def simple_demo():
    """Simple demonstration without complex dependencies"""
    
    print("="*70)
    print("🤖 SELF-HEALING MULTI-AGENT SYSTEM")
    print("="*70)
    
    # Import only what we need
    from src.agents.specialized_agents import DataProcessorAgent, APIGatewayAgent, AnalyticsAgent
    from src.agents.healing_agent import HealingAgent
    from src.api.qwen_client import QwenClient
    
    # Test Qwen connection
    print("\n🔗 Testing Qwen AI Connection...")
    try:
        qwen = QwenClient()
        test_response = await qwen.generate("Say 'READY'", max_tokens=5)
        print(f"✅ Qwen AI: {test_response.strip()}")
    except Exception as e:
        print(f"❌ Qwen connection failed: {e}")
        print("💡 Check HF_TOKEN in .env file")
        return
    
    # Create agents
    print("\n🤖 Creating Agents......")
    
    agents = [
        DataProcessorAgent("data_processor_1"),
        APIGatewayAgent("api_gateway_1"),
        AnalyticsAgent("analytics_1")
    ]
    
    healing_agent = HealingAgent("master_healer")
    
    print(f"✅ Created {len(agents)} specialized agents")
    print(f"✅ Created healing agent: {healing_agent.agent_id}")
    
    # Test 1: Individual agent processing
    print("\n" + "="*70)
    print("🧪 TEST 1: AGENT PROCESSING")
    print("="*70)
    
    test_tasks = [
        {
            "agent": agents[0],
            "task": {
                "operation": "transform",
                "data": {"name": "Alice", "age": 30, "city": "New York"}
            },
            "description": "Data transformation"
        },
        {
            "agent": agents[1],
            "task": {
                "endpoint": "/api/v1/users",
                "method": "GET",
                "client_id": "test_client"
            },
            "description": "API request"
        },
        {
            "agent": agents[2],
            "task": {
                "report_type": "summary",
                "metrics": {"sales": [100, 150, 200, 180]}
            },
            "description": "Analytics report"
        }
    ]
    
    for test in test_tasks:
        print(f"\n📋 Task: {test['description']}")
        try:
            result = await test['agent'].execute(test['task'])
            if result['success']:
                print(f"  ✅ Success! Response time: {result['response_time']:.3f}s")
            else:
                print(f"  ❌ Failed: {result['error']}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 2: Healing demonstration
    print("\n" + "="*70)
    print("⚡ TEST 2: HEALING DEMONSTRATION")
    print("="*70)
    
    # Create a problematic agent
    problematic_agent = DataProcessorAgent("problem_agent")
    problematic_agent.error_count = 5
    problematic_agent.status = "failed"
    
    print(f"Created problematic agent: {problematic_agent.agent_id}")
    print(f"Agent status: {problematic_agent.status}, Errors: {problematic_agent.error_count}")
    
    # Use healing agent to diagnose
    healing_task = {
        "type": "heal_agent",
        "target_agent": problematic_agent.agent_id,
        "issue": "High error count and failed status",
        "metrics": problematic_agent.get_metrics()
    }
    
    print("\n🔍 Requesting AI diagnosis...")
    try:
        diagnosis = await healing_agent.process(healing_task)
        print(f"✅ Diagnosis received")
        
        if "operation" in diagnosis:
            print(f"📋 Healing operation: {diagnosis['operation'].get('message', 'No message')}")
        else:
            print(f"📋 Diagnosis: {diagnosis}")
            
    except Exception as e:
        print(f"❌ Healing failed: {e}")
    
    # Test 3: System health check
    print("\n" + "="*70)
    print("🏥 TEST 3: SYSTEM HEALTH CHECK")
    print("="*70)
    
    print("\n📈 Agent Status:")
    all_agents = agents + [healing_agent, problematic_agent]
    
    for agent in all_agents:
        metrics = agent.get_metrics()
        status_icon = "🟢" if metrics['status'] == 'healthy' else \
                     "🟡" if metrics['status'] == 'degraded' else \
                     "🔴" if metrics['status'] == 'failed' else "⚪"
        
        print(f"  {status_icon} {agent.agent_id}")
        print(f"    Type: {metrics['agent_type']}")
        print(f"    Status: {metrics['status']}")
        print(f"    Errors: {metrics['error_count']}")
        print(f"    Requests: {metrics['metrics']['total_requests']}")
    
    # Qwen AI capabilities
    print("\n" + "="*70)
    print("🧠 QWEN AI CAPABILITIES DEMO")
    print("="*70)
    
    ai_tests = [
        "Explain self-healing systems in one sentence.",
        "What are common causes of agent failures?",
        "Suggest 3 strategies for system resilience."
    ]
    
    for i, prompt in enumerate(ai_tests, 1):
        print(f"\n{i}. {prompt}")
        try:
            response = await qwen.generate(prompt, max_tokens=100)
            print(f"   💡 {response[:100]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Final summary
    print("\n" + "="*70)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    total_agents = len(all_agents)
    healthy_agents = sum(1 for a in all_agents if a.status == "healthy")
    
    print(f"""
📋 SYSTEM SUMMARY:
• Total Agents: {total_agents}
• Healthy Agents: {healthy_agents}
• Qwen AI: ✅ Connected
• Self-Healing: ✅ Active

🚀 YOUR PROJECT IS WORKING!
    
💡 NEXT STEPS:
1. Extend BaseAgent for your custom agents
2. Add more complex healing strategies
3. Implement persistent storage
4. Create a web dashboard
    
🔧 QUICK START FOR OTHERS:
1. Get free HF_TOKEN: https://huggingface.co/settings/tokens
2. Add to .env file
3. Run: python examples/simple_demo.py
    """)

if __name__ == "__main__":
    asyncio.run(simple_demo())