"""
Attack-Vulnerable Agent - For Scenario D
"""
import asyncio
import re
from typing import Dict, Any
from .base_agent import BaseAgent

class VulnerableAgent(BaseAgent):
    """Agent vulnerable to security attacks"""
    
    def __init__(self, agent_id: str = "vulnerable_agent"):
        super().__init__(agent_id, "vulnerable")
        
        # Track attack patterns
        self.attack_attempts = []
        self.security_measures = {
            "sql_injection": False,
            "xss": False,
            "path_traversal": False,
            "rate_limit": False
        }
        
        # Known attack patterns
        self.attack_patterns = {
            "sql_injection": [
                r".*([';]|(--)|(union)|(select)).*",
                r".*(drop|delete|insert|update).*",
                r".*(or\s+['1']=['1']).*"
            ],
            "xss": [
                r".*(<script>|javascript:|onload=).*",
                r".*(alert\(|document\.cookie).*"
            ],
            "path_traversal": [
                r".*(\.\./|\.\.\\).*",
                r".*(/etc/passwd|C:\\Windows).*"
            ],
            "brute_force": [
                r".*(admin|root).*",
                r".*(password|123456|qwerty).*"
            ]
        }
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process request with security vulnerabilities"""
        user_input = task.get("input", "")
        action = task.get("action", "echo")
        
        print(f"🔓 Processing: {user_input[:50]}...")
        
        # Check for attacks
        detected_attacks = self._detect_attacks(user_input)
        
        if detected_attacks:
            # Log attack attempt
            self.attack_attempts.append({
                "input": user_input[:100],
                "attacks": detected_attacks,
                "timestamp": asyncio.get_event_loop().time()
            })
            
            # Check if we're protected against these attacks
            unprotected_attacks = [
                attack for attack in detected_attacks 
                if not self.security_measures.get(attack, False)
            ]
            
            if unprotected_attacks:
                # Vulnerable - attack succeeds
                attack_type = unprotected_attacks[0]
                raise SecurityError(f"Security vulnerability exploited: {attack_type}")
            else:
                # Protected - attack blocked
                print(f"🛡️  Attack blocked: {detected_attacks}")
                return {
                    "result": "Attack blocked",
                    "protected": True,
                    "attacks_detected": detected_attacks
                }
        
        # Normal processing
        await asyncio.sleep(0.1)
        
        if action == "echo":
            return {"result": f"Echo: {user_input}"}
        elif action == "reverse":
            return {"result": user_input[::-1]}
        else:
            return {"result": f"Processed: {user_input}"}
    
    def _detect_attacks(self, input_str: str) -> list:
        """Detect security attacks in input"""
        detected = []
        
        for attack_type, patterns in self.attack_patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_str, re.IGNORECASE):
                    if attack_type not in detected:
                        detected.append(attack_type)
                    break
        
        return detected
    
    def add_security_measure(self, attack_type: str, measure_code: str):
        """Add security measure for specific attack type"""
        self.security_measures[attack_type] = {
            "code": measure_code,
            "applied": True,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        print(f"🛡️  Added security measure for {attack_type}")
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get security status"""
        protected = sum(1 for v in self.security_measures.values() if v)
        total = len(self.security_measures)
        
        return {
            "agent_id": self.agent_id,
            "attack_attempts": len(self.attack_attempts),
            "protected_attacks": protected,
            "total_attack_types": total,
            "protection_rate": protected / total if total > 0 else 0,
            "recent_attacks": self.attack_attempts[-5:] if self.attack_attempts else [],
            "security_measures": self.security_measures
        }

class SecurityError(Exception):
    """Security-related exception"""
    pass