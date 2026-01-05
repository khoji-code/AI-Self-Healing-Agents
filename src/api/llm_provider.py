"""
LLM Provider Abstraction Layer - FIXED VERSION
"""
import os
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass

class LLMProvider(Enum):
    """Supported LLM Providers"""
    QWEN = "qwen"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    LOCAL = "local"

@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 500

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    async def generate(self, 
                      prompt: str,
                      system_prompt: Optional[str] = None,
                      **kwargs) -> str:
        """Generate text from LLM"""
        pass
    
    @abstractmethod
    async def check_health(self) -> bool:
        """Check if LLM is accessible"""
        pass

class QwenClient(BaseLLMClient):
    """Qwen client implementation - FIXED"""
    
    def __init__(self, config: LLMConfig):
        from huggingface_hub import InferenceClient
        
        self.config = config
        if not config.api_key:
            config.api_key = os.getenv("HF_TOKEN")
        
        # FIX: Pass model to InferenceClient constructor
        self.client = InferenceClient(
            model=config.model if config.model else "Qwen/Qwen2.5-7B-Instruct",
            token=config.api_key
        )
        print(f"🤖 Qwen Client initialized with model: {config.model}")
    
    async def generate(self, 
                      prompt: str,
                      system_prompt: Optional[str] = None,
                      **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            # Try chat completion first
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                **kwargs
            )
            
            if hasattr(response, 'choices'):
                return response.choices[0].message.content
            elif isinstance(response, dict):
                return response['choices'][0]['message']['content']
            return str(response)
            
        except Exception as e:
            # Fallback to text generation
            print(f"Chat completion failed, trying text generation: {e}")
            try:
                full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:" if system_prompt else prompt
                response = self.client.text_generation(
                    prompt=full_prompt,
                    max_new_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    **kwargs
                )
                return response
            except Exception as e2:
                raise Exception(f"Qwen API error: {str(e)} - Fallback also failed: {str(e2)}")
    
    async def check_health(self) -> bool:
        try:
            test = await self.generate("Say OK", max_tokens=5)
            return "OK" in test.upper()
        except:
            return False

class OpenAIClient(BaseLLMClient):
    """OpenAI client implementation"""
    
    def __init__(self, config: LLMConfig):
        from openai import AsyncOpenAI
        
        self.config = config
        if not config.api_key:
            config.api_key = os.getenv("OPENAI_API_KEY")
        
        self.client = AsyncOpenAI(api_key=config.api_key)
    
    async def generate(self,
                      prompt: str,
                      system_prompt: Optional[str] = None,
                      **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    async def check_health(self) -> bool:
        try:
            await self.generate("Say OK", max_tokens=5)
            return True
        except:
            return False

class LLMFactory:
    """Factory for creating LLM clients"""
    
    @staticmethod
    def create_client(config: LLMConfig) -> BaseLLMClient:
        """Create LLM client based on provider"""
        if config.provider == LLMProvider.QWEN:
            return QwenClient(config)
        elif config.provider == LLMProvider.OPENAI:
            return OpenAIClient(config)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")
    
    @staticmethod
    def from_env() -> BaseLLMClient:
        """Create client from environment variables"""
        provider = os.getenv("LLM_PROVIDER", "qwen").lower()
        model = os.getenv("LLM_MODEL") or os.getenv("QWEN_MODEL", "Qwen/Qwen2.5-7B-Instruct")
        
        if provider == "qwen":
            config = LLMConfig(
                provider=LLMProvider.QWEN,
                model=model,
                api_key=os.getenv("HF_TOKEN")
            )
        elif provider == "openai":
            config = LLMConfig(
                provider=LLMProvider.OPENAI,
                model=model,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return LLMFactory.create_client(config)