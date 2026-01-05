#!/usr/bin/env python3
"""
COMPLETE TEST SUITE - All Scenarios
"""
import asyncio
import os
import sys
import importlib.util
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

async def run_scenario(scenario_name, script_path):
    """Run a single scenario"""
    print(f"\n{'='*60}")
    print(f"🚀 RUNNING: {scenario_name}")
    print(f"{'='*60}")
    
    try:
        # Dynamically import and run the script
        spec = importlib.util.spec_from_file_location(scenario_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Try different function names
        if hasattr(module, 'main'):
            await module.main()
        elif hasattr(module, 'run_comparison'):
            await module.run_comparison()
        elif hasattr(module, 'scenario_c_demo'):
            await module.scenario_c_demo()
        elif hasattr(module, 'scenario_d_demo'):
            await module.scenario_d_demo()
        elif hasattr(module, 'simple_demo'):
            await module.simple_demo()
        elif hasattr(module, 'demo_custom_agents'):
            await module.demo_custom_agents()
        elif hasattr(module, 'complete_working_test'):
            await module.complete_working_test()
        else:
            print(f"❌ No known entry function found in {script_path}")
            return (scenario_name, False, "No known entry function")
        
        return (scenario_name, True, "Success")
        
    except Exception as e:
        print(f"❌ {scenario_name}: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return (scenario_name, False, str(e))

async def run_all_scenarios():
    """Run all improvement scenarios"""
    
    print("="*80)
    print("🎯 COMPLETE SELF-HEALING AGENTS TEST SUITE")
    print("="*80)
    
    scenarios = [
        ("TASK 1: Baseline Comparison", "examples/baseline_stock_bot.py"),
        ("TASK 2: LLM Comparison", "examples/llm_comparison.py"),
        ("TASK 3: Bug Detection & Code Regeneration", "examples/scenario_c_bug_fixing.py"),
        ("TASK 4: Security Attack Detection", "examples/scenario_d_security.py")
    ]
    
    results = []
    
    for scenario_name, script_path in scenarios:
        if os.path.exists(script_path):
            result = await run_scenario(scenario_name, script_path)
            results.append(result)
        else:
            print(f"❌ Script not found: {script_path}")
            results.append((scenario_name, False, f"Script not found: {script_path}"))
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 TEST SUITE SUMMARY")
    print(f"{'='*80}")
    
    successful = sum(1 for r in results if r[1])
    total = len(results)
    
    print(f"\n🎯 RESULTS: {successful}/{total} scenarios successful ({successful/total*100:.0f}%)")
    
    for i, (name, success, message) in enumerate(results, 1):
        status = "✅" if success else "❌"
        print(f"{i}. {status} {name}: {message}")
    
    if successful == total:
        print(f"\n{'='*80}")
        print("🎉 ALL SCENARIOS PASSED SUCCESSFULLY!")
        print(f"{'='*80}")
    else:
        print(f"\n{'='*80}")
        print(f"⚠️  {total - successful} SCENARIOS FAILED - NEEDS FIXING")
        print(f"{'='*80}")

if __name__ == "__main__":
    asyncio.run(run_all_scenarios())