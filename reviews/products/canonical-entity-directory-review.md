# Review: Canonical Entity Directory MVP

## What Changed

- Added a thin product slice at `apps/canonical-entity-directory/` with a minimal API + browser UI
- Implemented Git-backed canonical entity storage and versioning via JSON files
- Added lifecycle states and transition endpoint
- Added browse/search/filter and import/export support
- Added product and roadmap docs

## Current vs Next vs Future

### Current
A usable MVP exists inside the umbrella Data Platform repo.

### Next
Strengthen governance and validation (CI schema checks, formal review policies, provenance).

### Future
Evolve into a fuller entity registry module with cross-registry links and policy-driven publication.

## Mismatches Observed

Prompt/PRD references mention the following files as available in Prompt Registry, but they are missing in repo reality:

- `org/high-level-prd.md`
- `data-platform/overview.md`
- `shared/review-prompt.md`
- `agents/repo-builder-agent.md`

## Proposed Minimal Correction

1. Add the missing Prompt Registry/PRD files (or update prompts to point at canonical existing paths).
2. Add a short registry index document listing canonical prompt and PRD locations.
3. Keep this MVP in-repo for now; do not split repos yet.
