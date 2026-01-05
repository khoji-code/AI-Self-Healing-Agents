"""
Buggy Data Processor Agent - For Scenario C
"""
import asyncio
import re
from typing import Dict, Any
from .base_agent import BaseAgent

class BuggyDataProcessor(BaseAgent):
    """Data processor with bugs that occur for specific inputs"""
    
    def __init__(self, agent_id: str = "buggy_processor"):
        super().__init__(agent_id, "buggy_processor")
        
        # Track problematic inputs
        self.problematic_inputs = []
        self.bug_fixes = {}  # Store fixes for specific patterns
        
        # Known bugs (simulated)
        self.known_bugs = [
            {
                "pattern": r"special_case_\d+",
                "description": "Causes division by zero for special_case_* inputs",
                "fix": "Add validation check before division"
            },
            {
                "pattern": r"malformed_json",
                "description": "Causes JSON parsing error for malformed_json inputs",
                "fix": "Add try-catch around JSON parsing"
            },
            {
                "pattern": r"large_dataset_\d+",
                "description": "Causes memory overflow for large_dataset_* inputs",
                "fix": "Implement chunked processing"
            }
        ]
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process data with simulated bugs"""
        data = task.get("data", "")
        operation = task.get("operation", "process")
        
        print(f"🔧 Processing: {data[:30]}...")
        
        # Check if this input triggers known bugs
        bug_triggered = False
        triggered_bug = None
        
        for bug in self.known_bugs:
            if re.search(bug["pattern"], data):
                bug_triggered = True
                triggered_bug = bug
                break
        
        if bug_triggered:
            # Simulate the bug
            await asyncio.sleep(0.2)
            
            if "special_case_" in data:
                # Division by zero bug
                raise ZeroDivisionError(f"Division by zero for input: {data}")
            elif "malformed_json" in data:
                # JSON parsing bug
                raise ValueError(f"JSON parsing error for: {data}")
            elif "large_dataset_" in data:
                # Memory error bug
                raise MemoryError(f"Memory overflow processing: {data}")
        else:
            # Normal processing
            await asyncio.sleep(0.1)
            
            if operation == "reverse":
                return {"result": data[::-1]}
            elif operation == "uppercase":
                return {"result": data.upper()}
            elif operation == "count":
                return {"result": len(data)}
            else:
                return {"result": f"Processed: {data}"}
        
        return {"result": "Should not reach here"}
    
    def add_bug_fix(self, pattern: str, fix_code: str):
        """Add a bug fix for a specific pattern"""
        self.bug_fixes[pattern] = {
            "fix_code": fix_code,
            "applied": False,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Also update known bugs
        for bug in self.known_bugs:
            if bug["pattern"] == pattern:
                bug["fixed"] = True
                bug["fix_code"] = fix_code
                break
    
    def has_bug_fix(self, pattern: str) -> bool:
        """Check if bug fix exists for pattern"""
        return pattern in self.bug_fixes
    
    async def apply_bug_fix(self, pattern: str, input_data: str) -> Dict[str, Any]:
        """Apply bug fix for specific input"""
        if pattern not in self.bug_fixes:
            return {"success": False, "error": "No fix available"}
        
        fix = self.bug_fixes[pattern]
        
        print(f"🔧 Applying bug fix for pattern: {pattern}")
        print(f"📝 Fix: {fix['fix_code'][:100]}...")
        
        # Simulate applying fix
        await asyncio.sleep(0.3)
        
        # Apply the fix (in real system, this would modify the code)
        fix["applied"] = True
        
        # Now process with fix applied
        try:
            # Modified processing logic for this pattern
            if "special_case_" in pattern:
                # Fixed version: add validation
                if "0" in input_data:
                    return {"result": "Fixed: Validation added, division skipped"}
                return {"result": "Fixed: Processed with validation"}
            
            elif "malformed_json" in pattern:
                # Fixed version: try-catch added
                return {"result": "Fixed: JSON parsing with error handling"}
            
            elif "large_dataset_" in pattern:
                # Fixed version: chunked processing
                return {"result": "Fixed: Processing in chunks"}
            
            return {"result": f"Fixed processing for {input_data}"}
            
        except Exception as e:
            return {"success": False, "error": f"Fix application failed: {str(e)}"}