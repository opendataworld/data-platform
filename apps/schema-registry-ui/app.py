from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import unified_diff
from pathlib import Path
from typing import Any

import yaml
from flask import Flask, jsonify, request, send_from_directory
from jsonschema import Draft202012Validator

app = Flask(__name__, static_folder="static", static_url_path="/static")

BASE_DIR = Path(__file__).resolve().parents[2]
ASSET_ROOT = BASE_DIR / "data-platform" / "registry" / "schema-assets"
ALLOWED_STATUSES = {"draft", "approved", "published"}
ALLOWED_TYPES = {"json_schema"}


@dataclass
class SchemaAsset:
    schema_id: str
    name: str
    version: str
    status: str
    schema_type: str
    properties: dict[str, Any]
    required: list[str]
    validation: dict[str, Any]
    references: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "schema_type": self.schema_type,
            "properties": self.properties,
            "required": self.required,
            "validation": self.validation,
            "references": self.references,
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def schema_dir(schema_id: str) -> Path:
    return ASSET_ROOT / schema_id


def version_path(schema_id: str, version: str) -> Path:
    return schema_dir(schema_id) / f"{version}.json"


def read_asset(schema_id: str, version: str) -> dict[str, Any]:
    path = version_path(schema_id, version)
    if not path.exists():
        raise FileNotFoundError(f"Schema {schema_id} version {version} was not found")
    return json.loads(path.read_text())


def write_asset(asset: dict[str, Any]) -> Path:
    path = version_path(asset["schema_id"], asset["version"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asset, indent=2) + "\n")
    return path


def latest_version(schema_id: str) -> str | None:
    folder = schema_dir(schema_id)
    if not folder.exists():
        return None
    versions = sorted(p.stem for p in folder.glob("*.json"))
    return versions[-1] if versions else None


def validate_json_schema(schema_doc: dict[str, Any]) -> dict[str, Any]:
    try:
        Draft202012Validator.check_schema(schema_doc)
        return {"is_valid": True, "errors": []}
    except Exception as exc:  # jsonschema raises a typed exception hierarchy
        return {"is_valid": False, "errors": [str(exc)]}


def normalize_payload(payload: dict[str, Any]) -> SchemaAsset:
    schema_type = payload.get("schema_type", "json_schema")
    if schema_type not in ALLOWED_TYPES:
        raise ValueError(f"schema_type must be one of {sorted(ALLOWED_TYPES)}")

    status = payload.get("status", "draft")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"status must be one of {sorted(ALLOWED_STATUSES)}")

    schema_id = payload["schema_id"].strip()
    version = payload["version"].strip()
    if not schema_id or not version:
        raise ValueError("schema_id and version are required")

    properties = payload.get("properties", {})
    if not isinstance(properties, dict):
        raise ValueError("properties must be an object")

    required = payload.get("required", [])
    if not isinstance(required, list):
        raise ValueError("required must be an array")

    validation_result = validate_json_schema(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": payload.get("additionalProperties", True),
        }
    )

    return SchemaAsset(
        schema_id=schema_id,
        name=payload.get("name", schema_id),
        version=version,
        status=status,
        schema_type=schema_type,
        properties=properties,
        required=required,
        validation={
            "is_valid": validation_result["is_valid"],
            "errors": validation_result["errors"],
            "validated_at": now_iso(),
            "validator": "jsonschema.Draft202012Validator",
        },
        references=payload.get("references", []),
    )


@app.get("/")
def index() -> Any:
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/schemas")
def list_schemas() -> Any:
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    schemas = []
    for folder in sorted(p for p in ASSET_ROOT.iterdir() if p.is_dir()):
        versions = sorted(p.stem for p in folder.glob("*.json"))
        if not versions:
            continue
        latest = json.loads((folder / f"{versions[-1]}.json").read_text())
        schemas.append(
            {
                "schema_id": latest["schema_id"],
                "name": latest["name"],
                "latest_version": latest["version"],
                "status": latest["status"],
                "schema_type": latest["schema_type"],
                "version_count": len(versions),
            }
        )
    return jsonify(schemas)


@app.get("/api/schemas/<schema_id>")
def get_schema(schema_id: str) -> Any:
    version = request.args.get("version") or latest_version(schema_id)
    if not version:
        return jsonify({"error": "schema not found"}), 404
    return jsonify(read_asset(schema_id, version))


@app.post("/api/schemas")
def create_schema() -> Any:
    payload = request.get_json(force=True)
    asset = normalize_payload(payload).to_dict()
    path = write_asset(asset)
    return jsonify({"saved": str(path.relative_to(BASE_DIR)), "asset": asset}), 201


@app.post("/api/schemas/<schema_id>/status")
def update_status(schema_id: str) -> Any:
    payload = request.get_json(force=True)
    target_version = payload.get("version") or latest_version(schema_id)
    if not target_version:
        return jsonify({"error": "schema not found"}), 404

    asset = read_asset(schema_id, target_version)
    new_status = payload.get("status")
    if new_status not in ALLOWED_STATUSES:
        return jsonify({"error": f"status must be one of {sorted(ALLOWED_STATUSES)}"}), 400

    asset["status"] = new_status
    asset.setdefault("validation", {})["status_updated_at"] = now_iso()
    path = write_asset(asset)
    return jsonify({"saved": str(path.relative_to(BASE_DIR)), "asset": asset})


@app.get("/api/schemas/<schema_id>/diff")
def diff_versions(schema_id: str) -> Any:
    v1 = request.args.get("v1")
    v2 = request.args.get("v2") or latest_version(schema_id)
    if not v1 or not v2:
        return jsonify({"error": "v1 and v2 are required"}), 400

    before = json.dumps(read_asset(schema_id, v1), indent=2).splitlines(keepends=True)
    after = json.dumps(read_asset(schema_id, v2), indent=2).splitlines(keepends=True)
    diff = "".join(unified_diff(before, after, fromfile=v1, tofile=v2))
    return jsonify({"schema_id": schema_id, "v1": v1, "v2": v2, "diff": diff})


@app.post("/api/schemas/validate")
def validate_schema() -> Any:
    payload = request.get_json(force=True)
    schema_doc = payload.get("schema")
    if not isinstance(schema_doc, dict):
        return jsonify({"error": "schema must be an object"}), 400
    return jsonify(validate_json_schema(schema_doc))


@app.get("/api/schemas/<schema_id>/export")
def export_schema(schema_id: str) -> Any:
    version = request.args.get("version") or latest_version(schema_id)
    format_name = request.args.get("format", "json")
    if not version:
        return jsonify({"error": "schema not found"}), 404

    asset = read_asset(schema_id, version)
    if format_name == "json":
        return app.response_class(json.dumps(asset, indent=2), mimetype="application/json")
    if format_name == "yaml":
        return app.response_class(yaml.safe_dump(asset, sort_keys=False), mimetype="application/yaml")
    return jsonify({"error": "format must be json or yaml"}), 400


@app.post("/api/schemas/import")
def import_schema() -> Any:
    format_name = request.args.get("format", "json")
    raw = request.get_data(as_text=True)
    if format_name == "json":
        payload = json.loads(raw)
    elif format_name == "yaml":
        payload = yaml.safe_load(raw)
    else:
        return jsonify({"error": "format must be json or yaml"}), 400

    asset = normalize_payload(payload).to_dict()
    path = write_asset(asset)
    return jsonify({"saved": str(path.relative_to(BASE_DIR)), "asset": asset}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8787, debug=True)
