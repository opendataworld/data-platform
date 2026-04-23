# Canonical Entity Directory MVP

Thin product slice for managing canonical entities with Git-backed JSON assets.

## Run

```bash
cd apps/canonical-entity-directory
python3 server.py
```

Then open http://localhost:8091.

## Status model

- `draft` -> `approved` -> `published`

## Storage Convention

Entities are stored at:

- `apps/canonical-entity-directory/data/entities/<entity_id>/v<version>.json`
- `apps/canonical-entity-directory/data/entities/<entity_id>/latest.json`

Each save creates a new version.

## API

- `GET /api/entities?q=&status=&entity_type=`
- `GET /api/entities/<entity_id>`
- `POST /api/entities`
- `POST /api/entities/<entity_id>/transition` with `{ "status": "approved|published|draft" }`
- `GET /api/export.json`
- `GET /api/export.csv`
- `POST /api/import.json` with a JSON array
