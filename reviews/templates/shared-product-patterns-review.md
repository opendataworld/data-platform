# Shared Product Patterns Review Notes

Date: 2026-04-23

## Scope delivered

- Extracted common patterns from the four completed product slices:
  - `taxonomy-publisher`
  - `vocabulary-manager`
  - `schema-registry-ui`
  - `canonical-entity-directory`
- Added a shared product pattern guide at `docs/product-template.md`.
- Added reusable templates for product docs, roadmap, review notes, and asset schemas under `templates/`.
- Applied small normalization updates to existing product README files for consistent status-model language.
- Saved the current task prompt to `data-platform/templates/shared-product-patterns.md` and read it back as canonical.

## Common pattern decisions

1. Keep slices thin and app-local (`apps/<product-slug>/`) with minimal API/UI.
2. Keep GitHub/Git-tracked files as canonical asset storage and version timeline.
3. Use a shared lifecycle baseline: `draft -> approved -> published`.
4. Keep product docs in `docs/products/` and review notes in `reviews/products/`.
5. Use explicit `current/next/future` framing for roadmap and review outputs.

## Current vs Next vs Future

### Current
- Shared templates exist and reflect what worked in delivered MVP slices.
- Existing slice READMEs now use a consistent status model section.

### Next
- Add CI checks to validate required asset metadata keys.
- Add transition validation checks for lifecycle states.

### Future
- Adopt the same template contract in future domain-specific repos when module boundaries stabilize.

## Mismatches found

- Required PRD file `org/high-level-prd.md` is not present in current repo reality.

## Proposed minimal correction

1. Add `org/high-level-prd.md` to this repo Prompt Registry paths and reference it from product/template docs.
2. Add a lightweight index of canonical Prompt Registry artifacts to reduce repeated missing-path mismatches.
