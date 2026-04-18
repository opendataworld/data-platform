# opendataworld data-platform

Umbrella repo for the `opendataworld` open-source data stack.
One `docker-compose.yml`, nine services, Compose **profiles** so you install only what you need.

## Stack

| Layer | Tool | Profile |
|---|---|---|
| Catalog | [OpenMetadata](https://github.com/opendataworld/OpenMetadata) | `catalog` |
| Ingestion | Airbyte | `ingest` |
| Entity resolution | Zingg | `resolve` |
| Semantic layer | Cube | `semantic` |
| Dashboards | Superset | `viz` |
| CDP | Unomi | `cdp` |
| Doc / vector / ops store | SurrealDB | `store` |
| Editorial knowledge graph | TerminusDB | `kg-edit` |
| Publishing knowledge graph | GraphDB Free | `kg-pub` |

Authentication is delegated to an **external Keycloak** at `auth.unboxd.cloud` (not installed here — clients are registered in that Keycloak and referenced by env var).

## Quick start

```bash
cp .env.example .env            # fill in real values (Keycloak client secrets, etc.)
docker compose --profile catalog up -d     # install OpenMetadata only
docker compose --profile catalog --profile ingest up -d   # add Airbyte
```

See [`docs/phase-plan.md`](docs/phase-plan.md) for the recommended install order.

## Profiles

Services are tagged with Compose profiles so nothing starts unless you opt in:

```yaml
services:
  openmetadata:
    profiles: ["catalog"]
  airbyte-server:
    profiles: ["ingest"]
```

Run multiple at once:

```bash
docker compose --profile catalog --profile store --profile ingest up -d
```

## Conventions

- All hosts/ports/secrets come from `.env` — nothing is hardcoded in compose files.
- Each service uses OIDC against the external Keycloak — per-service client ID/secret in `.env`.
- Data volumes are named (not bind-mounted) for portability.
- See each service's README upstream for tuning; this repo is deployment only, not forks.

## What this repo is not

- Not a fork of any upstream tool. Use the official images.
- Not a Kubernetes manifest set (Compose only, for now).
- Not where Keycloak itself is managed.
