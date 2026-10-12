from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from .models import EnforcementCase
from .scoring import score_case


FIELD_ORDER = [
    "priority","subject","status","charging_agency","us_attorneys_office","court",
    "case_number","charges_statutes","factual_allegations_or_admissions",
    "victims_or_public_harm","trigger_or_referral",
    "cooperators_whistleblowers_competitors_political","warrants_subpoenas_raids",
    "key_dates","potential_sentence","primary_source","reporting_source",
    "jrf_relevance","proof_posture","healthcare","public_professional_email",
    "public_counsel_or_contact","counsel_email","public_phone","outreach_status",
    "tags","first_seen","last_updated","fingerprint",
]


def _clean(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " | ".join(str(x) for x in value)
    if hasattr(value, "value"):
        return str(value.value)
    return str(value)


def fingerprint(case: EnforcementCase) -> str:
    stable = "|".join([
        case.subject.strip().lower(),
        case.case_number.strip().lower(),
        (str(case.primary_source) if case.primary_source else "").lower(),
        case.charges_statutes.strip().lower(),
    ])
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()[:20]


def load_registry(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def upsert_case(path: Path, case: EnforcementCase) -> tuple[str, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    case.priority = score_case(case).priority
    fp = fingerprint(case)
    rows = load_registry(path)

    idx = next((i for i, row in enumerate(rows) if row.get("fingerprint") == fp or (
        case.case_number
        and row.get("case_number", "").strip().lower() == case.case_number.strip().lower()
        and row.get("subject", "").strip().lower() == case.subject.strip().lower()
    )), None)

    payload = case.model_dump(mode="json")
    row = {key: _clean(payload.get(key, "")) for key in FIELD_ORDER}
    row["fingerprint"] = fp

    action = "inserted"
    if idx is None:
        rows.append(row)
    else:
        row["first_seen"] = rows[idx].get("first_seen") or row["first_seen"]
        rows[idx] = row
        action = "updated"

    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELD_ORDER)
        writer.writeheader()
        writer.writerows(rows)

    return action, fp


def append_candidate(path: Path, item: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(item, ensure_ascii=False) + "\n")


def existing_source_urls(path: Path) -> set[str]:
    urls: set[str] = set()
    for row in load_registry(path):
        for key in ("primary_source", "reporting_source"):
            if row.get(key):
                urls.add(row[key])
    return urls
