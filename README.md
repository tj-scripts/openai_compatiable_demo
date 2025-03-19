# OpenAI API Compatibility Demo

[English](README.md) | [中文](README_zh.md)

> Author: tj-scripts
> Email: tangj1984@gmail.com
> Date: 2024-03-21

A demonstration project showing how to build applications compatible with the OpenAI API specification, supporting both native OpenAI API and compatible API services.

## ✨ Features

- Support for OpenAI API and compatible API services
- Asynchronous API calls
- Interactive chat interface
- Chat history management
- Configurable logging system
- Type hints and documentation
- Error handling and retries

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/openai_compatiable_demo.git
cd openai_compatiable_demo
```

2. Create and activate Python virtual environment using uv:
```bash
# Create virtual environment
uv venv .venv --python=3.12

# Activate virtual environment
# Unix/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

3. Install dependencies:
```bash
# First install build tools
uv pip install hatchling

# Install package in editable mode
uv pip install -e .
```

If you encounter any issues during installation, please ensure:
- Python 3.12 or higher is installed
- uv is properly installed and added to system PATH
- Virtual environment is activated before running installation commands

## ⚙️ Configuration

1. Copy the example configuration file:
```bash
cp config.toml.example config.toml
```

2. Edit `config.toml` to set your API configuration:
```toml
[api.openai]
api_key = "your-openai-api-key"
base_url = "https://api.openai.com/v1"
model = "gpt-3.5-turbo"
temperature = 0.7
max_tokens = 2000
timeout = 30
stream = false
retry_count = 3
retry_delay = 1

[logging]
level = "INFO"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
file = "app.log"
max_size = 10485760  # 10MB
backup_count = 5
```

### 📝 Configuration Details

#### 🔑 API Configuration
- `api_key`: Your OpenAI API key
- `base_url`: API endpoint URL
- `model`: Model name to use
- `temperature`: Controls randomness (0.0 to 1.0)
- `max_tokens`: Maximum tokens to generate
- `timeout`: Request timeout in seconds
- `stream`: Enable streaming responses
- `retry_count`: Number of retries for failed requests
- `retry_delay`: Delay between retries in seconds

#### 📊 Logging Configuration
- `level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `format`: Log message format
- `file`: Log file path
- `max_size`: Maximum size of log file in bytes
- `backup_count`: Number of backup log files to keep

## 💬 Usage

### Interactive Chat

Run the interactive chat demo:
```bash
python -m tj.scripts.main
```

The chat interface supports the following commands:
- Type your message and press Enter to send
- `history`: Display chat history
- `clear`: Clear chat history
- `help`: Show available commands
- `quit`: Exit chat
- Press Ctrl+C to exit at any time

Chat session example:
```
Welcome to the AI Chat! Type your message and press Enter to chat.
Commands:
  - 'quit': Exit the chat
  - 'clear': Clear chat history
  - 'history': Show chat history
  - 'help': Show this help message

You: Hello, please introduce yourself.

Assistant: Hello! I'm an AI assistant that can help you with questions, coding, data analysis, and more...

You: Can you help me write a Python function?

Assistant: Of course! Please let me know what functionality you want to implement...

You: history

=== Chat History ===

System: You are a helpful AI assistant.

User: Hello, please introduce yourself.

Assistant: Hello! I'm an AI assistant that can help you with questions, coding, data analysis, and more...

User: Can you help me write a Python function?

Assistant: Of course! Please let me know what functionality you want to implement...

===================
```

## 🛠️ Development

1. Ensure Python 3.12 or higher is installed
2. Use virtual environment for development
3. Follow PEP 8 coding standards
4. Add type hints to all functions
5. Write docstrings for all modules, classes, and methods

### 🔧 Development Tools

The project includes several development tools configured in `pyproject.toml`:

- `black`: Code formatting
- `isort`: Import sorting
- `mypy`: Type checking
- `pytest`: Testing

To install development dependencies:
```bash
uv pip install -e ".[dev]"
```

## 🤝 Contributing

1. Fork this repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📄 License

[MIT License](LICENSE)