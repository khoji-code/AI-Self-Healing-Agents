import asyncio
import os
from dotenv import load_dotenv
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

async def test():
    from src.api.llm_provider import LLMFactory
    
    print("Testing fixed Qwen client...")
    
    try:
        llm = LLMFactory.from_env()
        
        print("Testing health check...")
        healthy = await llm.check_health()
        print(f"Health check: {'✅' if healthy else '❌'}")
        
        if healthy:
            print("Testing generation...")
            response = await llm.generate("Say 'Test successful'", max_tokens=10)
            print(f"✅ Response: {response}")
        else:
            print("LLM is not accessible")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())