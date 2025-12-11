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
# Clone the repository
cd mysampleagent

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
├── main.py               # CLI test script
├── pyproject.toml        # Project dependencies
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore file
└── README.md             # This file
```

## Usage

### Example Queries

**Arithmetic Operations:**
- "Add 10 and 10, then subtract 5 from it and multiply by 4." → Result: 60
- "What is 2 + 2 * 3 - 4 / 2?" → Result: 6
- "Divide 100 by 5 and then multiply the result by 3"
- "Calculate (15 + 7) * 4 - 12 / 3"

**Greetings:**
- "Hello" → Warm greeting response
- "Hi there" → Friendly response
- "Hey" → Casual greeting

**Non-Arithmetic Queries:**
- "What's the weather?" → Politely declines and suggests arithmetic questions
- "Tell me a joke" → Redirects to arithmetic operations

## How It Works

1. **User Input**: Enter a query in the chat interface
2. **Agent Processing**: The agent analyzes the query and decides whether to use tools
3. **Tool Execution**: If arithmetic is needed, the agent calls the appropriate tools (add, subtract, multiply, divide)
4. **Streaming Response**: Tool calls, results, and final answers stream to the UI in real-time
5. **Display**: Intermediate steps show in a collapsible expander, final answer displays prominently

## Configuration

### Environment Variables

You can set these environment variables or modify them in the code:

- `GROQ_API_KEY`: Your Groq API key (currently hardcoded, should be moved to env var for production)
- `STREAMLIT_SERVER_PORT`: Port for Streamlit (default: 8501)

### Customization

**Add More Tools:**
```python
@tool
def power(a: float, b: float) -> float:
    """Raise a to the power of b."""
    return a ** b

# Add to tools list in initialize_agent()
tools = [add, subtract, multiply, divide, power]
```

**Change LLM Model:**
```python
llm = ChatGroq(
    model_name="mixtral-8x7b-32768",  # Different model
    temperature=0.5,
    # ... other params
)
```

## Testing

Run the CLI test script to verify functionality:

```bash
uv run python main.py
```

This runs three test cases:
1. Complex arithmetic: "Add 10 and 10, then subtract 5 from it and multiply by 4."
2. Greeting: "Hello"
3. Math expression: "What is 2 + 2 * 3 - 4 / 2?"

## Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t math-agent-app .

# Run the container
docker run -d -p 8501:8501 --name math-agent math-agent-app

# View logs
docker logs -f math-agent

# Stop the container
docker stop math-agent

# Remove the container
docker rm math-agent
```

### Docker Compose (Optional)

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  math-agent:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```



## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for learning and development.

## Acknowledgments

- **LangChain**: For the amazing agent framework
- **Groq**: For fast LLM inference
- **Streamlit**: For the beautiful UI framework
- **UV**: For blazingly fast package management
