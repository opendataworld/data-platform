# Chat API

## Overview

The Data Platform Agent is exposed as a chat API - you can converse with it using natural language.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Chat with the agent |
| GET | `/chat/sessions` | List chat sessions |
| GET | `/chat/sessions/{id}/history` | Get session history |
| DELETE | `/chat/sessions/{id}` | Delete session |

## Chat with Agent

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Crawl example.com and validate the data"
  }'
```

Response:
```json
{
  "response": "I'll crawl example.com and validate the data...",
  "session_id": "default",
  "tools_used": ["data_ingest", "data_quality"],
  "services_deployed": []
}
```

## Session Management

### Create new session
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "session_id": "my-session"
  }'
```

### Get history
```bash
curl http://localhost:8000/chat/sessions/my-session/history
```

## Example Conversations

| User Message | Agent Action |
|--------------|--------------|
| "Crawl example.com" | Uses data-ingest tool |
| "Validate this data" | Uses data-quality tool |
| "Embed this text" | Uses data-embed tool |
| "Create embeddings for these docs" | Deploys embeddings service |
| "Query with Llama3" | Deploys Ollama if needed |

## Web UI

For a simple web UI, you can use Chainlit:

```bash
cd orchestrator
chainlit run chat.py --port 8000
```

Or access via LangFlow at https://flow.open-data.world