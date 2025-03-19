"""
Main entry point for the OpenAI API compatibility demo.

Author: tj-scripts
Email: tangj1984@gmail.com
Date: 2024-03-21
"""

import asyncio
import sys
from typing import Optional, List
from .config import config, ConfigError
from .api.openai import OpenAIClient
from .models.chat import ChatSession
from .utils.logger import setup_logger

# Set up logging
logger = setup_logger(
    "tj.scripts",
    level=config.get("logging", "level", "INFO"),
    format=config.get("logging", "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    file=config.get("logging", "file", "app.log"),
    max_size=config.get("logging", "max_size", 10 * 1024 * 1024),  # 10MB
    backup_count=config.get("logging", "backup_count", 5)
)

def print_history(session: ChatSession) -> None:
    """
    Print the chat history.
    
    Args:
        session: Chat session instance
    """
    print("\n=== Chat History ===")
    for msg in session.messages:
        role = msg.role.capitalize()
        print(f"\n{role}: {msg.content}")
    print("\n===================")

async def chat_loop(client: OpenAIClient, session: ChatSession) -> None:
    """
    Run an interactive chat loop.
    
    Args:
        client: OpenAI API client
        session: Chat session instance
        
    Raises:
        Exception: If the API request fails
    """
    print("\nWelcome to the AI Chat! Type your message and press Enter to chat.")
    print("Commands:")
    print("  - 'quit': Exit the chat")
    print("  - 'clear': Clear chat history")
    print("  - 'history': Show chat history")
    print("  - 'help': Show this help message")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() == 'quit':
                print("\nGoodbye!")
                break
            elif user_input.lower() == 'clear':
                session.clear()
                print("\nChat history cleared.")
                continue
            elif user_input.lower() == 'history':
                print_history(session)
                continue
            elif user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  - 'quit': Exit the chat")
                print("  - 'clear': Clear chat history")
                print("  - 'history': Show chat history")
                print("  - 'help': Show this help message")
                continue
            elif not user_input:
                continue
            
            # Add user message to session
            session.add_message(
                role="user",
                content=user_input
            )
            
            # Send request
            print("\nAssistant is thinking...")
            response = await client.chat_completion(
                messages=session.get_messages(),
                temperature=session.temperature,
                max_tokens=session.max_tokens,
                stream=False
            )
            
            # Get and display assistant response
            assistant_message = response["choices"][0]["message"]["content"]
            print(f"\nAssistant: {assistant_message}")
            
            # Add assistant response to session
            session.add_message(
                role="assistant",
                content=assistant_message
            )
            
            # Log the exchange
            logger.info(f"User: {user_input}")
            logger.info(f"Assistant: {assistant_message}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error in chat loop: {str(e)}", exc_info=True)
            print(f"\nError: {str(e)}")
            print("Please try again or type 'quit' to exit.")

async def chat_example() -> None:
    """
    Run a chat completion example.
    
    Raises:
        ConfigError: If configuration is invalid
        Exception: If the API request fails
    """
    try:
        # Get OpenAI API configuration
        api_config = config.get_section("api").get("siliconflow", {})
        if not api_config:
            raise ConfigError("SiliconFlow API configuration not found")
        
        # Create OpenAI client
        client = OpenAIClient(api_config)
        
        # Create chat session
        session = ChatSession(
            temperature=api_config.get("temperature", 0.7),
            max_tokens=api_config.get("max_tokens", 2000)
        )
        
        # Add system message
        session.add_message(
            role="system",
            content="You are a helpful AI assistant."
        )
        
        # Run interactive chat loop
        await chat_loop(client, session)
        
    except ConfigError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error in chat example: {str(e)}", exc_info=True)
        raise

def main() -> Optional[int]:
    """
    Main entry point.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        logger.info("Starting OpenAI API demo...")
        asyncio.run(chat_example())
        logger.info("Demo completed successfully.")
        return 0
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user.")
        return 130
    except ConfigError as e:
        logger.error(f"Configuration error: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main() or 0) 