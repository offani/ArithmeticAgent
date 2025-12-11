# Math Agent Assistant with Streamlit

A conversational AI agent that performs basic arithmetic operations using LangChain agents and Groq LLM, with a beautiful Streamlit interface.

## Features

- **🔧 Arithmetic Operations**: Add, subtract, multiply, and divide numbers using dedicated tools
- **🤖 Intelligent Agent**: Uses LangChain's agent framework with tool calling
- **💬 Natural Conversation**: Responds warmly to greetings and politely declines non-arithmetic queries
- **📊 Intermediate Steps**: View tool calls and results in a collapsible expander
- **⚡ Streaming Responses**: Real-time streaming from backend to frontend
- **🎨 Interactive UI**: Built with Streamlit for a smooth user experience
- **🐳 Docker Ready**: Easy deployment with Docker

## Tech Stack

- **LangChain**: Agent orchestration and tool management
- **Groq**: Fast LLM inference with llama-3.3-70b-versatile
- **Streamlit**: Web UI framework
- **UV**: Fast Python package installer
- **Docker**: Containerization for easy deployment

## Installation

### Using UV (Recommended)

```bash
# Clone the repository then 
cd Arithmetic

# Install dependencies
uv sync

# Run the application
uv run streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Using Docker

```bash
# Build the Docker image
docker build -t math-agent-app .

# Run the container
docker run -p 8501:8501 math-agent-app
```

Access the app at `http://localhost:8501`

## Project Structure

```
mysampleagent/
├── app.py                 # Main Streamlit application
├── pyproject.toml        # Project dependencies
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore file
└── README.md             # This file
```


## How It Works

1. **User Input**: Enter a query in the chat interface
2. **Agent Processing**: The agent analyzes the query and decides whether to use tools
3. **Tool Execution**: If arithmetic is needed, the agent calls the appropriate tools (add, subtract, multiply, divide)
4. **Streaming Response**: Tool calls, results, and final answers stream to the UI in real-time
5. **Display**: Intermediate steps show in a collapsible expander, final answer displays prominently



## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for learning and development.

## Acknowledgments

- **LangChain**: For the amazing agent framework
- **Groq**: For fast LLM inference
- **Streamlit**: For the beautiful UI framework
- **UV**: For blazingly fast package management
