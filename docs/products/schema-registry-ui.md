# Schema Registry UI MVP

## Current state (as of 2026-04-23)
- Product slice added at `apps/schema-registry-ui/`.
- Schema assets are stored as versioned JSON files in Git-tracked path: `data-platform/registry/schema-assets/<schema_id>/<version>.json`.
- Minimal Flask API and browser UI implemented for browse/create/diff/validate/import/export.
- Lifecycle states currently supported: `draft`, `approved`, `published`.

## GitHub-backed storage convention
Each schema asset version is a single file:

`data-platform/registry/schema-assets/{schema_id}/{version}.json`

Versioning and approval history are handled through normal Git/GitHub commits, PR review, and merge history.

## MVP API surface
- `GET /api/schemas`
- `GET /api/schemas/{schema_id}?version=...`
- `POST /api/schemas`
- `POST /api/schemas/{schema_id}/status`
- `GET /api/schemas/{schema_id}/diff?v1=...&v2=...`
- `POST /api/schemas/validate`
- `GET /api/schemas/{schema_id}/export?format=json|yaml`
- `POST /api/schemas/import?format=json|yaml`

## Minimal schema asset model
Required top-level fields:
- `schema_id`
- `name`
- `version`
- `status`
- `schema_type`
- `properties`
- `required`
- `validation`

Optional fields:
- `references` (parent/schema links)

## PRD alignment and mismatch note
Requested architectural source file `org/high-level-prd.md` was not present in the repo at implementation time. To avoid blocking delivery, this MVP aligns with existing repo direction in `data-platform/bootstrap.md` (thin product slice, GitHub as system of record, practical progress). A follow-up is required to add and baseline `org/high-level-prd.md` for strict PRD-governed delivery.
