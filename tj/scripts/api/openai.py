"""
OpenAI API client implementation.

Author: tj-scripts
Email: tangj1984@gmail.com
Date: 2024-03-21
"""

import asyncio
import aiohttp
from typing import Dict, Any, Optional, List, Union
from .base import BaseAPIClient

class OpenAIClient(BaseAPIClient):
    """OpenAI API client implementation"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the OpenAI API client.
        
        Args:
            config: Configuration dictionary containing API settings
        """
        super().__init__(config)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(
        self,
        url: str,
        payload: Dict[str, Any],
        retry_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with retry logic.
        
        Args:
            url: API endpoint URL
            payload: Request payload
            retry_count: Number of retries remaining
            
        Returns:
            API response dictionary
            
        Raises:
            Exception: If the API request fails after all retries
        """
        retry_count = retry_count if retry_count is not None else self.retry_count
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                ) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                        if retry_count > 0:
                            await asyncio.sleep(self.retry_delay)
                            return await self._make_request(url, payload, retry_count - 1)
                        raise Exception(f"API request failed: {error_msg}")
                    return await response.json()
        except aiohttp.ClientError as e:
            if retry_count > 0:
                await asyncio.sleep(self.retry_delay)
                return await self._make_request(url, payload, retry_count - 1)
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            if retry_count > 0:
                await asyncio.sleep(self.retry_delay)
                return await self._make_request(url, payload, retry_count - 1)
            raise Exception(f"Unexpected error: {str(e)}")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat completion API endpoint.
        
        Args:
            messages: List of message dictionaries
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional arguments to pass to the API
            
        Returns:
            API response dictionary
        """
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.config.get("temperature", 0.7),
            "max_tokens": max_tokens or self.config.get("max_tokens", 2000),
            "stream": stream,
            **kwargs
        }
        
        return await self._make_request(url, payload)
    
    async def completion(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Text completion API endpoint.
        
        Args:
            prompt: Input text prompt
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional arguments to pass to the API
            
        Returns:
            API response dictionary
        """
        url = f"{self.base_url}/completions"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature or self.config.get("temperature", 0.7),
            "max_tokens": max_tokens or self.config.get("max_tokens", 2000),
            "stream": stream,
            **kwargs
        }
        
        return await self._make_request(url, payload) 