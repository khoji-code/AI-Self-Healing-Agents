import asyncio
import random
from src.agents.base_agent import BaseAgent
from src.agents.healing_agent import HealingAgent
from dotenv import load_dotenv

# Load secrets
load_dotenv()

# Custom Agent
class StockMonitorAgent(BaseAgent):
    """Monitors stock prices and crashes if 'API' fails"""
    
    def __init__(self, agent_id="stock_bot"):
        # Skeleton
        super().__init__(agent_id, "stock_monitor")

    async def process(self, task):
        symbol = task.get("symbol")
        print(f"\n📈 Checking price for {symbol}.....")
        
        await asyncio.sleep(0.5)
        
        # 30% chance the "API" fails and throws an error
        if random.random() < 0.3:
            print("  💥 API Error: Connection Reset by NYSE!!!")
            raise Exception("API Connection Failed: Timeout waiting for data")
            
        # If no error, return a fake price
        price = random.randint(100, 200)
        return {"symbol": symbol, "price": price, "status": "active"}

# Main Loop
async def main():
    print("🚀 Starting Stock Monitor System.....")
    
    # Create the Team
    trader = StockMonitorAgent("wall_street_bot")
    doctor = HealingAgent("market_healer")
    
    # A list of stocks to check
    stock_symbols = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN", "NFLX", "NVDA", "META", "AMD", "INTC"]
    
    print(f"📋 Jobs to process --> {len(stock_symbols)}")
    
    for i, symbol in enumerate(stock_symbols):
        print(f"\n--- Job {i+1}: {symbol} ---------")
        
        try:
            
            result = await trader.execute({"symbol": symbol})
            
            if result['success']:
                print(f"  ✅ Price: ${result['result']['price']}")
            else:
                print(f"  ❌ Fetch Failed! Error count: {trader.error_count}")
                
                
                if trader.error_count >= 2:
                    print("  🚑🚑 CRITICAL: Agent is unstable. Calling Doctor.....")
                    
                    healing_job = {
                        "type": "heal_agent",
                        "target_agent": trader.agent_id,
                        "issue": "API Connection Failed",
                        "metrics": trader.get_metrics()
                    }
                    
                    # fixes the agent
                    cure = await doctor.process(healing_job)
                    print(f"  💉 Doctor Action: {cure.get('message')}")
                    print("  ✨ Agent has been reset and healed.")
                    
        except Exception as e:
            print(f"System Critical Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())