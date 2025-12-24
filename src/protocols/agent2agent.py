
import json
import time
import uuid
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    """Types of messages between agents"""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    HEAL = "heal"
    STATUS = "status"



class AgentStatus(Enum):
    """Agent status states"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    HEALING = "healing"



@dataclass
class AgentMessage:
    """Standard message format"""
    message_id: str
    sender_id: str
    receiver_id: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: float = None
    
    def __post_init__(self):
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = time.time()
    
    def to_dict(self):
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "message_type": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp
        }

# Simple exports
__all__ = ["MessageType", "AgentStatus", "AgentMessage"]
