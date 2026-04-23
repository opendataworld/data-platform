# Review Notes: Shared Asset SDK

## Scope reviewed
- Introduced `src/shared/assets` helper package.
- Refactored current product slices to consume shared helpers where duplicated logic existed.

## Shared patterns extracted
- Status validation (`draft`, `approved`, `published`)
- UTC timestamp helper
- ID normalization helper
- JSON read/write helpers with newline + UTF-8 conventions
- Common error types for validation/not-found

## Product slices updated
- `apps/schema-registry-ui/app.py`
- `apps/taxonomy-publisher/app.py`
- `apps/vocabulary-manager/app.py`
- `apps/canonical-entity-directory/entity_store.py`

## Practicality check
- Lightweight extraction only; no framework layer added.
- Product-specific validation remains local to each slice.
- GitHub-backed file storage behavior remains unchanged.

## PRD/source-of-truth check
- Prompt stored at `data-platform/foundation/shared-asset-sdk.md` and read back.
- Requested PRD path `org/high-level-prd.md` is currently missing.

## Recommended follow-ups
1. Add missing org PRD file or correct path references.
2. Add thin tests for shared helpers (`ensure_status`, `save_asset_json`, `read_asset_json`).
3. Standardize status transition policies where needed (vocabulary manager currently has local transition map).
