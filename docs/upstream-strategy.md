# Upstream OSS Strategy

## Principle order

OpenDataWorld Data Platform uses an OSS-first strategy in this order:
1. **Integrate** upstream projects directly.
2. **Compose** services together in this umbrella repo.
3. **Clone** temporarily when practical for experimentation.
4. **Fork** only for durable, product-specific customization that cannot be handled upstream.

## Why this strategy

- Reduces maintenance burden.
- Keeps security and feature updates closer to upstream.
- Avoids unnecessary platform rewrites.
- Preserves reviewability and delivery speed.

## Current upstream foundations

Current foundations represented in this repo include OpenMetadata, Airbyte, OpenLineage/Marquez direction, Zingg, Cube, Superset, TerminusDB, GraphDB, Jena, SurrealDB, Postgres, Redis, Label Studio, Argilla, SearXNG, Firecrawl, Crawl4AI, and Playwright.

## Planned additions and expansion

- **Marquez** for stronger lineage backend workflows.
- **Feast** for feature-store workflows where online/offline feature management is required.

These additions should be integrated into existing module narratives rather than used as a trigger to prematurely split repositories.

## Forking policy

Fork only when all are true:
- required capability is not achievable via config/plugin/extension,
- upstream contribution path is blocked or too slow for committed milestones,
- long-term ownership cost is explicitly accepted.
