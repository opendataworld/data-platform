# <Product Name> MVP

Thin OpenDataWorld product slice for managing <asset-domain> with GitHub-backed assets.

## Purpose

- Problem solved:
- Primary users:
- Asset domain:

## Run

```bash
cd apps/<product-slug>
# install deps
# run service
```

## Storage convention

- Canonical path: `data-platform/registries/<asset-domain>/...`
- Git commit + PR history is the canonical version/review timeline.

## Status model

- `draft` -> `approved` -> `published` (optional `deprecated`)

## API/UI surface

- `GET /health`
- `GET /api/...`
- `POST /api/...`

## Asset metadata baseline

All assets should include:

- `asset_id`, `asset_type`, `name`, `version`, `status`
- `owners`, `tags`, `description`
- `created_at`, `updated_at`
- `source_repo`, `source_path`
- `review` metadata
