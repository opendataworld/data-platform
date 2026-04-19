# LangFlow + Orchestrator (Production Setup)

This repository is set up so LangFlow can call platform tools through the Orchestrator API, and the orchestrator can deploy services on demand using Docker Compose profiles.

## Architecture

```text
LangFlow Agent
  -> Orchestrator API (/agent, /tools, /services)
    -> Tool layer (crawl/embed/chunk/ocr/metadata/graph/db)
    -> Deployment layer (docker_deploy/docker_stop/docker_status)
      -> docker compose profiles in docker-compose.yml
```

## Service Tool Coverage

The orchestrator exposes tools aligned to the platform services and profiles:

| Profile | Core services | Typical tools |
|---|---|---|
| `crawl` | firecrawl, crawl4ai, playwright, searxng | `crawl_url`, `docker_deploy` |
| `ingest` | airbyte + crawl services | `crawl_url`, `transfer_data` |
| `store` | postgres, surrealdb | `execute_query`, `docker_deploy` |
| `catalog` | openmetadata | `register_dataset`, `search_metadata` |
| `semantic` | cube | `integrate_data`, `query_llm` |
| `viz` | superset | `orchestrate_workflow` |
| `kg-edit` | terminusdb, jena | `create_entity`, `create_relationship` |
| `kg-pub` | graphdb, jena | `query_graph` |
| `resolve` | zingg | `run_clustering`, `validate_data` |

See `orchestrator/deployment.py` for deploy/stop/status tools and profile/service mapping.

## LangFlow Wiring

1. In LangFlow, add an HTTP/API tool node pointing to the orchestrator:
   - Base URL: `https://api.open-data.world`
   - Main endpoint: `POST /agent`
2. Pass the user prompt as `user_input`.
3. Add policy in your system prompt for deployment orchestration:
   - If a requested capability is not available, call deployment tool first.
   - After deployment, call the task-specific tool.

## Production Checklist

- Use HTTPS endpoints behind Caddy/Traefik.
- Restrict CORS allow-list in `orchestrator/api.py` for production domains.
- Keep secrets in environment variables only.
- Add monitoring around `/health`, `/services`, and deployment tools.
- Pin container image tags where possible for deterministic releases.

## Link Validation for Landing Page

To validate links declared in `landing/index.html`:

```bash
python landing/check_links.py
```

If running inside a restricted network, run with a public base URL from an environment that has outbound internet access.
