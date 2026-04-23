# Parallel Run Consolidation Review

Date: 2026-04-23 (UTC)
Scope: Consolidation review of 4 parallel MVP runs (`taxonomy-publisher`, `vocabulary-manager`, `canonical-entity-directory`, `schema-registry-ui`).
Canonical prompt: `data-platform/reviews/parallel-run-consolidation.md`
Related PRD: `org/high-level-prd.md` (missing in current repo state)

## 1) Summary

The four runs all shipped usable thin product slices and broadly align with the umbrella-repo direction. The strongest common pattern is:
- one app per product under `apps/`
- one product spec prompt under `data-platform/products/`
- one product doc + roadmap under `docs/products/`
- one review note under `reviews/products/`

However, they diverge in storage conventions, naming, runtime stack, and lifecycle governance strictness. The clean merged state should preserve all four MVP slices while normalizing language, folder conventions, and cross-product standards so each product is easier to compare and evolve.

## 2) Conflicts found

### A. PRD source-of-truth conflict (highest priority)
- Required PRD path `org/high-level-prd.md` is missing.
- Every run references this file but cannot actually validate against it.
- This is a governance gap: prompt/PRD contract exists in text, but not in repository reality.

**Proposed correction:**
1. Add `org/high-level-prd.md` immediately.
2. Add a short Prompt Registry index that lists canonical prompt + PRD paths.
3. Gate future product runs on PRD file existence.

### B. Registry path inconsistency
- Schema assets use `data-platform/registry/schema-assets/...` (singular `registry`).
- Vocabulary assets use `data-platform/registries/vocabularies/...` (plural `registries`).
- Other slices store assets under app-local paths (`apps/.../storage` or `apps/.../data`).

**Consequence:** ambiguous canonical storage boundary for governed assets.

**Proposed correction:** normalize to `data-platform/registries/<domain>/...` for canonical assets, while allowing app-local cache/runtime files only when clearly non-canonical.

### C. Status/lifecycle governance inconsistency
- All slices use `draft|approved|published`, which is good.
- Transition rules differ:
  - vocabulary-manager enforces forward-only transitions.
  - taxonomy-publisher and schema-registry-ui permit broader direct updates.
  - canonical-entity-directory allows status changes but versions on each write.

**Proposed correction:** adopt one shared lifecycle policy (allowed transitions + required metadata) and reference it in each product README/doc.

### D. Versioning model inconsistency
- canonical-entity-directory: integer auto-increment (`v1`, `v2`).
- schema-registry-ui: explicit semantic-like string version folders/files.
- taxonomy-publisher: version field only in document, single file per taxonomy.
- vocabulary-manager: version field in document, single file per vocabulary.

**Proposed correction:** define canonical version semantics per asset class in a common policy doc; keep current MVP implementations but converge naming and validation over next iteration.

### E. Runtime stack inconsistency (acceptable for now)
- taxonomy + canonical entity use stdlib HTTP servers.
- schema uses Flask.
- vocabulary uses FastAPI.

**Assessment:** acceptable for thin MVPs; do not force immediate framework unification. Standardize API style and docs first.

## 3) Best changes to keep

1. Keep all four product slices and their docs/roadmaps/reviews.
2. Keep consistent lifecycle vocabulary (`draft`, `approved`, `published`) across all products.
3. Keep Git-backed asset pattern (all products persist assets as tracked JSON files).
4. Keep product-level roadmap separation (`docs/products/*-roadmap.md`) with current/next/future framing.
5. Keep review-note discipline under `reviews/products/`.

## 4) Changes to reject or modify

### Modify (not reject)
1. **Storage path naming**
   - Modify schema path from `data-platform/registry/schema-assets/` to pluralized registry convention in next consolidation PR.
2. **README/doc language normalization**
   - Normalize product README opening paragraph and section headings (Purpose, Run, Storage, Lifecycle, API, Current/Next/Future).
3. **Lifecycle transition enforcement**
   - Modify all services to use a shared transition matrix + optional metadata fields (`reviewed_by`, `approved_at`, `published_at`).
4. **Prompt/PRD references**
   - Modify prompt templates and docs to reference files that actually exist in-repo.

### Reject
1. Reject adding more divergent folder conventions for new products.
2. Reject introducing additional lifecycle labels before PRD baseline is present.
3. Reject premature repo split proposals until module boundaries stabilize.

## 5) Recommended final merged structure

```text
apps/
  taxonomy-publisher/
  vocabulary-manager/
  canonical-entity-directory/
  schema-registry-ui/

data-platform/
  products/
    taxonomy-publisher-mvp.md
    vocabulary-manager-mvp.md
    canonical-entity-directory-mvp.md
    schema-registry-ui-mvp.md
  reviews/
    parallel-run-consolidation.md
  registries/
    taxonomies/               # recommended target (future move from app-local storage)
    vocabularies/
    entities/                 # recommended target (future move from app-local storage)
    schemas/                  # recommended target (future rename from registry/schema-assets)

org/
  high-level-prd.md           # must be added

docs/
  products/
    taxonomy-publisher.md
    taxonomy-publisher-roadmap.md
    vocabulary-manager.md
    vocabulary-manager-roadmap.md
    canonical-entity-directory.md
    canonical-entity-directory-roadmap.md
    schema-registry-ui.md
    schema-registry-ui-roadmap.md

reviews/
  products/
    taxonomy-publisher-review.md
    vocabulary-manager-review.md
    canonical-entity-directory-review.md
    schema-registry-ui-review.md
  parallel-run-consolidation-review.md
```

## 6) Remaining follow-ups

### Current accepted state (ship now)
- Keep current four MVP slices as merged and runnable.
- Accept this consolidation review as the control document.

### Recommended next state (near-term)
1. Add missing PRD file `org/high-level-prd.md`.
2. Add one shared lifecycle policy doc and wire all four products to it.
3. Standardize canonical asset storage convention under `data-platform/registries/`.
4. Normalize README template language across product apps.
5. Add a single index doc listing canonical prompt and PRD locations.

### Deferred future work
1. Framework unification (FastAPI/Flask/http.server) only if operational costs justify it.
2. Repo/module splitting after interface boundaries and ownership are stable.
3. Cross-registry linking/policy automation after baseline governance files are in place.

## 7) Accept / Modify / Reject matrix

### Accept
- `apps/taxonomy-publisher/` (thin MVP, API + UI)
- `apps/vocabulary-manager/` (strong lifecycle transition enforcement)
- `apps/canonical-entity-directory/` (versioned entity history model)
- `apps/schema-registry-ui/` (schema validate + diff capabilities)
- `docs/products/*` and `reviews/products/*` artifacts as baseline MVP documentation

### Modify
- `data-platform/registry/schema-assets/` path naming and alignment with registries convention
- Product README/doc section ordering and terminology normalization
- Lifecycle transition behavior for consistency across all products
- Prompt references to missing assets and PRD indexability

### Reject
- Any additional naming variants for registry folders
- New lifecycle terms beyond `draft|approved|published` before PRD ratification
- Any premature multi-repo decomposition for these four product slices
