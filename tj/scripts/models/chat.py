"""
Chat models and data structures.

Author: tj-scripts
Email: tangj1984@gmail.com
Date: 2024-03-21
"""

from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field

@dataclass
class Message:
    """Chat message data structure"""
    role: Literal["system", "user", "assistant", "function"]
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None

@dataclass
class ChatSession:
    """Chat session management"""
    messages: List[Message] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 2000
    
    def add_message(
        self,
        role: Literal["system", "user", "assistant", "function"],
        content: str,
        name: Optional[str] = None,
        function_call: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a message to the chat session.
        
        Args:
            role: Message role (system, user, assistant, or function)
            content: Message content
            name: Optional name for the message sender
            function_call: Optional function call data
        """
        self.messages.append(Message(role=role, content=content, name=name, function_call=function_call))
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages in the session.
        
        Returns:
            List of message dictionaries
        """
        return [
            {
                "role": msg.role,
                "content": msg.content,
                **({"name": msg.name} if msg.name else {}),
                **({"function_call": msg.function_call} if msg.function_call else {})
            }
            for msg in self.messages
        ]
    
    def clear(self) -> None:
        """Clear all messages from the session."""
        self.messages.clear() 