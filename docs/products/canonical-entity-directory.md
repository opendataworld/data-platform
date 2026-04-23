# Canonical Entity Directory MVP

## Purpose

Canonical Entity Directory is a thin OpenDataWorld product slice for managing canonical entity records directly in GitHub-backed files (this repo), with a minimal browser UI and HTTP API.

## Current State (MVP)

The MVP is implemented at `apps/canonical-entity-directory/` and provides:

- entity create/update with version increments
- lifecycle states: `draft`, `approved`, `published`
- aliases and source references
- browse + text search + basic filters
- JSON and CSV export
- JSON import
- Git-backed asset versioning via committed files

## Asset Model

Each entity record contains:

- `entity_id` (string)
- `canonical_name` (string)
- `entity_type` (string)
- `version` (integer)
- `status` (`draft|approved|published`)
- `aliases` (string[])
- `source_references` (string[])
- `description` (optional string)
- `notes` (optional string)
- `updated_at` (ISO timestamp)

## Storage Convention

Entity assets are stored under:

- `apps/canonical-entity-directory/data/entities/<entity_id>/v<version>.json`
- `apps/canonical-entity-directory/data/entities/<entity_id>/latest.json`

This convention keeps a simple append-only history by version while exposing a stable latest pointer.

## API Surface

- `GET /api/entities?q=&status=&entity_type=`
- `GET /api/entities/<entity_id>`
- `POST /api/entities`
- `POST /api/entities/<entity_id>/transition`
- `GET /api/export.json`
- `GET /api/export.csv`
- `POST /api/import.json`

## UI Surface

- Single-page browser UI at `/`
- Form for create/update
- Search and filter controls
- Tabular browse results
- Export links for JSON / CSV

## PRD and Prompt Registry Mismatch Notes

The prompt references these assets as existing source-of-truth inputs:

- `org/high-level-prd.md`
- `data-platform/overview.md`
- `shared/review-prompt.md`
- `agents/repo-builder-agent.md`

In current repo state, these files are missing. This MVP proceeds with the umbrella-platform direction from existing docs and `AGENTS.md`, and logs the mismatch for correction in review notes.
