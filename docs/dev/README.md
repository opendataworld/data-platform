# Developer Documentation

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourorg/data-platform.git
cd data-platform

# Start services
docker-compose up -d

# Run the orchestrator
cd orchestrator
pip install -r requirements.txt
python agent.py
```

## Architecture

### Components

1. **Orchestrator Agent** - LangGraph-powered agent with AutonomyX
2. **API Server** - FastAPI for REST endpoints
3. **MCP Server** - Model Context Protocol for AI integration
4. **LangFlow Components** - Visual workflow components
5. **Billing** - Lago integration for usage tracking

### Directory Structure

```
orchestrator/
├── agent.py           # Main LangGraph agent
├── api.py             # FastAPI server
├── billing.py         # Lago billing integration
├── autonomyx_agent.py # AutonomyX spec
├── mcp_services.py    # MCP server
├── unified_api.py     # Unified API
└── langflow_components/ # LangFlow components
    └── components.py
```

## Creating Custom Tools

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(param: str) -> dict:
    """My custom tool description."""
    # Your implementation
    return {"result": "success"}
```

## Adding Services to Registry

```python
# In agent.py
class ServiceRegistry:
    NEW_SERVICE = ["service1", "service2"]
```

## Billing Integration

```python
from billing import ServiceUsageTracker

tracker = ServiceUsageTracker()

# Track usage
tracker.track_usage("customer-123", "crawl.jina-reader", 100)

# Get billing summary
summary = tracker.get_customer_usage("customer-123")
```

## AutonomyX Agent Creation

```python
from agent import DataPlatformAgent

agent = DataPlatformAgent()

# Register with AutonomyX
agent.register_with_autonomyx(
    name="my-agent",
    sponsor_id="user-001",
    tenant_id="tenant-001"
)
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| LLM_MODEL | Default LLM model |
| OLLAMA_URL | Ollama server URL |
| LAGO_URL | Lago billing URL |
| LAGO_API_KEY | Lago API key |