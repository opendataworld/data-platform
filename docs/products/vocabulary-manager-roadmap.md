# Vocabulary Manager Roadmap

## Current MVP (now)

- API-first product slice for vocabulary CRUD + lifecycle.
- GitHub-backed JSON asset storage.
- CSV/JSON import-export.
- Basic relationship fields between terms.

## Recommended next state (near-term)

1. Add minimal browser UI for non-technical editors:
   - list vocabularies
   - edit terms
   - submit status change requests
2. Add schema validation hooks in CI for vocabulary JSON files.
3. Add lightweight review automation:
   - enforce valid state transition in PR checks
   - publish changelog snippet per vocabulary version update
4. Add explicit "publish bundle" output (for downstream catalog/search consumption).

## Future state (later)

1. Evolve this product slice toward a dedicated `vocabulary-registry` module/repo when boundaries stabilize.
2. Add richer semantic capabilities:
   - SKOS mapping export
   - broader linked-data graph integration
3. Add policy/governance layer:
   - role-based approvals
   - provenance metadata
   - deprecation and replacement policies
4. Integrate with other canonical registries:
   - taxonomy registry
   - schema registry
   - entity/thing registries

## Non-goals for current MVP

- Full enterprise taxonomy/vocabulary suite.
- Complex workflow orchestration.
- Immediate multi-repo decomposition.
