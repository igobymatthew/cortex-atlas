from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

from backend.core.pipeline import run_pipeline


def _load_documents(path: Path) -> Iterable[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "documents" in payload:
        return payload["documents"]
    if isinstance(payload, list):
        return payload
    raise ValueError("Input JSON must be a list of documents or an object with a 'documents' key.")


def _model_to_dict(model: Any) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump(by_alias=True)
    return model.dict(by_alias=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Cortex Atlas pipeline on a JSON file.")
    parser.add_argument("path", type=Path, help="Path to a JSON file containing documents.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the JSON output.")
    args = parser.parse_args()

    documents = _load_documents(args.path)
    report = run_pipeline(documents)
    payload = _model_to_dict(report)
    indent = 2 if args.pretty else None
    print(json.dumps(payload, indent=indent))


if __name__ == "__main__":
    main()
