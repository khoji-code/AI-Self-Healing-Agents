#!/usr/bin/env python3
"""
LLM Comparison Test
"""
import asyncio
import os
import sys
import time
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

async def main():
    """Compare different LLM providers"""
    print("="*70)
    print("🤖 LLM PROVIDER COMPARISON")
    print("="*70)
    
    from src.api.llm_provider import LLMConfig, LLMProvider, LLMFactory
    
    # Test prompts
    test_prompts = [
        "Explain self-healing systems in one sentence.",
        "What are 3 common causes of software failures?",
        "Suggest a strategy for automatic error recovery."
    ]
    
    # Test configurations
    llm_configs = []
    
    # Qwen config
    if os.getenv("HF_TOKEN"):
        llm_configs.append({
            "name": "Qwen 7B",
            "config": LLMConfig(
                provider=LLMProvider.QWEN,
                model="Qwen/Qwen2.5-7B-Instruct",
                api_key=os.getenv("HF_TOKEN")
            )
        })
    
    # OpenAI config (if available)
    if os.getenv("OPENAI_API_KEY"):
        llm_configs.append({
            "name": "OpenAI GPT-3.5",
            "config": LLMConfig(
                provider=LLMProvider.OPENAI,
                model="gpt-3.5-turbo",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        })
    
    results = []
    
    for llm_info in llm_configs:
        print(f"\n🧪 Testing {llm_info['name']}...")
        
        try:
            llm = LLMFactory.create_client(llm_info['config'])
            
            # Health check
            if not await llm.check_health():
                print(f"  ❌ {llm_info['name']} is not accessible")
                continue
            
            # Test responses
            responses = []
            start_time = time.time()
            
            for prompt in test_prompts:
                try:
                    response = await llm.generate(prompt, max_tokens=100)
                    responses.append(response[:100] + "..." if len(response) > 100 else response)
                except Exception as e:
                    responses.append(f"Error: {str(e)}")
            
            total_time = time.time() - start_time
            avg_time = total_time / len(test_prompts)
            
            results.append({
                "name": llm_info['name'],
                "provider": llm_info['config'].provider.value,
                "model": llm_info['config'].model,
                "success": True,
                "avg_response_time": avg_time,
                "responses": responses,
                "total_time": total_time
            })
            
            print(f"  ✅ Success! Avg response: {avg_time:.2f}s")
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results.append({
                "name": llm_info['name'],
                "success": False,
                "error": str(e)
            })
    
    # Display comparison
    print("\n" + "="*70)
    print("📊 LLM COMPARISON RESULTS")
    print("="*70)
    
    successful_llms = [r for r in results if r['success']]
    
    if successful_llms:
        print("\n🏆 PERFORMANCE COMPARISON:")
        print("-"*50)
        
        for result in successful_llms:
            print(f"\n{result['name']} ({result['model']}):")
            print(f"  Provider: {result['provider']}")
            print(f"  Avg Response Time: {result['avg_response_time']:.2f}s")
            print(f"  Total Time: {result['total_time']:.2f}s")
            
            print("\n  Sample Responses:")
            for i, (prompt, response) in enumerate(zip(test_prompts, result['responses'])):
                print(f"    {i+1}. {prompt[:40]}...")
                print(f"       → {response}")
        
        # Find fastest
        fastest = min(successful_llms, key=lambda x: x['avg_response_time'])
        print(f"\n🎯 Fastest LLM: {fastest['name']} ({fastest['avg_response_time']:.2f}s)")
    
    print("\n💡 USAGE TIPS:")
    print("1. For free usage: Use Qwen with HF_TOKEN")
    print("2. For better quality: Use OpenAI GPT-4")
    print("3. Switch providers by changing LLM_PROVIDER in .env")
    print("\n.env configuration:")
    print("  LLM_PROVIDER=qwen  # or 'openai'")
    print("  HF_TOKEN=your_token  # for Qwen")
    print("  OPENAI_API_KEY=your_key  # for OpenAI")

if __name__ == "__main__":
    asyncio.run(main())