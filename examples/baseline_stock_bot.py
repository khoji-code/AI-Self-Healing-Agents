#!/usr/bin/env python3
"""
BASELINE Stock Bot WITHOUT Self-Healing - For Comparison
"""
import asyncio
import random
import time
from dotenv import load_dotenv

load_dotenv()

class BaselineStockAgent:
    """Baseline stock agent without self-healing"""
    
    def __init__(self, agent_id="baseline_stock_bot"):
        self.agent_id = agent_id
        self.status = "healthy"
        self.error_count = 0
        self.success_count = 0
        
    async def process(self, symbol):
        """Check stock price with 30% failure rate"""
        print(f"📈 [BASELINE] Checking {symbol}...")
        
        await asyncio.sleep(0.3)
        
        # 30% chance of failure (same as healing version)
        if random.random() < 0.3:
            self.error_count += 1
            raise Exception(f"API Connection Failed for {symbol}")
        
        self.success_count += 1
        return random.randint(100, 200)

async def main():
    """Run comparison experiment"""
    print("="*70)
    print("📊 BASELINE SYSTEM EXPERIMENT (No Self-Healing)")
    print("="*70)
    
    stock_symbols = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN", "NFLX", "NVDA", "META"]
    
    # Baseline system
    baseline_agent = BaselineStockAgent("baseline_bot")
    baseline_results = []
    
    print(f"\n📋 Processing {len(stock_symbols)} stocks with BASELINE system...")
    
    for i, symbol in enumerate(stock_symbols):
        print(f"\n--- Job {i+1}: {symbol} ---------")
        
        try:
            price = await baseline_agent.process(symbol)
            baseline_results.append(True)
            print(f"  ✅ Price: ${price}")
        except Exception as e:
            baseline_results.append(False)
            print(f"  ❌ Failed: {str(e)[:40]}")
            
            # NO HEALING - just continue with errors
            if baseline_agent.error_count >= 3:
                print(f"  ⚠️  Agent has {baseline_agent.error_count} errors (No healing available)")
    
    # Calculate metrics
    baseline_success = baseline_results.count(True)
    baseline_failure = baseline_results.count(False)
    baseline_success_rate = baseline_success / len(baseline_results) if baseline_results else 0
    
    print("\n" + "="*70)
    print("📊 BASELINE SYSTEM RESULTS:")
    print("="*70)
    print(f"""
📈 Performance Metrics:
• Total Jobs: {len(stock_symbols)}
• Successful: {baseline_success}
• Failed: {baseline_failure}
• Success Rate: {baseline_success_rate:.1%}

⚠️  Issues:
• Error Count: {baseline_agent.error_count}
• Final Status: {baseline_agent.status}
• No automatic healing available
• Manual restart required: {baseline_agent.error_count > 3}

🔧 Limitations:
1. No error recovery
2. No automatic diagnosis
3. No proactive healing
4. Manual intervention needed
    """)

if __name__ == "__main__":
    asyncio.run(main())