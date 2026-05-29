import importlib
import json
from pathlib import Path


REGISTRY_PATH = Path(__file__).resolve().parents[1] / "formula_versions" / "registry.json"


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_formula(version_id):
    registry = load_registry()
    versions = registry.get("versions", {})
    if version_id not in versions:
        raise KeyError(f"Unknown formula version: {version_id}")
    module_name = versions[version_id]["module"]
    module = importlib.import_module(module_name)
    return module


def list_versions(active_only=True):
    registry = load_registry()
    out = []
    for version_id, meta in registry.get("versions", {}).items():
        if active_only and not meta.get("active", False):
            continue
        out.append(version_id)
    return out
