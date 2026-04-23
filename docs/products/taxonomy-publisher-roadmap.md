# Taxonomy Publisher Roadmap

## Current MVP (Now)

- Single-service local app with file-backed JSON taxonomy assets in Git-tracked storage.
- Manual lifecycle progression (`draft` -> `approved` -> `published`) via API update.
- CSV import/export and JSON CRUD endpoints.

## Recommended Next State (Near-Term)

1. Add lightweight validation profile checks (duplicate term IDs, parent existence, cycle detection).
2. Add explicit review metadata (`reviewed_by`, `approved_at`, change note).
3. Add publish guardrail endpoint that only allows `approved -> published` transitions.
4. Add GitHub API mode (optional) for branch/PR-based writes instead of local file write.
5. Add minimal auth gate suitable for internal product use.

## Future State (Platform-Scale)

1. Promote this slice into a dedicated taxonomy registry module when boundaries are stable.
2. Add event hooks to catalog, lineage, and semantic modules.
3. Add schema registry linkage to validate taxonomy references in datasets.
4. Add multi-taxonomy dependency and release channels.
5. Add package exports for downstream systems and policy-based publication.

## Repo-Structure Guidance

- Keep taxonomy publisher in this umbrella repo until product boundary, ownership, and API contracts stabilize.
- Split into a dedicated repo only after repeated release cadence and cross-module contract maturity.
