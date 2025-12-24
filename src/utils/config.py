
import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class SystemConfig:
    """System configuration"""
    
    # Qwen AI Configuration
    hf_token: str = os.getenv("HF_TOKEN", "")
    qwen_model: str = os.getenv("QWEN_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    
    # Agent Configuration
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
    healing_threshold: float = float(os.getenv("HEALING_THRESHOLD", "0.7"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # System Configuration
    enable_monitoring: bool = os.getenv("ENABLE_MONITORING", "true").lower() == "true"
    enable_healing: bool = os.getenv("ENABLE_HEALING", "true").lower() == "true"
    max_agents: int = int(os.getenv("MAX_AGENTS", "10"))
    
    def validate(self):
        """Validate configuration"""
        if not self.hf_token:
            raise ValueError("HF_TOKEN is required in .env file")
        
        if not self.hf_token.startswith("hf_"):
            print("⚠️  Warning: HF_TOKEN doesn't start with 'hf_' - may be invalid")
    
    @classmethod
    def load(cls):
        """Load and validate configuration"""
        config = cls()
        config.validate()
        return config
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "qwen_model": self.qwen_model,
            "max_retries": self.max_retries,
            "healing_threshold": self.healing_threshold,
            "log_level": self.log_level,
            "enable_monitoring": self.enable_monitoring,
            "enable_healing": self.enable_healing,
            "max_agents": self.max_agents
        }