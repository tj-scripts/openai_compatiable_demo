"""
Gradio UI interface for OpenAI API compatibility demo.

Author: tj-scripts
Email: tangj1984@gmail.com
Date: 2024-03-21
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import gradio as gr
from .models.chat import ChatSession
from .config import config
from .utils.logger import setup_logger
from .api.openai import OpenAIClient

# Set up logging
logger = setup_logger(
    "tj.scripts",
    level=config.get("logging", "level", "INFO"),
    format=config.get("logging", "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    file=config.get("logging", "file", "app.log"),
    max_size=config.get("logging", "max_size", 10 * 1024 * 1024),  # 10MB
    backup_count=config.get("logging", "backup_count", 5)
)

# 获取资源目录路径
RESOURCE_DIR = Path(__file__).parent.parent / "resources"
AVATAR_DIR = RESOURCE_DIR / "avatars"

# 确保头像目录存在
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

# 默认头像路径
USER_AVATAR = str(AVATAR_DIR / "user.png")
ASSISTANT_AVATAR = str(AVATAR_DIR / "assistant.png")

class ChatUI:
    """Chat UI class for managing the Gradio interface."""

    def __init__(self) -> None:
        """Initialize the chat UI."""
        try:
            self.chat_session: Optional[ChatSession] = None
            self.client: Optional[OpenAIClient] = None
            self.history: List[Tuple[str, str]] = []  # 修改为元组列表
            self.is_initialized = False
            logger.info("Chat UI initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chat UI: {e}")
            raise

    async def initialize_chat(self) -> None:
        """Initialize the chat session."""
        if self.is_initialized:
            return

        try:
            # 获取 API 配置
            api_config = config.get_section("api").get("siliconflow", {})
            if not api_config:
                raise ValueError("SiliconFlow API configuration not found")
            
            # 创建 OpenAI 客户端
            self.client = OpenAIClient(api_config)
            
            # 创建聊天会话
            self.chat_session = ChatSession(
                temperature=api_config.get("temperature", 0.7),
                max_tokens=api_config.get("max_tokens", 2000)
            )
            
            # 添加系统消息
            self.chat_session.add_message(
                role="system",
                content="You are a helpful AI assistant."
            )
            
            # 添加欢迎消息
            welcome_message = (
                "Welcome to the AI Chat! I'm here to help you with any questions or tasks you have.\n\n"
                "Features:\n"
                "- Interactive chat interface\n"
                "- Chat history management\n"
                "- Configurable parameters\n"
                "- Error handling and retries\n\n"
                "Feel free to start chatting!"
            )
            
            # 添加助手的欢迎消息到历史记录
            self.history.append(("", welcome_message))
            
            self.is_initialized = True
            logger.info("Chat session initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize chat session: {e}")
            self.is_initialized = False
            raise

    async def send_message(
        self,
        message: str,
        history: List[Tuple[str, str]],  # 修改为元组列表
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Tuple[List[Tuple[str, str]], str]:  # 修改为元组列表
        """Send a message and get the response.

        Args:
            message: The message to send
            history: The chat history as list of (user_message, assistant_message) tuples
            temperature: The temperature for response generation
            max_tokens: The maximum number of tokens to generate

        Returns:
            Tuple containing:
            - The updated chat history as list of (user_message, assistant_message) tuples
            - Empty string to clear input
        """
        if not message.strip():
            return history, ""

        try:
            if not self.is_initialized:
                await self.initialize_chat()

            if not self.chat_session or not self.client:
                raise ValueError("Chat session or client not initialized")

            # 更新聊天参数
            self.chat_session.temperature = temperature
            self.chat_session.max_tokens = max_tokens

            # 添加用户消息
            self.chat_session.add_message(
                role="user",
                content=message
            )

            # 发送请求
            response = await self.client.chat_completion(
                messages=self.chat_session.get_messages(),
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )

            # 获取助手回复
            assistant_message = response["choices"][0]["message"]["content"]

            # 添加助手回复
            self.chat_session.add_message(
                role="assistant",
                content=assistant_message
            )

            # 更新历史记录
            history.append((message, assistant_message))

            # 记录日志
            logger.info(f"User: {message}")
            logger.info(f"Assistant: {assistant_message}")

            return history, ""
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(f"Error sending message: {e}")
            history.append((message, error_msg))  # 使用元组而不是字典
            return history, ""

    def clear_history(self) -> List[Tuple[str, str]]:  # 修改为元组列表
        """Clear the chat history.

        Returns:
            Empty chat history as list of (user_message, assistant_message) tuples
        """
        if self.chat_session:
            self.chat_session.clear()
            # 重新添加系统消息
            self.chat_session.add_message(
                role="system",
                content="You are a helpful AI assistant."
            )
        self.history = []
        logger.info("Chat history cleared")
        return []

    def create_ui(self) -> gr.Blocks:
        """Create the Gradio UI interface.

        Returns:
            The Gradio interface
        """
        with gr.Blocks(title="OpenAI API Chat Demo", theme=gr.themes.Soft()) as interface:
            gr.Markdown(
                """
                # 🤖 OpenAI API Chat Demo
                
                A demonstration of OpenAI API compatibility with interactive chat interface.
                
                ## Features
                - Support for OpenAI API and compatible services
                - Interactive chat interface
                - Chat history management
                - Configurable parameters
                - Error handling and retries
                """
            )

            with gr.Row():
                with gr.Column(scale=4):
                    chatbot = gr.Chatbot(
                        [],  # 初始化为空列表
                        elem_id="chatbot",
                        bubble_full_width=False,
                        avatar_images=(USER_AVATAR, ASSISTANT_AVATAR),  # 使用实际图片文件
                        height=350,
                        show_label=False,
                    )
                    with gr.Row():
                        txt = gr.Textbox(
                            show_label=False,
                            placeholder="Type your message here...",
                            container=False,
                            lines=3,
                            max_lines=5,
                        )
                        submit_btn = gr.Button("Send", variant="primary")

                with gr.Column(scale=1):
                    with gr.Accordion("Parameters", open=False):
                        temperature = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=0.7,
                            step=0.1,
                            label="Temperature",
                            info="Controls randomness in the response",
                        )
                        max_tokens = gr.Slider(
                            minimum=100,
                            maximum=4000,
                            value=2000,
                            step=100,
                            label="Max Tokens",
                            info="Maximum number of tokens to generate",
                        )
                    with gr.Row():
                        clear_btn = gr.Button("Clear History", variant="secondary")
                        retry_btn = gr.Button("Retry Last Message", variant="secondary")

            # Event handlers
            submit_btn.click(
                self.send_message,
                [txt, chatbot, temperature, max_tokens],
                [chatbot, txt],
            )

            clear_btn.click(self.clear_history, None, [chatbot])

            # Enter key submission (Shift+Enter for new line)
            txt.submit(
                self.send_message,
                [txt, chatbot, temperature, max_tokens],
                [chatbot, txt],
            )

        return interface

def main() -> None:
    """Main entry point for the UI application."""
    try:
        chat_ui = ChatUI()
        interface = chat_ui.create_ui()
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            favicon_path="🤖",  # 使用 emoji 作为网站图标
        )
    except Exception as e:
        logger.error(f"Failed to start UI: {e}")
        raise

if __name__ == "__main__":
    main() 