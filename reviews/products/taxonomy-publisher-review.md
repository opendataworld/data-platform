# Taxonomy Publisher MVP Review Notes

## Scope Delivered

- Created first product slice under `apps/taxonomy-publisher/`.
- Implemented usable browser-accessible UI and minimal HTTP API.
- Added taxonomy asset model with lifecycle status, version, aliases, and parent-child support.
- Added JSON/CSV import/export capabilities.
- Added product and roadmap docs.

## Current vs Next vs Future

### Current
- MVP ships as a thin service with local file persistence in git-tracked storage.
- Governance represented by lifecycle state and reviewable git commits.

### Recommended Next
- Add stricter workflow constraints and validation.
- Add explicit review metadata and publish checks.
- Add optional GitHub API write mode for PR-native promotion flow.

### Future
- Evolve into taxonomy-registry-aligned module/repo after boundaries stabilize.
- Integrate with broader platform registries and policy controls.

## Mismatches Found

1. Prompt references `org/high-level-prd.md`, but file is missing from current repository.
2. Related prompt assets referenced in task (`data-platform/overview.md`, `shared/review-prompt.md`, `agents/repo-builder-agent.md`) are also missing.

## Proposed Minimal Corrections

1. Add `org/high-level-prd.md` as canonical architecture baseline.
2. Add missing prompt assets or update prompt references to existing canonical files.
3. Keep product slice in-repo while establishing product acceptance checks in PRD.
