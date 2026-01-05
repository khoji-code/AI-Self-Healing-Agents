"""
Mock LLM for testing without API calls
"""
import asyncio
import json
import random
from typing import Optional, Dict, Any, List

class MockLLM:
    """Mock LLM that returns realistic responses for testing"""
    
    def __init__(self):
        self.responses = {
            "diagnosis": {
                "root_cause": "API connection timeout due to network latency",
                "severity": "MEDIUM",
                "recommended_actions": ["Restart the service", "Check network configuration", "Increase timeout settings"],
                "confidence": 0.85
            },
            "healing_plan": """1. Restart the affected agent
2. Clear temporary cache and buffers
3. Verify network connectivity to dependencies
4. Implement exponential backoff for retries
5. Add monitoring for future occurrences

Expected recovery time: 2-5 minutes
Success probability: 95%""",
            "security_defense": """import re

def sanitize_input(input_str: str) -> str:
    \"\"\"Sanitize input to prevent SQL injection and XSS attacks\"\"\"
    # Remove SQL injection patterns
    sql_patterns = [
        r\"[';]\", r\"--\", r\"UNION\", r\"SELECT\", r\"INSERT\", 
        r\"UPDATE\", r\"DELETE\", r\"DROP\", r\"CREATE\"
    ]
    
    cleaned = input_str
    for pattern in sql_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Remove XSS patterns
    xss_patterns = [
        r\"<script>\", r\"</script>\", r\"javascript:\", 
        r\"onload=\", r\"onerror=\", r\"onclick=\"
    ]
    
    for pattern in xss_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # HTML encode special characters
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&#x27;",
        ">": "&gt;",
        "<": "&lt;",
    }
    
    for char, escape in html_escape_table.items():
        cleaned = cleaned.replace(char, escape)
    
    return cleaned""",
            "bug_fix": """def process_data_fixed(input_string: str):
    \"\"\"Process data with proper error handling and validation\"\"\"
    import json
    
    # Input validation
    if not input_string or not isinstance(input_string, str):
        raise ValueError("Input must be a non-empty string")
    
    try:
        if 'special_case_' in input_string:
            # Extract number and validate
            parts = input_string.split('_')
            if len(parts) > 1:
                try:
                    num = int(parts[-1])
                    if num == 0:
                        return {"error": "Cannot divide by zero", "alternative": 0}
                    return {"result": 100 / num, "processed": True}
                except ValueError:
                    return {"error": "Invalid number format", "processed": False}
        
        elif 'malformed_json' in input_string:
            # Try to parse JSON with error handling
            try:
                # Simulated JSON parsing
                parsed = json.loads('{"test": "data"}')
                return {"parsed": parsed, "valid": True}
            except json.JSONDecodeError as e:
                return {"error": f"JSON parsing failed: {str(e)}", "valid": False}
        
        elif 'large_dataset_' in input_string:
            # Process in chunks to avoid memory issues
            chunk_size = 1000
            total = 0
            for i in range(0, 1000000, chunk_size):
                chunk = list(range(i, min(i + chunk_size, 1000000)))
                total += len(chunk)
                # Simulate processing
            return {"total_processed": total, "method": "chunked"}
        
        else:
            return {"result": f"Processed: {input_string}", "status": "success"}
            
    except Exception as e:
        return {"error": str(e), "status": "failed"}"""
        }
        
        self.generic_responses = [
            "I've analyzed the issue and here's my recommendation...",
            "Based on the metrics provided, the system needs the following adjustments...",
            "The root cause appears to be related to resource constraints...",
            "Implementing these changes should resolve the issue within minutes...",
            "This is a common problem that can be fixed with proper configuration..."
        ]
    
    async def generate(self, 
                      prompt: str,
                      system_prompt: Optional[str] = None,
                      max_tokens: int = 500,
                      **kwargs) -> str:
        """Return mock responses based on prompt content"""
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate API delay
        
        prompt_lower = prompt.lower()
        
        # Return structured responses for specific queries
        if any(word in prompt_lower for word in ["diagnose", "root cause", "analysis"]):
            return json.dumps(self.responses["diagnosis"], indent=2)
        
        elif any(word in prompt_lower for word in ["healing", "plan", "procedure", "steps"]):
            return self.responses["healing_plan"]
        
        elif any(word in prompt_lower for word in ["security", "defense", "protect", "attack"]):
            return self.responses["security_defense"]
        
        elif any(word in prompt_lower for word in ["bug", "fix", "error", "correct", "regenerate"]):
            return self.responses["bug_fix"]
        
        elif any(word in prompt_lower for word in ["code", "function", "program"]):
            return """def example_function(input_data):
    \"\"\"Example function with proper error handling\"\"\"
    try:
        # Process input
        result = input_data.upper() if isinstance(input_data, str) else str(input_data)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}"""
        
        # Generic response
        else:
            response = random.choice(self.generic_responses)
            if len(prompt) > 20:
                response += f"\n\nSpecifically regarding '{prompt[:50]}...', I suggest implementing automated monitoring and retry logic."
            return response
    
    async def check_health(self) -> bool:
        return True
    
    async def generate_structured(self,
                               prompt: str,
                               output_format: Dict[str, Any],
                               **kwargs) -> Dict[str, Any]:
        """Generate structured JSON output"""
        
        # Generate a response
        response = await self.generate(prompt, **kwargs)
        
        try:
            # Try to parse as JSON
            return json.loads(response)
        except:
            # Return in requested format
            return {
                "analysis": response,
                "confidence": random.uniform(0.7, 0.95),
                "recommendations": ["Implement fix", "Monitor results", "Test thoroughly"],
                "timestamp": "2024-01-01T00:00:00Z"
            }