# Data Platform Repo Roadmap

## Current state (now)

- `opendataworld/data-platform` functions as the umbrella integration/deployment repo.
- Docker Compose profiles drive selective service startup.
- Documentation exists but has been partially inconsistent with evolving module language.

## Recommended next state (near term)

1. Keep this repo as the central integration surface.
2. Align docs with actual profile/service reality.
3. Stabilize module language (`catalog`, `lineage`, `ingestion`, `resolution`, `semantic`, `visualization`, `graph`, `store`, `labeling`, `features`, `search`, `docs`, `registries`).
4. Incrementally harden lineage and features coverage (including Marquez and Feast pathways).
5. Track mismatches between docs and compose as explicit review items.

## Future state (modular split when stable)

A future split can occur after boundaries are stable and ownership is clear, for example:
- keep umbrella orchestration/docs in `data-platform`
- move mature, independently operated slices into dedicated repos
- keep registry-domain repos separate only when governance and interfaces are stable

## Non-goals for this phase

- No premature explosion into many repos.
- No claims that future repos already exist.
- No rewrite of mature upstream OSS components.

## Decision gates before any split

- Clear module ownership.
- Stable API/event/data contracts.
- Repeatable deployment and support model.
- Net reduction in operational complexity.
