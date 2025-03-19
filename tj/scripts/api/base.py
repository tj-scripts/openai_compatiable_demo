"""
Base API client implementation.

Author: tj-scripts
Email: tangj1984@gmail.com
Date: 2024-03-21
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union

class BaseAPIClient(ABC):
    """Base API client class"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the API client.
        
        Args:
            config: Configuration dictionary containing API settings
        """
        self.config = config
        self.base_url = config.get("base_url", "")
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "")
        self.timeout = config.get("timeout", 30)
        self.retry_count = config.get("retry_count", 3)
        self.retry_delay = config.get("retry_delay", 1)
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass 