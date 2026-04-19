FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy application code
COPY *.py .
COPY chat_ui.html .
COPY langflow_components/ ./langflow_components/
COPY skills/ ./skills/

# Create data directories
RUN mkdir -p /data/models /data/logs

# Expose ports
EXPOSE 8000 11434 11433

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start Ollama in background and then run the agent
CMD ollama serve & \
    sleep 10 && \
    python agent.py
