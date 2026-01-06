#!/usr/bin/env python3
"""
Benchmark Runner for Self-Healing Bug Detection
"""
import asyncio
import json
import os
import sys
import time
import ast
import statistics
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@dataclass
class TestResult:
    """Results of a single test case"""
    test_id: str
    test_name: str
    difficulty: str
    success: bool
    bugs_detected: List[str]
    bugs_missed: List[str]
    fix_generated: bool
    fix_valid: bool
    fix_improvement: float  # 0.0 to 1.0
    execution_time: float
    error_message: Optional[str] = None
    
    def to_dict(self):
        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "difficulty": self.difficulty,
            "success": self.success,
            "bugs_detected": self.bugs_detected,
            "bugs_missed": self.bugs_missed,
            "fix_generated": self.fix_generated,
            "fix_valid": self.fix_valid,
            "fix_improvement": self.fix_improvement,
            "execution_time": self.execution_time,
            "error_message": self.error_message
        }

class BenchmarkRunner:
    """Runs benchmark tests against healing system"""
    
    def __init__(self, benchmark_file: str = "tests/bug_benchmark.json"):
        self.benchmark_file = benchmark_file
        self.results: List[TestResult] = []
        self.healing_agent = None
        
    async def load_benchmark(self) -> Dict[str, Any]:
        """Load benchmark from JSON file"""
        try:
            with open(self.benchmark_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Benchmark file not found: {self.benchmark_file}")
            # Create minimal benchmark
            return {
                "name": "Default Benchmark",
                "test_cases": []
            }
    
    async def initialize_healing_agent(self):
        """Initialize the healing agent"""
        try:
            from src.agents.code_healing_agent import CodeHealingAgent
            from src.api.llm_provider import LLMFactory
            
            # Use mock LLM for testing
            from src.api.mock_llm import MockLLM
            
            class MockHealingAgent(CodeHealingAgent):
                def __init__(self):
                    # Skip parent initialization that needs LLM
                    from src.agents.base_agent import BaseAgent
                    BaseAgent.__init__(self, "benchmark_healer", "healer")
                    self.llm = MockLLM()
                    self.code_fixes = {}
                    self.bug_patterns = {}
                    self.regenerated_functions = {}
                    
            self.healing_agent = MockHealingAgent()
            print("✅ Initialized healing agent with mock LLM")
            
        except Exception as e:
            print(f"⚠️  Could not initialize healing agent: {e}")
            # Create minimal mock
            self.healing_agent = type('MockAgent', (), {
                'analyze_and_fix_bug': lambda self, task: {
                    "success": True,
                    "fix": "Mock fix"
                }
            })()
    
    async def run_test_case(self, test_case: Dict[str, Any]) -> TestResult:
        """Run a single test case"""
        start_time = time.time()
        
        result = TestResult(
            test_id=test_case["id"],
            test_name=test_case["name"],
            difficulty=test_case["difficulty"],
            success=False,
            bugs_detected=[],
            bugs_missed=[],
            fix_generated=False,
            fix_valid=False,
            fix_improvement=0.0,
            execution_time=0.0
        )
        
        try:
            # Step 1: Analyze the buggy code
            analysis = await self.analyze_buggy_code(test_case)
            
            if analysis["bugs_found"]:
                result.bugs_detected = analysis["bugs_found"]
                result.success = True
                
                # Step 2: Generate fix
                fix_result = await self.generate_fix(test_case, analysis)
                
                if fix_result["fix_generated"]:
                    result.fix_generated = True
                    
                    # Step 3: Validate fix
                    validation = await self.validate_fix(
                        test_case, 
                        analysis, 
                        fix_result
                    )
                    
                    result.fix_valid = validation["valid"]
                    result.fix_improvement = validation["improvement_score"]
                    
                    # Check for missed bugs
                    known_bugs = test_case.get("expected_fixes", [])
                    detected = set(result.bugs_detected)
                    expected = set(known_bugs)
                    result.bugs_missed = list(expected - detected)
                    
            else:
                result.error_message = "No bugs detected"
                result.bugs_missed = test_case.get("expected_fixes", [])
                
        except Exception as e:
            result.error_message = str(e)
            result.success = False
            
        result.execution_time = time.time() - start_time
        return result
    
    async def analyze_buggy_code(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze buggy code to detect bugs"""
        original_code = test_case["original_code"]
        
        # Simple static analysis
        bugs_found = []
        
        # Check for division by zero
        if "/" in original_code and "zero" not in original_code.lower():
            bugs_found.append("division_by_zero")
        
        # Check for null pointer
        if ".name" in original_code or ".upper()" in original_code:
            bugs_found.append("null_pointer")
        
        # Check for JSON parsing without try-catch
        if "json.loads" in original_code and "try:" not in original_code:
            bugs_found.append("json_parsing_unsafe")
        
        # Check for memory issues with large data
        if "large" in original_code.lower() or "1000000" in original_code:
            bugs_found.append("memory_issue")
        
        return {
            "bugs_found": bugs_found,
            "total_lines": len(original_code.split('\n')),
            "complexity": "high" if len(original_code) > 500 else "medium" if len(original_code) > 200 else "low"
        }
    
    async def generate_fix(self, test_case: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fix for buggy code"""
        if not self.healing_agent:
            return {"fix_generated": False, "error": "No healing agent"}
        
        try:
            # Simulate fix generation
            fix_result = await self.healing_agent.analyze_and_fix_bug({
                "error": f"Bug in {test_case['name']}",
                "input": "test input",
                "code": test_case["original_code"]
            })
            
            return {
                "fix_generated": fix_result.get("success", False),
                "fix_code": fix_result.get("analysis", {}).get("corrected_code", ""),
                "analysis": fix_result.get("analysis", {})
            }
            
        except Exception as e:
            return {"fix_generated": False, "error": str(e)}
    
    async def validate_fix(self, test_case: Dict[str, Any], 
                          analysis: Dict[str, Any], 
                          fix_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if fix actually works"""
        
        if not fix_result.get("fix_generated"):
            return {"valid": False, "improvement_score": 0.0}
        
        fix_code = fix_result.get("fix_code", "")
        
        # Simple validation checks
        improvement = 0.0
        checks_passed = 0
        total_checks = 4
        
        # Check 1: Code compiles
        try:
            ast.parse(fix_code)
            checks_passed += 1
        except:
            pass
        
        # Check 2: Has error handling
        if "try:" in fix_code and "except" in fix_code:
            checks_passed += 1
        
        # Check 3: Has input validation
        if any(keyword in fix_code for keyword in ["if", "is not None", "isinstance", "len("]):
            checks_passed += 1
        
        # Check 4: Addresses specific bug types
        expected_fixes = test_case.get("expected_fixes", [])
        addressed = 0
        for bug in expected_fixes:
            if bug in fix_code.lower().replace("_", ""):
                addressed += 1
        
        if expected_fixes:
            checks_passed += (addressed / len(expected_fixes))
        
        improvement = checks_passed / total_checks
        
        return {
            "valid": improvement > 0.5,
            "improvement_score": improvement,
            "checks_passed": checks_passed,
            "total_checks": total_checks
        }
    
    async def run_benchmark(self) -> Dict[str, Any]:
        """Run complete benchmark"""
        print("="*70)
        print("🏃 RUNNING BUG DETECTION BENCHMARK")
        print("="*70)
        
        benchmark = await self.load_benchmark()
        await self.initialize_healing_agent()
        
        print(f"\n📊 Benchmark: {benchmark.get('name', 'Unnamed')}")
        print(f"📋 Test Cases: {len(benchmark.get('test_cases', []))}")
        
        self.results = []
        
        for i, test_case in enumerate(benchmark.get("test_cases", []), 1):
            print(f"\n🔍 Test {i}: {test_case['name']} ({test_case['difficulty']})")
            print(f"   Description: {test_case['description'][:60]}...")
            
            result = await self.run_test_case(test_case)
            self.results.append(result)
            
            # Print result
            status = "✅" if result.success else "❌"
            print(f"   Result: {status} Bugs detected: {len(result.bugs_detected)}/{len(test_case.get('expected_fixes', []))}")
            print(f"   Fix: {'✅' if result.fix_generated else '❌'} Valid: {'✅' if result.fix_valid else '❌'}")
            print(f"   Improvement: {result.fix_improvement:.1%}")
        
        return await self.generate_benchmark_report(benchmark)
    
    async def generate_benchmark_report(self, benchmark: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive benchmark report"""
        
        if not self.results:
            return {"error": "No results generated"}
        
        # Calculate statistics
        difficulties = {"easy": [], "medium": [], "hard": []}
        for result in self.results:
            difficulties[result.difficulty].append(result)
        
        stats = {
            "total_tests": len(self.results),
            "tests_passed": sum(1 for r in self.results if r.success),
            "success_rate": sum(1 for r in self.results if r.success) / len(self.results) if self.results else 0,
            "fix_generation_rate": sum(1 for r in self.results if r.fix_generated) / len(self.results) if self.results else 0,
            "fix_validation_rate": sum(1 for r in self.results if r.fix_valid) / len(self.results) if self.results else 0,
            "average_improvement": statistics.mean([r.fix_improvement for r in self.results if r.fix_generated]) if any(r.fix_generated for r in self.results) else 0,
            "average_execution_time": statistics.mean([r.execution_time for r in self.results]),
            "by_difficulty": {}
        }
        
        for diff, results in difficulties.items():
            if results:
                stats["by_difficulty"][diff] = {
                    "count": len(results),
                    "success_rate": sum(1 for r in results if r.success) / len(results),
                    "avg_improvement": statistics.mean([r.fix_improvement for r in results]),
                    "avg_time": statistics.mean([r.execution_time for r in results])
                }
        
        # Calculate score
        scoring = benchmark.get("scoring", {
            "detection_weight": 0.4,
            "fix_weight": 0.4,
            "performance_weight": 0.2
        })
        
        detection_score = stats["success_rate"]
        fix_score = stats["fix_validation_rate"]
        performance_score = 1.0 - min(stats["average_execution_time"] / 10.0, 1.0)  # Normalize
        
        total_score = (
            detection_score * scoring["detection_weight"] +
            fix_score * scoring["fix_weight"] +
            performance_score * scoring["performance_weight"]
        )
        
        # Apply difficulty multiplier
        difficulty_multiplier = scoring.get("difficulty_multiplier", {"easy": 1.0, "medium": 1.5, "hard": 2.0})
        weighted_score = 0
        total_weight = 0
        
        for diff, diff_stats in stats["by_difficulty"].items():
            multiplier = difficulty_multiplier.get(diff, 1.0)
            weighted_score += diff_stats["success_rate"] * multiplier * diff_stats["count"]
            total_weight += multiplier * diff_stats["count"]
        
        if total_weight > 0:
            weighted_score /= total_weight
        
        report = {
            "benchmark_name": benchmark.get("name", "Unknown"),
            "timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "scores": {
                "detection_score": detection_score,
                "fix_score": fix_score,
                "performance_score": performance_score,
                "total_score": total_score,
                "weighted_score": weighted_score
            },
            "results": [r.to_dict() for r in self.results],
            "recommendations": self._generate_recommendations(stats)
        }
        
        # Print summary
        self._print_report(report)
        
        # Save report
        self._save_report(report)
        
        return report
    
    def _generate_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on results"""
        recommendations = []
        
        if stats["success_rate"] < 0.7:
            recommendations.append("Improve bug detection algorithms for better coverage")
        
        if stats["fix_validation_rate"] < 0.6:
            recommendations.append("Enhance fix validation with more comprehensive testing")
        
        if stats["average_execution_time"] > 5.0:
            recommendations.append("Optimize healing agent for faster response times")
        
        if stats["by_difficulty"].get("hard", {}).get("success_rate", 1.0) < 0.5:
            recommendations.append("Focus on improving performance for complex test cases")
        
        if not recommendations:
            recommendations.append("System performs well across all metrics. Consider adding more diverse test cases.")
        
        return recommendations
    
    def _print_report(self, report: Dict[str, Any]):
        """Print formatted report"""
        print("\n" + "="*70)
        print("📈 BENCHMARK REPORT")
        print("="*70)
        
        stats = report["statistics"]
        scores = report["scores"]
        
        print(f"\n📊 Overall Statistics:")
        print(f"  Total Tests: {stats['total_tests']}")
        print(f"  Tests Passed: {stats['tests_passed']} ({stats['success_rate']:.1%})")
        print(f"  Fix Generation Rate: {stats['fix_generation_rate']:.1%}")
        print(f"  Fix Validation Rate: {stats['fix_validation_rate']:.1%}")
        print(f"  Average Improvement: {stats['average_improvement']:.1%}")
        print(f"  Avg Execution Time: {stats['average_execution_time']:.2f}s")
        
        print(f"\n🎯 Performance by Difficulty:")
        for diff, diff_stats in stats['by_difficulty'].items():
            print(f"  {diff.upper():7}: Success: {diff_stats['success_rate']:.1%} | "
                  f"Improvement: {diff_stats['avg_improvement']:.1%} | "
                  f"Time: {diff_stats['avg_time']:.2f}s")
        
        print(f"\n🏆 Scores:")
        print(f"  Detection:   {scores['detection_score']:.3f}")
        print(f"  Fix Quality: {scores['fix_score']:.3f}")
        print(f"  Performance: {scores['performance_score']:.3f}")
        print(f"  Total Score: {scores['total_score']:.3f}")
        print(f"  Weighted:    {scores['weighted_score']:.3f}")
        
        print(f"\n💡 Recommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
        
        print(f"\n📁 Report saved to: benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    def _save_report(self, report: Dict[str, Any]):
        """Save report to file"""
        filename = f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also save as markdown
        self._save_markdown_report(report, filename.replace('.json', '.md'))
    
    def _save_markdown_report(self, report: Dict[str, Any], filename: str):
        """Save report as markdown"""
        with open(filename, 'w') as f:
            f.write(f"# Benchmark Report: {report['benchmark_name']}\n\n")
            f.write(f"**Date**: {report['timestamp']}\n\n")
            
            stats = report['statistics']
            
            f.write("## Overall Statistics\n\n")
            f.write(f"- **Total Tests**: {stats['total_tests']}\n")
            f.write(f"- **Tests Passed**: {stats['tests_passed']} ({stats['success_rate']:.1%})\n")
            f.write(f"- **Fix Generation Rate**: {stats['fix_generation_rate']:.1%}\n")
            f.write(f"- **Fix Validation Rate**: {stats['fix_validation_rate']:.1%}\n")
            f.write(f"- **Average Improvement**: {stats['average_improvement']:.1%}\n")
            f.write(f"- **Average Execution Time**: {stats['average_execution_time']:.2f}s\n\n")
            
            f.write("## Performance by Difficulty\n\n")
            f.write("| Difficulty | Success Rate | Avg Improvement | Avg Time |\n")
            f.write("|------------|--------------|-----------------|----------|\n")
            for diff, diff_stats in stats['by_difficulty'].items():
                f.write(f"| {diff.upper()} | {diff_stats['success_rate']:.1%} | {diff_stats['avg_improvement']:.1%} | {diff_stats['avg_time']:.2f}s |\n")
            
            f.write("\n## Recommendations\n\n")
            for rec in report['recommendations']:
                f.write(f"- {rec}\n")

async def main():
    """Main function"""
    runner = BenchmarkRunner()
    await runner.run_benchmark()

if __name__ == "__main__":
    asyncio.run(main())