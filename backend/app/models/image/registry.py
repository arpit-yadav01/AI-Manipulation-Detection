import json
from pathlib import Path

BASE_DIR = Path(__file__).parent


def get_active_image_model_dir() -> Path:
    registry_path = BASE_DIR / "registry.json"

    with open(registry_path, "r") as f:
        registry = json.load(f)

    version = registry["active_version"]
    model_dir = BASE_DIR / version

    if not model_dir.exists():
        raise FileNotFoundError(f"Active model directory not found: {model_dir}")

    return model_dir


def get_active_image_model_version() -> str:
    registry_path = BASE_DIR / "registry.json"

    with open(registry_path, "r") as f:
        registry = json.load(f)

    return str(registry["active_version"])
