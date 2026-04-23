# Canonical Entity Directory Roadmap

## Current (Delivered in this MVP)

- GitHub-backed canonical entity assets in repo-managed JSON files
- Thin web UI + API for CRUD-lite workflows
- Versioned entity writes
- Lifecycle support (`draft`, `approved`, `published`)
- Alias and source-reference tracking
- Browse/search/filter + JSON/CSV export + JSON import

## Next State (Recommended)

1. Add schema validation and linting for entity assets in CI
2. Add review workflow conventions (PR templates, required reviewers per entity type)
3. Add provenance fields (`created_by`, `reviewed_by`, `change_reason`)
4. Add simple audit page (entity version timeline view)
5. Add optional GitHub API mode for external repo-backed registry storage

## Future State (Entity Registry Evolution)

1. Promote this slice to a broader `entity-registry` module once boundaries stabilize
2. Add cross-registry references (taxonomy/vocabulary/schema/entity links)
3. Add stronger publishing controls and policy gates
4. Add semantic/graph integration for entity relationships
5. Split into dedicated repo only when product boundaries and interfaces are stable
