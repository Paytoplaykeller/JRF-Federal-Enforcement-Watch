from __future__ import annotations

import json
from pathlib import Path

from jrf_watch.registry import append_candidate, existing_source_urls
from jrf_watch.sources import load_source_config, scan_sources


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "config" / "sources.yaml"
REGISTRY = ROOT / "data" / "registry.csv"
CANDIDATES = ROOT / "data" / "candidates.jsonl"


def main() -> None:
    source_defs = load_source_config(str(SOURCES))
    seen = existing_source_urls(REGISTRY)
    found = scan_sources(source_defs)

    added = 0
    for item in found:
        if item.url in seen:
            continue
        append_candidate(CANDIDATES, item.as_dict())
        added += 1

    print(json.dumps({"discovered": len(found), "new_candidates": added}, indent=2))


if __name__ == "__main__":
    main()
