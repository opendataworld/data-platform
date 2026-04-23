# Schema Registry UI MVP Review Notes

Date: 2026-04-23

## What changed
- Added `apps/schema-registry-ui` with Flask API + minimal browser UI.
- Added initial schema assets under `data-platform/registry/schema-assets/customer-profile/`.
- Added product docs and roadmap under `docs/products/`.

## Mismatches and corrections
- Expected PRD file `org/high-level-prd.md` is currently missing.
- Correction proposed: create and maintain `org/high-level-prd.md` as a mandatory source-of-truth artifact before additional product slices.

## Quality and usability
- MVP is intentionally small but usable: create/list/get/diff/validate/import/export and lifecycle status update.
- Uses Git/GitHub commit history as version and review backbone.

## Follow-ups
- Add CI checks for schema validation and compatibility.
- Add GitHub PR templates/checklists for schema state transitions.
- Add stronger UI browse/search and per-field diff rendering.
