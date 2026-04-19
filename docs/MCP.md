## LangFlow + MCP Integration

## Overview

The Data Platform includes:

1. **LangFlow** - Built-in agent, components
2. **MCP Server** - Preloaded tools
3. **Skills** - Preloaded for agent

## What's Included

### 1. LangFlow Built-in Agent

LangFlow already has a powerful agent component built-in:

```
LangFlow Agent Component:
├── Input: User message
├── Tools: Any LangFlow components
├── Memory: Conversation history
└── Output: Response
```

**Usage in LangFlow:**
1. Open LangFlow: https://flow.open-data.world
2. Drag "Agent" component to canvas
3. Configure tools (Crawl, Embed, LLM, etc.)
4. Connect to Chat components

### 2. MCP Server (Model Context Protocol)

The platform includes an MCP server at `http://api.open-data.world:8000/mcp`:

```
MCP Server Endpoints:
├── /mcp/tools         - List available tools (20+)
├── /mcp/execute        - Execute a tool
├── /mcp/agents         - List agents
└── /mcp/sessions      - Manage sessions
```

### 3. Custom Components

Our custom components integrate with the platform:

```
Custom Components:
├── CrawlUrlComponent     → jina-reader, firecrawl
├── EmbedTextComponent   → sentence-transformers, bge
├── ChunkTextComponent   → recursive, semantic
├── OCRImageComponent    → tesseract, easyocr
├── TranscribeAudio      → whisper, faster-whisper
├── QueryLLMComponent    → ollama, gpt4all
├── DataQualityComponent → great-expectations
└── ExtractEntities     → spacy-ner, presidio
```

## Preloaded in Agent

The agent automatically has all skills and MCP tools available at startup:

- 20+ data management tools
- 13 skills (IBM Data Management Guide aligned)
- MCP protocol for external integrations

## Connecting External AI to LangFlow

### Claude / ChatGPT Integration

```python
# Use LangFlow as API from external AI
import requests

# Get LangFlow flow ID
FLOWS_URL = "https://flow.open-data.world/api/v1/flows"

# Run flow
response = requests.post(
    "https://flow.open-data.world/api/v1/predict",
    json={
        "flow_id": "your-flow-id",
        "inputs": {"text": "Your input"}
    }
)
```

### MCP Client Connection

```python
# Connect MCP client to platform
from mcp import Client

client = Client("https://api.open-data.world/mcp")

# List tools
tools = client.list_tools()

# Execute tool
result = client.execute("crawl_url", {"url": "https://example.com"})
```

## Service URLs

| Service | URL |
|---------|-----|
| LangFlow | https://flow.open-data.world |
| LangFlow API | https://flow.open-data.world/api/v1 |
| MCP Server | https://api.open-data.world/mcp |

## Pre-built Flows

Import these flows in LangFlow:

### RAG Pipeline
```
Crawl URL → Chunk Text → Embed Text → Vector Store → Query LLM → Response
```

### Data Quality
```
Load Data → Great Expectations → Validate → Report
```

### Entity Extraction
```
Input Text → Extract Entities → Detect PII → Anonymize → Output