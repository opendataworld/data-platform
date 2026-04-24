# Docker Compose Profiles

## Document metadata

- **Repository:** `opendataworld/data-platform`
- **Canonical implementation path:** `docker-compose.yml`
- **Related docs:** [`docs/phase-plan.md`](phase-plan.md), [`docs/platform-overview.md`](platform-overview.md), [`docs/module-map.md`](module-map.md)
- **Document owner role:** technical writer / platform maintainer
- **Last major revision:** 2026-04-24
- **Revision note:** Aligned with `openautonomyx/common-instructions` technical-writer guidance for source-of-truth repository Markdown, stable sections, explicit scope, assumptions, implementation references, rationale, and changelog notes.

## Purpose

This page documents the Docker Compose profiles used by `opendataworld/data-platform`.

The compose file is the implementation source of truth. This document explains how the profiles are intended to be used, why they are grouped this way, and what needs to stay aligned when the compose configuration changes.

## Scope

### In scope

- Operational meaning of Compose profiles in `docker-compose.yml`.
- Recommended startup sequence for local/dev and staged platform assembly.
- Known naming differences between product capability language and operational profile names.
- Production-readiness notes for scaffolded services.
- Maintenance rules for keeping docs aligned with implementation.

### Out of scope

- Full service-by-service hardening instructions.
- Production deployment runbooks.
- Secret-management implementation details.
- External Keycloak lifecycle ownership.
- AgentNxt AI Platform product scope.
- Claims that future lineage, feature-store, or registry repos already exist.

## Assumptions

- Operators run services through Docker Compose profiles rather than starting the entire stack by default.
- `.env` contains required non-secret defaults, while real secrets are injected through approved secret-management workflows.
- `docker-compose.yml` may include scaffolded services that require additional backing dependencies, credentials, or hardening before production use.
- Profile names are operational startup groups and may not map one-to-one to platform product capability names.

## Current state

`opendataworld/data-platform` is an umbrella integration workspace. Most services are guarded by Compose profiles so teams can start only the slice they need.

The current profile model supports:

- staged rollout through catalog, storage, ingestion, resolution, semantic, visualization, and CDP phases;
- optional supporting capabilities such as SSO, crawling, labeling, feedback, search, testing, knowledge graph editing/publishing, and ML/AI utilities;
- scaffolded integrations that may need additional production dependencies before full deployment.

## Decision rationale

Profiles are used to keep the umbrella repo practical while avoiding premature repo sprawl.

This approach:

- lets teams run narrow product slices during development;
- keeps implementation and architecture reviewable in one repo;
- allows OSS services to be integrated before custom platform code is written;
- makes current state, next state, and future architecture intent explicit;
- supports staged hardening without claiming that every scaffolded service is production-ready.

## Profile reference

| Profile | Purpose | Primary services / examples |
|---|---|---|
| `sso` | Shared SSO gateway support | `oauth2-proxy` |
| `catalog` | Metadata catalog and governance foundation | `openmetadata` |
| `ingest` | Data ingestion, acquisition, crawling helpers, and enrichment utilities | `airbyte`, `firecrawl`, `crawl4ai`, `iab-taxonomy`, `g2-api`, `google-search-console`, `maps`, `opennlp`, plus selected ML/enrichment utilities |
| `crawl` | Web crawling, browser automation, search-adjacent collection, and content extraction | `firecrawl`, `crawl4ai`, `playwright`, `searxng`, `wikidata`, `wikipedia-topics`, selected OCR/computer-vision utilities |
| `store` | Core storage foundations | `postgres`, `surrealdb`, selected taxonomy data loaders |
| `kg-edit` | Knowledge graph authoring/editing path | `terminusdb`, `jena` |
| `kg-pub` | Knowledge graph publication/query path | `graphdb`, `jena`, `wikidata`, `wikipedia-topics` |
| `resolve` | Entity resolution workflows | `zingg` |
| `semantic` | Semantic modeling and metrics serving | `cube` |
| `viz` | Dashboards and visualization | `superset` |
| `cdp` | Customer/event data platform path | `unomi` |
| `label` | Human labeling and annotation | `labelstudio`, `argilla` |
| `feedback` | Feedback and review loops | `argilla` |
| `search` | Search and discovery support | `searxng`, `google-search-console` |
| `test` | Test and browser automation support | `playwright` |
| `ml` | ML/AI utilities used by ingestion, enrichment, OCR, speech, vision, LLM, clustering, and embedding workflows | TensorFlow Serving, YOLO, OCR tools, Whisper variants, Ollama, GPT4All, embedding/topic utilities, and other scaffolded ML services |

