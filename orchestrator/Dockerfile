FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    git curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy app files
COPY *.py .
COPY chat_ui.html .
COPY langflow_components/ ./langflow_components/
COPY skills/ ./skills/

# Create data dirs
RUN mkdir -p /data/models /data/logs

# Run API server
CMD ["python", "api.py"]
