# Bootstrap Review: Data Platform Repositioning

## What changed

- Rewrote `README.md` to position this repository as the OpenDataWorld Data Platform umbrella repo.
- Added architecture framing that clearly separates OpenDataWorld Data Platform scope from AgentNxt AI Platform scope.
- Added four new docs:
  - `docs/platform-overview.md`
  - `docs/module-map.md`
  - `docs/upstream-strategy.md`
  - `docs/repo-roadmap.md`
- Documented module meanings including a future `registries` module for canonical domain registries.
- Explicitly separated current state, recommended next state, and future modular split across docs.

## What remains future work

- Harmonize existing profile documentation (for example `docs/PROFILES.md`) with current `docker-compose.yml` profile reality.
- Add concrete implementation guidance for stronger lineage and feature-store pathways (Marquez/Feast) as part of module hardening.
- Define governance and readiness criteria for any eventual modular repo split.

## Mismatches found between repo reality and PRD/prompt requirements

1. **Missing PRD file**
   - Expected: `org/high-level-prd.md`
   - Observed: file not present in repository at execution time.
   - Correction proposed: add and maintain `org/high-level-prd.md` in this repo (or sync it in via prompt-registry automation) so architectural checks can be validated against an actual source file.

2. **Documentation drift risk**
   - Existing docs reference profile groupings and services that may not fully align with the evolving compose file.
   - Correction proposed: establish a lightweight doc-sync check in CI (or periodic review checklist) to keep profile docs consistent with compose definitions.