## Recommended rollout sequence

Use the phase plan for the canonical install order:

1. External auth prerequisites: configure required OIDC clients and secrets.
2. `catalog`: start catalog/discovery early so downstream assets can be registered.
3. `store`, `kg-edit`, `kg-pub`: bring storage and knowledge graph destinations online.
4. `ingest`: connect ingestion and acquisition workflows.
5. `resolve`: run entity resolution after raw data exists.
6. `semantic`, `viz`: add metrics models and dashboards.
7. `cdp`: add event capture after the destination and warehouse path is working.

## Common commands

### List profiles

```bash
docker compose config --profiles
```

### Start a single profile

```bash
docker compose --profile catalog up -d
```

### Start multiple profiles

```bash
docker compose --profile store --profile kg-edit --profile kg-pub up -d
```

### Preview services for a profile

```bash
docker compose --profile ingest config
```

### Stop services for a profile

```bash
docker compose --profile ingest down
```

## Example startup paths

### Minimal storage foundation

```bash
docker compose --profile store up -d
```

Starts core storage services such as Postgres and SurrealDB.

### Catalog-first setup

```bash
docker compose --profile catalog up -d
```

Starts the catalog foundation. Some catalog services still require production dependency wiring, such as database/search backing services, before a hardened deployment.

### Knowledge graph foundation

```bash
docker compose --profile kg-edit --profile kg-pub up -d
```

Starts the editable and publishable knowledge graph paths, including TerminusDB, GraphDB, and Jena where configured.

### Ingestion and crawling setup

```bash
docker compose --profile ingest --profile crawl up -d
```

Starts ingestion and crawling-related services. Some services are scaffolded clients or helpers and require credentials in `.env` before they perform useful work.

### Semantic and visualization setup

```bash
docker compose --profile semantic --profile viz up -d
```

Starts Cube and Superset for semantic modeling and dashboards after data destinations are available.

## Profile naming guidance

The architecture docs use product capability names such as `catalog`, `lineage`, `ingestion`, `resolution`, `semantic`, `visualization`, `graph`, `store`, `labeling`, `features`, `search`, `docs`, and future `registries`.

Compose profile names are operational startup groups. They do not always map one-to-one to product capability names:

- `kg-edit` and `kg-pub` implement graph-related operational paths.
- `crawl` is a supporting acquisition profile under ingestion/search workflows.
- `ml` contains utility services that support enrichment and extraction, but this repo remains the OpenDataWorld Data Platform, not the AgentNxt AI Platform.
- Lineage and feature-store capabilities are architectural directions and should be added as explicit profile/service paths only when they are integrated in compose.

## Production-readiness notes

Several services are intentionally scaffolded and include TODO comments in `docker-compose.yml`. Before treating a profile as production-ready:

- confirm all required backing services are defined and healthy;
- confirm `.env` templates declare required configuration keys;
- confirm real secrets are not committed to git;
- confirm external credentials and approved secret-management paths are configured;
- verify OIDC clients and redirect URIs for protected services;
- prefer immutable image tags for release-bound deployments;
- run `docker compose --profile <profile> config` to validate the rendered configuration;
- update this document whenever profiles or service memberships change.

## Documentation maintenance rule

When changing `docker-compose.yml`, update this page in the same change if any of the following change:

- a profile is added, renamed, or removed;
- a major service moves between profiles;
- the recommended startup sequence changes;
- a scaffolded service becomes production-ready, or a production-ready service becomes scaffold-only;
- an implementation path, dependency, or external interface changes.

## Open questions

- Should lineage become an explicit Compose profile when Marquez is fully wired?
- Should feature-store support become an explicit Compose profile when Feast is integrated?
- Which scaffolded ML/enrichment services are intended for long-term support versus temporary experimentation?
- Which profiles require separate production runbooks before release use?

## Follow-up tasks

- Add or update `.env.example` coverage for every variable referenced by active services.
- Run `docker compose config --profiles` after compose changes and compare the output with this page.
- Create production runbooks for profiles that graduate beyond scaffold status.
- Record reviewer feedback and recurring documentation gaps in a follow-up review note.

## Changelog

### 2026-04-24

- Reworked this page against `openautonomyx/common-instructions` technical-writer guidance.
- Added document metadata, scope, assumptions, decision rationale, open questions, follow-up tasks, and changelog sections.
- Kept `docker-compose.yml` as the named implementation source of truth.
- Preserved operational profile reference and command examples while making scaffold and production-readiness boundaries explicit.
