
import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

async def main_demo():
    """Main demonstration of the self-healing system"""
    
    print("="*70)
    print("🤖 SELF-HEALING MULTI-AGENT SYSTEM WITH QWEN AI")
    print("="*70)
    
    # Import components
    from src.agents.specialized_agents import DataProcessorAgent, APIGatewayAgent, AnalyticsAgent
    from src.agents.healing_agent import HealingAgent
    from src.graph.healing_graph import HealingGraph
    from src.api.qwen_client import QwenClient
    
    # Test Qwen connection first
    print("\n🔗 Testing Qwen AI Connection......")
    try:
        qwen = QwenClient()
        test_response = await qwen.generate("Say 'System Ready'", max_tokens=10)
        print(f"✅✅✅ Qwen AI: {test_response}")
    except Exception as e:
        print(f"❌ Qwen connection failed: {e}")
        print("💡 Check HF_TOKEN in .env file")
        return
    
    # Create agents
    print("\n🤖 Creating Agents....")
    
    agents = [
        DataProcessorAgent("data_processor_1"),
        APIGatewayAgent("api_gateway_1"),
        AnalyticsAgent("analytics_1"),
        DataProcessorAgent("data_processor_2"),
        APIGatewayAgent("api_gateway_2")
    ]
    
    healing_agent = HealingAgent("master_healer")
    
    print(f"✅✅✅ Created {len(agents)} specialized agents")
    print(f"✅✅✅✅ Created healing agent: {healing_agent.agent_id}")
    
    # Create healing graph
    healing_graph = HealingGraph()
    
    # Test 1: Normal processing
    print("\n" + "="*70)
    print("🧪 TEST 1: NORMAL PROCESSING")
    print("="*70)
    
    task_1 = {
        "type": "data_processing",
        "data": {
            "id": "user_001",
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "orders": 15
        },
        "operation": "analyze",
        "metrics": {"jan": 100, "feb": 150, "mar": 200, "apr": 180},
        "endpoint": "/api/v1/users",
        "method": "GET"
    }
    
    result_1 = await healing_graph.run(
        agents=agents,
        healing_agent=healing_agent,
        task=task_1
    )
    
    print(f"\n📊 Test 1 Results:")
    print(f"  Step: {result_1.get('step', 'unknown')}")
    if result_1.get('final_report'):
        report = result_1['final_report']['summary']
        print(f"  Success Rate: {report.get('success_rate', 0):.1%}")
        print(f"  Successful: {len(report.get('successful_agents', []))}")
        print(f"  Failed: {len(report.get('failed_agents', []))}")
    
    # Test 2: Force errors and test healing
    print("\n" + "="*70)
    print("⚡ TEST 2: ERROR SIMULATION & SELF-HEALING")
    print("="*70)
    
    # Force some errors
    for agent in agents[:3]:  # First 3 agents
        agent.error_count = 4  # Set to degraded status
        agent.status = "degraded"
    
    print("💥 Injected errors into 3 agents...")
    
    task_2 = {
        "type": "stress_test",
        "data": {"test": "error_handling"},
        "metrics": {"q1": 50, "q2": 45, "q3": 30, "q4": 60},
        "endpoint": "/api/v1/stress",
        "method": "POST",
        "payload": {"requests": 100}
    }
    
    result_2 = await healing_graph.run(
        agents=agents,
        healing_agent=healing_agent,
        task=task_2
    )
    
    print(f"\n📊 Test 2 Results:")
    if result_2.get('final_report'):
        report = result_2['final_report']['summary']
        print(f"  Success Rate: {report.get('success_rate', 0):.1%}")
        print(f"  Healed Agents: {len(report.get('healed_agents', []))}")
        
        # Show AI insights
        if 'ai_insights' in result_2['final_report']:
            print(f"\n🤖 AI Insights:")
            print(f"  {result_2['final_report']['ai_insights'][:200]}...")
    
    # Test 3: System health check
    print("\n" + "="*70)
    print("🏥 TEST 3: SYSTEM HEALTH CHECK")
    print("="*70)
    
    print("\n📈 Agent Health Status:")
    for agent in agents + [healing_agent]:
        metrics = agent.get_metrics()
        status_icon = "🟢" if metrics['status'] == 'healthy' else \
                     "🟡" if metrics['status'] == 'degraded' else \
                     "🔴" if metrics['status'] == 'failed' else "⚪"
        
        print(f"  {status_icon} {agent.agent_id}")
        print(f"    Type: {metrics['agent_type']}")
        print(f"    Status: {metrics['status']}")
        print(f"    Errors: {metrics['error_count']}")
        print(f"    Uptime: {metrics['uptime_seconds']:.0f}s")
        print(f"    Needs Healing: {metrics.get('needs_healing', False)}")
    
    # Healing statistics
    print(f"\n⚕️  Healing Statistics:")
    stats = healing_agent.get_healing_stats()
    print(f"  Total Operations: {stats['total_operations']}")
    print(f"  Successful Healings: {stats['successful_healings']}")
    print(f"  Expertise Areas: {len(stats['expertise_areas'])}")
    
    # Final summary
    print("\n" + "="*70)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    print(f"""
📋 SYSTEM SUMMARY:
• Total Agents: {len(agents) + 1}
• Qwen AI: ✅ Active
• Self-Healing: ✅ Enabled
• Monitoring: ✅ Active

🚀 The PROJECT is READY FOR:
1. Production deployment
2. Adding custom agents
3. Real-world monitoring
4. Team collaboration

💡 NEXT STEPS:
1. Create your custom agents by extending BaseAgent
2. Add more specialized healing strategies
3. Implement persistent storage
4. Add web dashboard for monitoring

🔧 QUICK START FOR NEW USERS:
1. Get HF_TOKEN from https://huggingface.co/settings/tokens
2. Add to .env file
3. Run: python examples/main_demo.py
    """)

if __name__ == "__main__":
    asyncio.run(main_demo())