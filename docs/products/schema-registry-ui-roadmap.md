# Schema Registry UI Roadmap

## MVP (delivered)
- Thin schema registry product slice in umbrella repo
- GitHub-backed schema storage convention
- Basic schema validation and lifecycle states
- Diff visibility between versions
- JSON and YAML import/export

## Next state (recommended)
1. Add PR workflow templates for schema lifecycle transitions (draft->approved->published)
2. Add server-side semantic version policy checks
3. Add richer schema browser with search/filter
4. Add branch-aware preview/validation checks in CI
5. Add authn/authz integration with platform gateway

## Future state
- Promote this slice into a standalone `schema-registry` module/repo when boundaries stabilize
- Add cross-registry references (taxonomy/entity/vocabulary)
- Add policy rules for backward compatibility and deprecation windows
- Add review workflow automation (status gates tied to PR labels/checks)
