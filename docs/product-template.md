# Shared Product Slice Template (OpenDataWorld)

This document defines the reusable pattern for building the next thin OpenDataWorld product slice in this umbrella Data Platform repo.

## PRD and Prompt Registry prerequisites

1. Save the task prompt under an agreed Prompt Registry path in this repo.
2. Read the saved prompt back and treat it as canonical.
3. Read the org PRD (`org/high-level-prd.md`) before implementation.
4. If the PRD path is missing, log it as a mismatch in docs/review notes and propose the smallest correction.

## Common patterns identified from existing slices

Across `taxonomy-publisher`, `vocabulary-manager`, `schema-registry-ui`, and `canonical-entity-directory`, these patterns are consistent:

- Thin product slice under `apps/<product-slug>/`
- Browser-accessible surface (minimal HTML UI and/or OpenAPI docs)
- Lightweight Python service layer (Flask/FastAPI/stdlib HTTP)
- Git-tracked asset files as canonical storage/version history
- Lifecycle states centered on `draft -> approved -> published`
- Product docs under `docs/products/`
- Roadmap docs separated from current-state docs
- Review notes under `reviews/products/` with current/next/future framing

## Standard product folder structure

Use this as the default:

```text
apps/<product-slug>/
  README.md
  app.py|server.py
  requirements.txt (if needed)
  static/index.html (if UI)
  data/ or storage/ (only when product-local assets are needed)

data-platform/registries/<asset-domain>/
  <asset files>

docs/products/
  <product-slug>.md
  <product-slug>-roadmap.md

reviews/products/
  <product-slug>-review.md
```

## Standard asset metadata/frontmatter schema

Every asset JSON/YAML should include:

- `asset_id` (string)
- `asset_type` (string)
- `name` (string)
- `version` (string)
- `status` (`draft|approved|published|deprecated`)
- `owners` (string array)
- `tags` (string array)
- `description` (string)
- `created_at` (ISO-8601)
- `updated_at` (ISO-8601)
- `source_repo` (string)
- `source_path` (string)
- `review` object:
  - `review_status`
  - `reviewed_by`
  - `reviewed_at`
  - `review_notes_path`

Domain-specific payload should live under a single `content` key.

## Lifecycle/status model

Use this default state progression:

- `draft`: editable, not approved for downstream use
- `approved`: reviewed and accepted for controlled use
- `published`: official release for broader use
- `deprecated` (optional): maintained for compatibility but no new investment

Guardrails:

- Default forward path: `draft -> approved -> published`
- Backward transitions require an explicit review note entry
- Publishing should reference commit/PR traceability

## GitHub-backed storage pattern

- Assets are files in this repo (or a designated registry repo when split later)
- Git commits/PRs are the auditable change log
- Review notes and docs are committed alongside asset changes
- Product APIs should expose `source_path` and version/status metadata

## Product docs pattern

Each product should ship:

1. Product doc (`docs/products/<product>.md`)
   - purpose
   - current state
   - asset model
   - storage/versioning
   - API/UI surface
   - PRD alignment and mismatch notes
2. Roadmap doc (`docs/products/<product>-roadmap.md`)
   - now/next/later plan
   - explicit non-goals

## Review note pattern

Each substantial slice/template update should log:

- what changed
- common pattern decisions
- current vs next vs future
- mismatches with PRD/prompt/repo reality
- smallest correction proposed

## Current vs next vs future (template level)

### Current state
- Reusable templates now exist for product/docs/assets/reviews.
- Existing MVP slices share a common baseline pattern.

### Recommended next state
- Add CI checks to validate required metadata keys and status transitions.
- Add a repo-level checklist for new product slices.

### Future state
- Split domain registries only once boundaries stabilize.
- Keep the same template contract across future repos.
