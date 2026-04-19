# LangFlow Integration Guide

## Custom Components Available

The Data Platform includes custom LangFlow components that connect to all platform services.

### Components Installed

| Component | Description |
|-----------|-------------|
| Crawl URL | Web crawling with Jina Reader, Firecrawl |
| Embed Text | Sentence Transformers, BGE, E5 embeddings |
| Chunk Text | Text chunking (recursive, semantic) |
| OCR Image | Tesseract, EasyOCR image to text |
| Transcribe Audio | Whisper, Faster-Whisper speech to text |
| Query LLM | Ollama, GPT4All LLM queries |
| Data Quality | Great Expectations validation |
| Extract Entities | spaCy NER entity extraction |
| Detect PII | Presidio PII detection |
| Workflow Trigger | Airflow, Prefect workflow triggers |
| Service Registry | Browse available services |

## Using Components in LangFlow

### 1. Access LangFlow
```
https://flow.open-data.world
```

### 2. Components Location
After installing, components appear in:
- **Custom Components** tab in the component sidebar

### 3. Install Custom Components

```bash
# Copy components to LangFlow custom components directory
cp -r langflow_components ~/.langflow/components/

# Or use the LangFlow UI to load components
```

### 4. Build Workflows

Example: Crawl → Embed → Query LLM

```
[Crawl URL] → [Chunk Text] → [Embed Text] → [Query LLM] → [Chat Output]
```

## Agent Component

The Data Platform Agent is also available as a LangFlow component:

```
[DataPlatform Agent]
  - Input: User prompt
  - Tools: All 20+ tools available
  - Output: Agent response
```

## Service Connection

Each component connects to services via:

1. **Environment Variables** - Set in `.env`
2. **Service URLs** - Default to internal Docker network
3. **API Keys** - For external services (OpenAI, etc.)

## Troubleshooting

### Components not showing?
```bash
# Restart LangFlow after adding components
docker-compose restart langflow
```

### Service connection errors?
- Check service is running: `docker-compose ps`
- Check environment variables in `.env`
- Verify network connectivity between containers