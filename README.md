# OpenDataWorld Data Platform (`opendataworld/data-platform`)

This repository is the **umbrella repo** for the OpenDataWorld **Data Platform**.

It is the primary place for:
- deployment and integration
- local/dev platform assembly
- OSS service composition via Docker Compose profiles
- platform architecture documentation
- module and roadmap definition

It is **not** the AI Platform, Identity Platform, or Intelligence Platform.

## Platform positioning

- **OpenDataWorld** = Data Platform (this repo)
- **AgentNxt** = AI Platform (separate platform/repo concern)

This repo intentionally focuses on data infrastructure and data product plumbing. It can integrate with AgentNxt, but it does not absorb AgentNxt scope.

## Current scope (today)

Current repo reality is an umbrella deployment and integration workspace with:
- compose-managed OSS services across catalog, ingestion, storage, semantic, visualization, graph, search, and labeling concerns
- profile-based startup so teams can run only what they need
- architecture and operations docs that describe rollout phases and environments

Key current OSS foundations in this repo include:
- OpenMetadata
- Airbyte
- Zingg
- Cube
- Superset
- TerminusDB
- GraphDB
- Apache Jena
- SurrealDB
- Postgres
- Redis
- Label Studio
- Argilla
- SearXNG
- Firecrawl
- Crawl4AI
- Playwright

Planned/expanding integrations include lineage and feature components such as **Marquez** and **Feast**, integrated as needed rather than rewritten.

## Long-term architecture direction

OpenDataWorld’s Data Platform direction includes canonical domain registries, such as:
- dataset registry
- schema registry
- taxonomy registry
- vocabulary registry
- entity registry
- thing registry
- publication registry
- license registry
- eval data registry

These are a **future architectural destination**. They should be documented and staged before any aggressive repo split.

## Documentation map

- [Platform overview](docs/platform-overview.md)
- [Module map](docs/module-map.md)
- [Upstream strategy](docs/upstream-strategy.md)
- [Repo roadmap](docs/repo-roadmap.md)
- [Compose profiles reference](docs/PROFILES.md)
- [Phase plan](docs/phase-plan.md)

## Operating principles

- Build practical, usable product slices first.
- Prefer OSS integration/composition before cloning/forking.
- Make minimum structural change needed for the current deliverable.
- Keep current state, next state, and future state explicit in docs.
- Keep GitHub artifacts (prompt, docs, review notes) as system-of-record outputs.
