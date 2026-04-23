# Schema Registry UI MVP

Thin product slice for OpenDataWorld Data Platform.

## What it provides
- GitHub-backed schema asset storage under `data-platform/registry/schema-assets/`
- Minimal browser UI (`/`) for browse + save + diff
- Minimal API for create/read/status/diff/validate/import/export
- Lifecycle states: `draft`, `approved`, `published`

## Run locally
```bash
cd apps/schema-registry-ui
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:8787`.

## Schema asset shape
```json
{
  "schema_id": "customer-profile",
  "name": "Customer Profile",
  "version": "1.0.0",
  "status": "draft",
  "schema_type": "json_schema",
  "properties": {"customerId": {"type": "string"}},
  "required": ["customerId"],
  "validation": {
    "is_valid": true,
    "errors": [],
    "validated_at": "2026-04-23T00:00:00+00:00",
    "validator": "jsonschema.Draft202012Validator"
  },
  "references": []
}
```
