# Phase plan

Recommended install order. Each phase is gated on the previous one working.
Run only what you need — nothing about the stack forces all-or-nothing.

## Phase 0 — Auth prerequisites (external, no install here)

Before installing any service, register OIDC clients in Keycloak at `auth.unboxd.cloud`, realm `opendataworld`:

| Client ID | For service | Redirect URI |
|---|---|---|
| `openmetadata` | OpenMetadata | `https://<om-host>/callback` |
| `airbyte` | Airbyte | `https://<ab-host>/auth/callback` |
| `superset` | Superset | `https://<ss-host>/oauth-authorized/keycloak` |
| `unomi` | Unomi (via oauth2-proxy) | `https://<un-host>/oauth2/callback` |

Drop each client's secret into `.env`.

## Phase 1 — Catalog

```bash
docker compose --profile catalog up -d
```

**Why first:** Everything else you install after this gets cataloged automatically. Lineage/discovery is worth more the earlier it starts.

## Phase 2 — Storage foundations

```bash
docker compose --profile store --profile kg-edit --profile kg-pub up -d
```

SurrealDB + TerminusDB + GraphDB. Destinations must exist before ingestion.

## Phase 3 — Ingestion

```bash
docker compose --profile ingest up -d
```

Airbyte connects to the stores from phase 2 as destinations.

## Phase 4 — Entity resolution

```bash
docker compose --profile resolve up -d
```

Zingg runs on ingested raw data to produce golden entities.

## Phase 5 — Semantic + viz

```bash
docker compose --profile semantic --profile viz up -d
```

Cube models metrics on golden data; Superset dashboards.

## Phase 6 — CDP

```bash
docker compose --profile cdp up -d
```

Unomi captures events; feeds back into ingestion. Last because it depends on a working warehouse.

## Rollback

Compose profiles are additive, not destructive. To stop a phase:

```bash
docker compose --profile <name> down
```

Data volumes persist; removing them is manual (`docker volume rm opendataworld_<name>`).
