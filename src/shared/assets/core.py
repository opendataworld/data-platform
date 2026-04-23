from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_STATUSES = {"draft", "approved", "published"}


class AssetError(Exception):
    """Base class for shared asset helper errors."""


class AssetValidationError(AssetError):
    """Raised when an asset payload fails validation."""


class AssetNotFoundError(AssetError):
    """Raised when an asset file cannot be found."""


@dataclass
class AssetMetadata:
    asset_id: str
    name: str
    version: str
    status: str = "draft"
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(
        cls,
        payload: dict[str, Any],
        *,
        id_key: str,
        name_key: str = "name",
        version_key: str = "version",
        allowed_statuses: set[str] | None = None,
    ) -> "AssetMetadata":
        raw_id = str(payload.get(id_key, "")).strip()
        version = str(payload.get(version_key, "")).strip()
        if not raw_id or not version:
            raise AssetValidationError(f"{id_key} and {version_key} are required")

        name = str(payload.get(name_key) or raw_id).strip()
        status = ensure_status(payload.get("status", "draft"), allowed_statuses=allowed_statuses)
        extra = {k: v for k, v in payload.items() if k not in {id_key, name_key, version_key, "status"}}
        return cls(asset_id=raw_id, name=name, version=version, status=status, extra=extra)


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sanitize_asset_id(value: str, *, separator: str = "-", lower: bool = True) -> str:
    normalized = value.strip().lower() if lower else value.strip()
    normalized = re.sub(r"[^a-z0-9]+" if lower else r"[^A-Za-z0-9]+", separator, normalized).strip(separator)
    if not normalized:
        raise AssetValidationError("asset id must include at least one alphanumeric character")
    return normalized


def ensure_status(status: str, *, allowed_statuses: set[str] | None = None) -> str:
    normalized = str(status).strip().lower()
    allowed = allowed_statuses or DEFAULT_STATUSES
    if normalized not in allowed:
        raise AssetValidationError(f"status must be one of {sorted(allowed)}")
    return normalized


def read_asset_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssetNotFoundError(f"asset file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_asset_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path
