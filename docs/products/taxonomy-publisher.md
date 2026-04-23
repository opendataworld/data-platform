# Taxonomy Publisher MVP

## Purpose

Taxonomy Publisher is the first narrow OpenDataWorld product slice. It provides a minimal governed workflow for taxonomy assets stored directly in GitHub (this repository), with lifecycle states and import/export support.

## Current State (Implemented in MVP)

- Product slice created at `apps/taxonomy-publisher/`.
- Browser-accessible UI at `/` served by a lightweight Python HTTP service.
- API for list/create/update/get taxonomy assets.
- Lifecycle states supported: `draft`, `approved`, `published`.
- JSON taxonomy model with parent-child relationship and aliases.
- CSV import and CSV export support.
- GitHub-backed storage convention via git-tracked JSON files in `apps/taxonomy-publisher/storage/taxonomies/`.

## Taxonomy Asset Model

```json
{
  "id": "animals",
  "name": "Animals",
  "version": "0.1.0",
  "status": "draft",
  "terms": [
    {
      "id": "mammals",
      "label": "Mammals",
      "parent_id": null,
      "aliases": []
    },
    {
      "id": "canines",
      "label": "Canines",
      "parent_id": "mammals",
      "aliases": ["dogs"]
    }
  ],
  "metadata": {},
  "created_at": "2026-04-23T00:00:00+00:00",
  "updated_at": "2026-04-23T00:00:00+00:00"
}
```

## Storage and Versioning Convention

- Path pattern: `apps/taxonomy-publisher/storage/taxonomies/{taxonomy-id}.json`
- Taxonomy IDs are slugified for stable filenames.
- Each change is persisted as file updates; git commit history is the canonical version timeline.
- Version field is explicit (`version`) and can be incremented by reviewers/publishers.

## Workflow

1. Create taxonomy in `draft`.
2. Review and transition to `approved`.
3. Publish by transitioning to `published`.
4. Export published taxonomy via CSV endpoint for downstream systems.

## Minimal API Surface

- `GET /health`
- `GET /api/taxonomies`
- `GET /api/taxonomies?status=<draft|approved|published>`
- `POST /api/taxonomies`
- `PUT /api/taxonomies/{id}`
- `GET /api/taxonomies/{id}`
- `GET /api/taxonomies/{id}/export.csv`
- `POST /api/import/csv`

## PRD Alignment and Mismatch Note

- Requested PRD file `org/high-level-prd.md` is currently missing in repo reality.
- Minimal correction proposed: add `org/high-level-prd.md` to Prompt Registry with canonical architecture and acceptance criteria for product slices.
- MVP implementation intentionally remains thin and repo-local to honor umbrella-repo-first architecture and avoid premature split.
