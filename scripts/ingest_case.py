from __future__ import annotations

import json
import sys
from pathlib import Path

from jrf_watch.models import EnforcementCase
from jrf_watch.registry import upsert_case
from jrf_watch.scoring import score_case


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "registry.csv"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/ingest_case.py <case.json>")

    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    case = EnforcementCase.model_validate(payload)
    score = score_case(case)
    action, fp = upsert_case(REGISTRY, case)

    print(json.dumps({
        "action": action,
        "fingerprint": fp,
        "priority": score.priority,
        "healthcare_high_alert": score.healthcare_high_alert,
        "reasons": score.reasons,
    }, indent=2))


if __name__ == "__main__":
    main()
