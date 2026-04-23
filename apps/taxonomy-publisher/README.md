# Taxonomy Publisher MVP

Thin product slice for managing governed taxonomy assets in GitHub-backed JSON files.

## Run

```bash
python3 app.py
```

Then open <http://localhost:8787>.

## API

- `GET /api/taxonomies` list all taxonomy assets
- `GET /api/taxonomies?status=draft|approved|published` filter by lifecycle state
- `POST /api/taxonomies` create/upsert taxonomy from JSON
- `PUT /api/taxonomies/{id}` update taxonomy fields from JSON patch payload
- `GET /api/taxonomies/{id}` fetch taxonomy asset
- `GET /api/taxonomies/{id}/export.csv` export taxonomy terms as CSV
- `POST /api/import/csv` import CSV to taxonomy asset

## Status model

- `draft` -> `approved` -> `published`

## Storage convention

- Taxonomy assets are stored under `apps/taxonomy-publisher/storage/taxonomies/*.json`.
- Git history in this repository is the canonical version log.
- Lifecycle state is stored in each asset (`draft`, `approved`, `published`).
