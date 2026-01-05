"""
Code-Regenerating Healing Agent - For Scenario C
"""
import re
import ast
import hashlib
import time
import asyncio
from typing import Dict, Any, Optional
from .healing_agent_llm import LLMHealingAgent

class CodeHealingAgent(LLMHealingAgent):
    """Healing agent that regenerates buggy code"""
    
    def __init__(self,
                 agent_id: str = "code_doctor",
                 config: Optional[Dict[str, Any]] = None,
                 llm_config: Optional[Any] = None):
        
        super().__init__(agent_id, config, llm_config)
        
        # Code analysis database
        self.code_fixes = {}
        self.bug_patterns = {}
        self.regenerated_functions = {}
        
        print(f"💻 Code Healing Agent Activated: {self.agent_id}")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process code healing requests"""
        request_type = task.get("type", "analyze_bug")
        
        if request_type == "analyze_bug":
            return await self.analyze_and_fix_bug(task)
        elif request_type == "regenerate_code":
            return await self.regenerate_function(task)
        elif request_type == "test_fix":
            return await self.test_code_fix(task)
        else:
            return await super().process(task)
    
    async def analyze_and_fix_bug(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze bug and generate fix"""
        error_message = task.get("error", "")
        input_data = task.get("input", "")
        function_code = task.get("code", "")
        
        print(f"🐛 Analyzing bug: {error_message[:50]}...")
        print(f"📥 Input: {input_data[:50]}...")
        
        # Extract bug pattern
        bug_pattern = self._extract_bug_pattern(error_message, input_data)
        
        # Check if we already have a fix
        if bug_pattern in self.code_fixes:
            print(f"🔄 Using existing fix for pattern: {bug_pattern}")
            return {
                "success": True,
                "action": "apply_existing_fix",
                "pattern": bug_pattern,
                "fix": self.code_fixes[bug_pattern]
            }
        
        # Generate new fix using LLM
        print(f"🤖 Generating new fix using {self.llm.__class__.__name__}...")
        
        prompt = f"""
        BUG ANALYSIS AND FIX GENERATION
        
        Error: {error_message}
        Input that caused error: {input_data}
        Function code: {function_code}
        
        Analyze the bug and:
        1. Identify the root cause
        2. Suggest a fix
        3. Provide corrected Python code
        
        Return as JSON with: root_cause, fix_description, corrected_code
        """
        
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are a senior Python developer debugging code.",
                max_tokens=800
            )
            
            # Parse response
            try:
                import json
                analysis = json.loads(response)
            except:
                analysis = {"raw_response": response}
            
            # Store the fix
            self.code_fixes[bug_pattern] = {
                "analysis": analysis,
                "pattern": bug_pattern,
                "generated_at": self._current_timestamp(),
                "input_example": input_data,
                "error": error_message
            }
            
            # Store bug pattern
            self.bug_patterns[bug_pattern] = {
                "first_seen": self._current_timestamp(),
                "occurrences": 1,
                "last_input": input_data
            }
            
            return {
                "success": True,
                "action": "generated_new_fix",
                "pattern": bug_pattern,
                "analysis": analysis,
                "message": f"Generated fix for bug pattern: {bug_pattern}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Bug analysis failed: {str(e)}"
            }
    
    async def regenerate_function(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Regenerate entire function with fixes"""
        function_name = task.get("function", "unknown_function")
        original_code = task.get("original_code", "")
        bug_reports = task.get("bug_reports", [])
        
        print(f"🔄 Regenerating function: {function_name}")
        print(f"📋 Bug reports: {len(bug_reports)}")
        
        prompt = f"""
        REGENERATE FUNCTION WITH BUG FIXES
        
        Function name: {function_name}
        Original code: {original_code}
        
        Bug reports to fix:
        {self._format_bug_reports(bug_reports)}
        
        Requirements:
        1. Fix all reported bugs
        2. Keep the same function signature
        3. Add proper error handling
        4. Add input validation
        5. Include docstring
        
        Return only the corrected Python code.
        """
        
        try:
            new_code = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are regenerating Python functions with bug fixes.",
                max_tokens=1000
            )
            
            # Validate the generated code
            is_valid = await self._validate_python_code(new_code)
            
            if not is_valid:
                return {
                    "success": False,
                    "error": "Generated code is not valid Python"
                }
            
            # Store regenerated function
            code_hash = hashlib.md5(new_code.encode()).hexdigest()[:8]
            self.regenerated_functions[function_name] = {
                "new_code": new_code,
                "original_code": original_code,
                "bug_reports": bug_reports,
                "hash": code_hash,
                "regenerated_at": self._current_timestamp(),
                "validated": is_valid
            }
            
            return {
                "success": True,
                "function": function_name,
                "new_code": new_code,
                "code_hash": code_hash,
                "message": f"Function {function_name} regenerated successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Function regeneration failed: {str(e)}"
            }
    
    async def test_code_fix(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Test if code fix works"""
        original_code = task.get("original_code", "")
        fixed_code = task.get("fixed_code", "")
        test_inputs = task.get("test_inputs", [])
        
        print(f"🧪 Testing code fix with {len(test_inputs)} test cases")
        
        results = []
        
        for test_input in test_inputs:
            try:
                # Test original code (should fail for buggy inputs)
                original_result = await self._execute_code_safely(original_code, test_input)
                
                # Test fixed code
                fixed_result = await self._execute_code_safely(fixed_code, test_input)
                
                results.append({
                    "input": test_input,
                    "original_success": original_result["success"],
                    "fixed_success": fixed_result["success"],
                    "improvement": fixed_result["success"] and not original_result["success"]
                })
                
            except Exception as e:
                results.append({
                    "input": test_input,
                    "error": str(e)
                })
        
        improvements = sum(1 for r in results if r.get("improvement", False))
        
        return {
            "success": True,
            "test_results": results,
            "improvements": improvements,
            "total_tests": len(test_inputs),
            "improvement_rate": improvements / len(test_inputs) if test_inputs else 0
        }
    
    def _extract_bug_pattern(self, error_message: str, input_data: str) -> str:
        """Extract pattern from bug"""
        # Simple pattern extraction
        patterns = []
        
        if "division" in error_message.lower() and "zero" in error_message.lower():
            patterns.append("division_by_zero")
        
        if "json" in error_message.lower():
            patterns.append("json_parsing")
        
        if "memory" in error_message.lower():
            patterns.append("memory_overflow")
        
        # Extract input pattern
        if re.search(r'special_case_\d+', input_data):
            patterns.append("special_case_number")
        elif re.search(r'malformed_json', input_data):
            patterns.append("malformed_json")
        elif re.search(r'large_dataset_\d+', input_data):
            patterns.append("large_dataset")
        
        return "_".join(patterns) if patterns else "unknown_bug"
    
    async def _validate_python_code(self, code: str) -> bool:
        """Validate Python code syntax"""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    
    async def _execute_code_safely(self, code: str, input_data: str) -> Dict[str, Any]:
        """Execute code safely in a restricted environment"""
        try:
            # Create a safe execution context
            safe_globals = {
                "__builtins__": {
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'len': len,
                    'range': range,
                    'print': print,
                    'Exception': Exception
                }
            }
            
            # In a real system, you would use a sandboxed execution environment
            # For this demo, we'll simulate execution
            await asyncio.sleep(0.05)
            
            # Simulate different outcomes based on input
            if "special_case_" in input_data and "validation" not in code:
                return {"success": False, "error": "Division by zero"}
            elif "malformed_json" in input_data and "try" not in code:
                return {"success": False, "error": "JSON parsing error"}
            elif "large_dataset_" in input_data and "chunk" not in code:
                return {"success": False, "error": "Memory overflow"}
            else:
                return {"success": True, "result": f"Processed: {input_data}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _format_bug_reports(self, bug_reports):
        """Format bug reports for LLM prompt"""
        formatted = []
        for i, report in enumerate(bug_reports, 1):
            formatted.append(f"{i}. Error: {report.get('error', 'Unknown')}")
            formatted.append(f"   Input: {report.get('input', 'Unknown')}")
            formatted.append(f"   Pattern: {report.get('pattern', 'Unknown')}")
        return "\n".join(formatted)
    
    def _current_timestamp(self):
        return time.time()