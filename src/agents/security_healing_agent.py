"""
Security Healing Agent - For Scenario D
"""
import re
import hashlib
import time
from typing import Dict, Any, Optional
from .code_healing_agent import CodeHealingAgent

class SecurityHealingAgent(CodeHealingAgent):
    """Healing agent for security attack detection and hardening"""
    
    def __init__(self,
                 agent_id: str = "security_guard",
                 config: Optional[Dict[str, Any]] = None,
                 llm_config: Optional[Any] = None):
        
        super().__init__(agent_id, config, llm_config)
        
        # Security-specific tracking
        self.attack_defenses = {}
        self.security_patches = {}
        self.threat_intelligence = {}
        
        # Known security patterns
        self.known_threats = {
            "sql_injection": {
                "description": "SQL injection attacks",
                "severity": "CRITICAL",
                "defense": "Parameterized queries, input validation"
            },
            "xss": {
                "description": "Cross-site scripting attacks",
                "severity": "HIGH",
                "defense": "Output encoding, CSP headers"
            },
            "path_traversal": {
                "description": "Path traversal attacks",
                "severity": "HIGH",
                "defense": "Path validation, sandboxing"
            },
            "brute_force": {
                "description": "Brute force attacks",
                "severity": "MEDIUM",
                "defense": "Rate limiting, account lockout"
            }
        }
        
        print(f"🛡️  Security Healing Agent Activated: {self.agent_id}")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process security healing requests"""
        request_type = task.get("type", "analyze_attack")
        
        if request_type == "analyze_attack":
            return await self.analyze_security_attack(task)
        elif request_type == "generate_defense":
            return await self.generate_security_defense(task)
        elif request_type == "harden_agent":
            return await self.harden_agent_security(task)
        else:
            return await super().process(task)
    
    async def analyze_security_attack(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security attack and generate defense"""
        attack_input = task.get("attack_input", "")
        attack_type = task.get("attack_type", "unknown")
        vulnerable_code = task.get("vulnerable_code", "")
        
        print(f"🚨 Analyzing security attack: {attack_type}")
        print(f"💥 Attack input: {attack_input[:50]}...")
        
        # Check if we already have defense
        attack_hash = self._hash_attack_pattern(attack_input)
        
        if attack_hash in self.attack_defenses:
            print(f"🔄 Using existing defense for attack pattern")
            return {
                "success": True,
                "action": "apply_existing_defense",
                "attack_hash": attack_hash,
                "defense": self.attack_defenses[attack_hash]
            }
        
        # Generate new defense using LLM
        print(f"🤖 Generating security defense using {self.llm.__class__.__name__}...")
        
        threat_info = self.known_threats.get(attack_type, {})
        
        prompt = f"""
        SECURITY ATTACK ANALYSIS AND DEFENSE GENERATION
        
        Attack Type: {attack_type}
        Attack Description: {threat_info.get('description', 'Unknown')}
        Severity: {threat_info.get('severity', 'UNKNOWN')}
        
        Attack Input: {attack_input}
        Vulnerable Code: {vulnerable_code}
        
        Requirements:
        1. Analyze how this attack exploits the vulnerability
        2. Suggest security measures to prevent it
        3. Generate secure code that fixes the vulnerability
        4. Include input validation and sanitization
        
        Return as JSON with: analysis, defense_strategy, secure_code
        """
        
        try:
            response = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are a senior security engineer fixing vulnerabilities.",
                max_tokens=1000
            )
            
            # Parse response
            try:
                import json
                security_analysis = json.loads(response)
            except:
                security_analysis = {"raw_response": response}
            
            # Store defense
            self.attack_defenses[attack_hash] = {
                "analysis": security_analysis,
                "attack_type": attack_type,
                "attack_input": attack_input[:100],
                "generated_at": self._current_timestamp(),
                "threat_info": threat_info
            }
            
            # Update threat intelligence
            if attack_type not in self.threat_intelligence:
                self.threat_intelligence[attack_type] = {
                    "first_seen": self._current_timestamp(),
                    "occurrences": 0,
                    "defenses_generated": 0
                }
            
            self.threat_intelligence[attack_type]["occurrences"] += 1
            self.threat_intelligence[attack_type]["defenses_generated"] += 1
            
            return {
                "success": True,
                "action": "generated_new_defense",
                "attack_hash": attack_hash,
                "analysis": security_analysis,
                "message": f"Generated defense for {attack_type} attack"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Security analysis failed: {str(e)}"
            }
    
    async def generate_security_defense(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific security defense code"""
        attack_type = task.get("attack_type", "")
        vulnerability = task.get("vulnerability", "")
        code_context = task.get("code_context", "")
        
        prompt = f"""
        GENERATE SECURITY DEFENSE CODE
        
        Attack Type: {attack_type}
        Vulnerability: {vulnerability}
        
        Code Context:
        {code_context}
        
        Generate Python code that:
        1. Prevents {attack_type} attacks
        2. Validates and sanitizes input
        3. Includes proper error handling
        4. Follows security best practices
        
        Return only the security defense code.
        """
        
        try:
            defense_code = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are generating security defense code.",
                max_tokens=600
            )
            
            # Store security patch
            patch_id = f"patch_{hashlib.md5(defense_code.encode()).hexdigest()[:8]}"
            self.security_patches[patch_id] = {
                "attack_type": attack_type,
                "defense_code": defense_code,
                "vulnerability": vulnerability,
                "generated_at": self._current_timestamp()
            }
            
            return {
                "success": True,
                "patch_id": patch_id,
                "defense_code": defense_code,
                "attack_type": attack_type,
                "message": f"Generated defense for {attack_type}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Defense generation failed: {str(e)}"
            }
    
    async def harden_agent_security(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Harden agent against multiple attack types"""
        agent_id = task.get("agent_id", "")
        attack_types = task.get("attack_types", [])
        current_code = task.get("current_code", "")
        
        print(f"🛡️  Hardening agent {agent_id} against {len(attack_types)} attack types")
        
        all_defenses = []
        
        for attack_type in attack_types:
            # Generate defense for each attack type
            defense = await self.generate_security_defense({
                "attack_type": attack_type,
                "vulnerability": f"Vulnerable to {attack_type}",
                "code_context": current_code
            })
            
            if defense['success']:
                all_defenses.append({
                    "attack_type": attack_type,
                    "patch_id": defense['patch_id'],
                    "defense_code": defense['defense_code']
                })
        
        # Generate hardened code
        if all_defenses:
            hardened_code = await self._generate_hardened_code(current_code, all_defenses)
            
            return {
                "success": True,
                "agent_id": agent_id,
                "hardened_code": hardened_code,
                "applied_defenses": all_defenses,
                "defense_count": len(all_defenses),
                "message": f"Hardened agent against {len(all_defenses)} attack types"
            }
        else:
            return {
                "success": False,
                "error": "No defenses generated"
            }
    
    async def _generate_hardened_code(self, original_code: str, defenses: list) -> str:
        """Generate hardened code with all defenses"""
        
        defenses_summary = "\n".join([
            f"- {d['attack_type']}: {d['patch_id']}" for d in defenses
        ])
        
        prompt = f"""
        GENERATE HARDENED SECURITY CODE
        
        Original Code:
        {original_code}
        
        Security Defenses to Integrate:
        {defenses_summary}
        
        Defense Code:
        {self._format_defenses(defenses)}
        
        Generate a single hardened version that:
        1. Integrates all security defenses
        2. Maintains original functionality
        3. Adds comprehensive input validation
        4. Includes security monitoring
        5. Follows secure coding practices
        
        Return the complete hardened code.
        """
        
        hardened_code = await self.llm.generate(
            prompt=prompt,
            system_prompt="You are creating security-hardened code.",
            max_tokens=1500
        )
        
        return hardened_code
    
    def _hash_attack_pattern(self, attack_input: str) -> str:
        """Create hash for attack pattern"""
        # Extract pattern features
        patterns = []
        
        # SQL injection patterns
        if re.search(r"([';]|(--)|(union)|(select))", attack_input, re.IGNORECASE):
            patterns.append("sql")
        
        # XSS patterns
        if re.search(r"(<script>|javascript:|onload=)", attack_input, re.IGNORECASE):
            patterns.append("xss")
        
        # Path traversal
        if re.search(r"(\.\./|\.\.\\)", attack_input):
            patterns.append("path")
        
        # Create hash
        if patterns:
            pattern_str = "_".join(sorted(patterns))
            return hashlib.md5(pattern_str.encode()).hexdigest()[:8]
        else:
            return hashlib.md5(attack_input.encode()).hexdigest()[:8]
    
    def _format_defenses(self, defenses):
        """Format defenses for prompt"""
        formatted = []
        for defense in defenses:
            formatted.append(f"\n=== Defense for {defense['attack_type']} ===")
            formatted.append(defense['defense_code'])
        return "\n".join(formatted)
    
    def get_security_report(self) -> Dict[str, Any]:
        """Get security healing report"""
        return {
            "agent_id": self.agent_id,
            "attack_defenses": len(self.attack_defenses),
            "security_patches": len(self.security_patches),
            "threat_intelligence": self.threat_intelligence,
            "known_threats": list(self.known_threats.keys()),
            "protection_level": len(self.attack_defenses) / len(self.known_threats) if self.known_threats else 0
        }
    
    def _current_timestamp(self):
        return time.time()