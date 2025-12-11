
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim


WORKDIR /app


COPY pyproject.toml ./


RUN uv pip install --system --no-cache-dir -r pyproject.toml


COPY app.py ./
COPY main.py ./
COPY README.md ./

EXPOSE 8501


ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false


HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1


CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
