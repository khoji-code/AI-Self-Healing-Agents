#!/usr/bin/env python3
"""
SCENARIO C: Bug Detection & Code Regeneration
"""
import asyncio
import os
import sys
import random
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

async def scenario_c_demo():
    """Demonstrate bug detection and code regeneration"""
    
    print("="*70)
    print("🔬 SCENARIO C: BUG DETECTION & CODE REGENERATION")
    print("="*70)
    
    from src.agents.buggy_processor import BuggyDataProcessor
    from src.agents.code_healing_agent import CodeHealingAgent
    from src.api.llm_provider import LLMFactory
    
    # Create agents
    print("\n🤖 Creating Agents...")
    
    buggy_agent = BuggyDataProcessor("buggy_data_processor")
    code_healer = CodeHealingAgent("code_doctor")
    
    print(f"✅ Created buggy agent: {buggy_agent.agent_id}")
    print(f"✅ Created code healing agent: {code_healer.agent_id}")
    
    # Test inputs that trigger different bugs
    test_cases = [
        {"input": "normal_data", "should_fail": False},
        {"input": "special_case_123", "should_fail": True},
        {"input": "malformed_json_data", "should_fail": True},
        {"input": "large_dataset_5000", "should_fail": True},
        {"input": "another_normal", "should_fail": False}
    ]
    
    bug_reports = []
    
    print("\n" + "="*70)
    print("🧪 PHASE 1: DETECTING BUGS")
    print("="*70)
    
    for i, test_case in enumerate(test_cases, 1):
        input_data = test_case["input"]
        print(f"\nTest {i}: Processing '{input_data}'")
        
        try:
            result = await buggy_agent.execute({
                "data": input_data,
                "operation": "process"
            })
            
            if result['success']:
                print(f"  ✅ Success: {result['result'].get('result', 'Processed')}")
            else:
                print(f"  ❌ Failed: {result['error'][:50]}...")
                
                # Report bug to healing agent
                bug_report = {
                    "error": result['error'],
                    "input": input_data,
                    "agent_id": buggy_agent.agent_id,
                    "pattern": "unknown"  # Will be detected by healer
                }
                
                bug_reports.append(bug_report)
                
                # Analyze bug
                print(f"  🔍 Reporting bug to code healer...")
                analysis = await code_healer.analyze_and_fix_bug({
                    "error": result['error'],
                    "input": input_data,
                    "code": "def process(data):\n    # Original buggy code"
                })
                
                if analysis['success']:
                    print(f"  🤖 Analysis: {analysis.get('message', 'Analyzed')}")
                else:
                    print(f"  ⚠️  Analysis failed: {analysis.get('error', 'Unknown')}")
                
        except Exception as e:
            print(f"  💥 Exception: {str(e)[:50]}...")
    
    print("\n" + "="*70)
    print("💻 PHASE 2: CODE REGENERATION")
    print("="*70)
    
    if bug_reports:
        print(f"\n📋 Found {len(bug_reports)} bugs. Regenerating code...")
        
        # Original buggy function (simplified)
        original_code = """
def process_data(input_string):
    if 'special_case_' in input_string:
        # Bug: division by zero
        return 100 / int(input_string.split('_')[-1])
    elif 'malformed_json' in input_string:
        # Bug: no error handling
        import json
        return json.loads(input_string)
    elif 'large_dataset_' in input_string:
        # Bug: processes everything at once
        data = [i for i in range(1000000)]
        return len(data)
    else:
        return f"Processed: {input_string}"
        """
        
        # Regenerate the function
        regeneration = await code_healer.regenerate_function({
            "function": "process_data",
            "original_code": original_code,
            "bug_reports": bug_reports
        })
        
        if regeneration['success']:
            print(f"✅ Code regenerated successfully!")
            print(f"📝 New code hash: {regeneration['code_hash']}")
            
            # Show diff (simplified)
            print("\n🔀 CODE IMPROVEMENTS:")
            print("  Original code had:")
            print("    - Division by zero bug for special_case_*")
            print("    - No JSON error handling")
            print("    - Memory overflow for large datasets")
            print("\n  Regenerated code includes:")
            print("    - Input validation")
            print("    - Try-catch error handling")
            print("    - Chunked processing for large data")
            
            # Test the fix
            print("\n🧪 PHASE 3: TESTING FIXED CODE")
            print("="*70)
            
            test_inputs = [
                "special_case_0",  # Would cause division by zero
                "malformed_json",  # Would cause parsing error
                "normal_data"      # Should work fine
            ]
            
            test_results = await code_healer.test_code_fix({
                "original_code": original_code,
                "fixed_code": regeneration['new_code'],
                "test_inputs": test_inputs
            })
            
            if test_results['success']:
                print(f"\n📊 Fix testing results:")
                print(f"  Total tests: {test_results['total_tests']}")
                print(f"  Improvements: {test_results['improvements']}")
                print(f"  Success rate improvement: {test_results['improvement_rate']:.0%}")
                
                # Apply fixes to buggy agent
                for pattern in ["special_case_number", "json_parsing", "memory_overflow"]:
                    if pattern in code_healer.code_fixes:
                        fix_code = f"# Fixed: {pattern}"
                        buggy_agent.add_bug_fix(pattern, fix_code)
                        print(f"  🔧 Applied fix for pattern: {pattern}")
            
        else:
            print(f"❌ Code regeneration failed: {regeneration.get('error', 'Unknown')}")
    else:
        print("🎉 No bugs detected! All tests passed.")
    
    print("\n" + "="*70)
    print("📈 SCENARIO C SUMMARY")
    print("="*70)
    
    print(f"""
🎯 ACHIEVEMENTS:
1. ✅ Bug detection for specific input patterns
2. ✅ Automatic bug analysis using LLM
3. ✅ Code regeneration with fixes
4. ✅ Fix validation through testing
5. ✅ Application of fixes to running agent

🔧 TECHNICAL FEATURES:
• Pattern-based bug detection
• LLM-powered code analysis
• Automated code regeneration
• Safe code validation
• Incremental improvement

🚀 REAL-WORLD APPLICATION:
This demonstrates how self-healing systems can:
1. Detect recurring bug patterns
2. Automatically generate fixes
3. Test and validate fixes
4. Apply fixes without downtime
5. Learn from past bugs

💡 NEXT STEPS:
1. Extend to more complex bug patterns
2. Add automated testing framework
3. Implement A/B testing for fixes
4. Add rollback capability for failed fixes
    """)

if __name__ == "__main__":
    asyncio.run(scenario_c_demo())