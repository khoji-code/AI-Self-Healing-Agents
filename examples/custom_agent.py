
import asyncio
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()



async def demo_custom_agents():
    print("="*60)
    print("🛠️  CREATING CUSTOM AGENTS - start")
    print("="*60)
    
    from src.agents.base_agent import BaseAgent
    from src.agents.healing_agent import HealingAgent
    

    # Example Custom Agent
    class EmailAgent(BaseAgent):
        """Sends and manages emails"""
        
        def __init__(self, agent_id="email_manager"):
            super().__init__(agent_id, "email_sender")
        
        async def process(self, task):
            recipient = task.get("to")
            subject = task.get("subject", "No Subject")
            
            if not recipient:
                raise ValueError("Recipient email required")
            
            return {
                "email_id": f"email_001",
                "sent_to": recipient,
                "subject": subject,
                "status": "success"
            }
    
    print("\n🚀 Creating and Testing Custom Agents......")
    
    # Create instances
    email_agent = EmailAgent("my_email_sender")
    healer = HealingAgent("system_healer")
    
    print(f"\n✅✅✅ Created agents:")
    print(f"   • {email_agent.agent_id} - {email_agent.agent_type}")
    print(f"   • {healer.agent_id} - {healer.agent_type}")
    
    # Test Email Agent
    print("\n📧 Testing Email Agent...")
    result = await email_agent.execute({
        "to": "khoji2001social@gmail.com",
        "subject": "Welcome to Self-Healing Agents"
    })
    print(f"   Status: {result['result']['status'] if result['success'] else 'Failed'}")
    
    print("\n" + "="*60)
    print("🎯 CUSTOM AGENT DEMO COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(demo_custom_agents())