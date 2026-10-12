from __future__ import annotations

from datetime import date
from pathlib import Path

from .registry import load_registry


def _truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def build_markdown_report(registry_path: Path, high_only: bool = True) -> str:
    rows = load_registry(registry_path)
    if high_only:
        rows = [r for r in rows if r.get("priority") == "HIGH"]
    rows.sort(key=lambda r: r.get("last_updated", ""), reverse=True)

    lines = [
        f"# JRF Federal Enforcement Watch — {date.today().isoformat()}",
        "",
        f"Tracked matters in this report: **{len(rows)}**",
        "",
    ]

    for row in rows:
        health = " — HEALTHCARE HIGH ALERT" if _truthy(row.get("healthcare", "")) else ""
        lines.extend([
            f"## {row.get('subject', 'Unknown')}{health}",
            f"**Status:** {row.get('status', '')}",
            f"**Court / case:** {row.get('court', '')} {row.get('case_number', '')}".strip(),
            f"**Charges / statutes:** {row.get('charges_statutes', '')}",
            f"**Facts:** {row.get('factual_allegations_or_admissions', '')}",
            f"**Trigger / referral:** {row.get('trigger_or_referral', '') or 'Not publicly disclosed / not recorded'}",
            f"**Cooperators / whistleblowers / political actors:** {row.get('cooperators_whistleblowers_competitors_political', '') or 'None publicly documented / not recorded'}",
            f"**Warrants / subpoenas / raids:** {row.get('warrants_subpoenas_raids', '') or 'None publicly confirmed / not recorded'}",
            f"**Potential sentence:** {row.get('potential_sentence', '') or 'Not officially stated / not recorded'}",
            f"**JRF/P2P relevance:** {row.get('jrf_relevance', '')}",
            f"**Proof posture:** {row.get('proof_posture', '')}",
            f"**Primary source:** {row.get('primary_source', '')}",
            f"**Reporting:** {row.get('reporting_source', '')}",
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"
