
import os
import asyncio
from typing import Optional, Dict, Any, List
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class QwenClient:
    """Main Qwen client for the self-healing agents project"""
    
    def __init__(self, model: str = None):
        self.hf_token = os.getenv("HF_TOKEN")
        if not self.hf_token:
            raise ValueError("HF_TOKEN not found in .env file")
            
        self.model = model or os.getenv("QWEN_MODEL", "Qwen/Qwen2.5-7B-Instruct")
        self.client = InferenceClient(model=self.model, token=self.hf_token)
        
        print(f"🤖 Qwen AI Activated: {self.model}")
    
    async def generate(self,
                      prompt: str,
                      system_prompt: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: int = 500,
                      **kwargs) -> str:
        """Generate text using Qwen"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            # Extract response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].message.content
            elif isinstance(response, dict) and 'choices' in response:
                content = response['choices'][0]['message']['content']
            else:
                content = str(response)
            
            # Clean markdown if present
            content = content.replace("```json", "").replace("```", "").strip()
            return content
            
        except Exception as e:
            raise Exception(f"Qwen API error: {str(e)}")
    
    async def generate_structured(self,
                               prompt: str,
                               output_format: Dict[str, Any],
                               **kwargs) -> Dict[str, Any]:
        """Generate structured JSON output"""
        
        format_str = json.dumps(output_format, indent=2)
        structured_prompt = f"""
        {prompt}
        
        Return the response in this exact JSON format:
        {format_str}
        
        Only return the JSON, no other text.
        """
        
        response = await self.generate(structured_prompt, **kwargs)
        
        try:
            import json
            return json.loads(response)
        except:
            return {"raw_response": response}
    
    async def check_health(self) -> bool:
        """Check if Qwen API is accessible"""
        try:
            test = await self.generate("Say OK", max_tokens=5)
            return "OK" in test.upper()
        except:
            return False
    
    async def batch_generate(self,
                           prompts: List[str],
                           **kwargs) -> List[str]:
        """Generate multiple responses"""
        tasks = [self.generate(prompt, **kwargs) for prompt in prompts]
        return await asyncio.gather(*tasks)