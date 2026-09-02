import json
import sys
from pathlib import Path

# Ensure backend root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Project root (where docs/ directory lives)
PROJECT_ROOT = BASE_DIR.parent
DOCS_DIR = PROJECT_ROOT / "docs"

from app.main import app

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def export_openapi():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    openapi_schema = app.openapi()

    # 1. Export as JSON
    json_path = DOCS_DIR / "api-spec.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    print(f"[+] Exported OpenAPI JSON specification to: {json_path}")

    # 2. Export as YAML if PyYAML is available
    if HAS_YAML:
        yaml_path = DOCS_DIR / "api-spec.yaml"
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(openapi_schema, f, sort_keys=False, allow_unicode=True)
        print(f"[+] Exported OpenAPI YAML specification to: {yaml_path}")


if __name__ == "__main__":
    export_openapi()
