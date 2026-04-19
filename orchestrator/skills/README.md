# Data Platform Skills

Skills aligned with IBM Data Management Guide for the data platform orchestrator.

## Available Skills

### 1. Data Quality (`data-quality`)
Validates data accuracy, completeness, consistency, uniqueness, and timeliness.

**Tools**: great-expectations, soda-core, ydata-profiling

**Use cases**:
- Validate data against schemas
- Generate data quality reports
- Check for duplicates
- Verify data freshness

### 2. Data Governance (`data-governance`)
Manages data policies, standards, and access control.

**Tools**: datahub, atlas, collibra, openmetadata, marquez

**Use cases**:
- Track data lineage
- Manage data assets
- Apply access policies
- Audit data usage

### 3. Data Ingestion (`data-ingest`)
Crawls and extracts data from various sources.

**Tools**: firecrawl, crawl4ai, playwright, jina-reader, trafilatura, grobid

**Use cases**:
- Crawl websites
- Extract PDF content
- Parse documents
- Scrape dynamic content

### 4. Data Embedding (`data-embed`)
Creates embeddings for semantic search.

**Tools**: sentence-transformers, bge, e5, word2vec, fasttext

**Use cases**:
- Semantic search
- Similarity finding
- RAG applications

### 5. Data Orchestration (`data-orchestrate`)
Orchestrates data pipelines.

**Tools**: airflow, dagster, prefect, temporal

**Use cases**:
- Schedule pipelines
- Manage dependencies
- Handle failures

### 6. Data Streaming (`data-stream`)
Processes data in real-time.

**Tools**: kafka, redpanda

**Use cases**:
- Event processing
- Real-time analytics
- Change data capture

### 7. Data Transfer (`data-transfer`)
Moves data between systems.

**Tools**: rclone, airbyte, meltano, debezium

**Use cases**:
- Cloud migration
- CDC replication
- ETL pipelines

### 8. Data Integration (`data-integrate`)
Combines data from multiple sources.

**Tools**: trino, duckdb, apache-pinot

**Use cases**:
- Cross-source queries
- Federated analytics
- Data virtualization

### 9. NLP Processing (`nlp-process`)
Processes text for entities and PII.

**Tools**: spacy-ner, presidio, flair

**Use cases**:
- Entity extraction
- PII detection
- Text classification

### 10. Image AI (`image-ai`)
Processes images and generates embeddings.

**Tools**: timm, clip, sam, blip, yolo

**Use cases**:
- Image classification
- Object detection
- Image captioning

### 11. Speech AI (`speech-ai`)
Transcribes and generates speech.

**Tools**: whisper, faster-whisper, coqui-stt

**Use cases**:
- Audio transcription
- Speaker diarization

### 12. LLM Operations (`llm-ops`)
Query and manage LLMs.

**Tools**: ollama, gpt4all, text-generation-webui

**Use cases**:
- Text generation
- Chat completion
- Fine-tuning

### 13. Workflow Automation (`workflow`)
Low-code/no-code workflow builders.

**Tools**: langflow, n8n, flowise, chainlit

**Use cases**:
- Visual workflows
- Chatbot building
- Automation

## Integration with Agent, LangFlow & MCP

### Agent (Preloaded)

The agent **automatically** has access to all skills and MCP tools at startup:

```python
# agent.py - Already configured
AGENT_TOOLS = create_data_management_tools()  # 20+ tools preloaded
SKILLS = load_skills()  # All 13 skills loaded
MCP_TOOLS = create_mcp_server()  # All MCP tools available
```

**What's available:**
- 20+ data management tools (crawl, embed, validate, etc.)
- 13 skills (data-quality, data-governance, etc.)
- MCP protocol for external integrations

For example, when you ask:
```
"Crawl website and validate the data"
```
The agent automatically uses `data-ingest` skill + `data-quality` tool.

### LangFlow Integration

Skills are also exposed as LangFlow components:

```python
from agent import DataPlatformAgent

agent = DataPlatformAgent()

# Agent will automatically select appropriate skill
result = await agent.run("Crawl website and extract entities")
# → Uses: data-ingest + nlp-process

result = await agent.run("Validate this CSV file")
# → Uses: data-quality
```

### LangFlow Integration

Skills are exposed as LangFlow components:

1. Open https://flow.open-data.world
2. Drag skill component to canvas
3. Configure inputs/outputs
4. Connect to other components

### MCP Integration

Skills are available via MCP protocol:

```python
from mcp import Client

client = Client("https://api.open-data.world/mcp")

# List available skills
skills = client.list_tools()

# Execute a skill
result = client.execute("data_quality_check", {
    "source": "s3://bucket/data.csv"
})
```

## Skill Metadata

- **Version**: 1.0.0
- **Platform**: Data Platform Stack
- **IBM Guide**: https://www.ibm.com/think/topics/data-management-guide
- **AutonomyX**: Certified agent tools