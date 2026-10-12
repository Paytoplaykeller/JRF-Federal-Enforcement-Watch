from __future__ import annotations

from dataclasses import dataclass

from .models import EnforcementCase


HEALTHCARE_TERMS = {
    "healthcare", "health care", "medicare", "medicaid", "physician", "doctor",
    "hospital", "laboratory", "lab", "telemedicine", "telehealth", "pharmacy",
    "false claims act", "qui tam", "hhs-oig", "dme", "durable medical",
}

POWER_TERMS = {
    "raid", "search warrant", "seizure", "forfeiture", "asset restraint",
    "subpoena", "grand jury", "public corruption", "bribery", "whistleblower",
    "cooperating witness", "confidential informant", "mandatory minimum",
    "superseding indictment", "parallel civil", "political", "official",
    "inspector general", "oig", "trial", "mistrial",
}

HIGH_VALUE_STATUSES = {
    "criminal complaint", "indictment", "superseding indictment", "information",
    "guilty plea", "conviction", "dismissal", "mistrial", "acquittal",
}


@dataclass(frozen=True)
class Score:
    points: int
    priority: str
    healthcare_high_alert: bool
    reasons: list[str]


def score_case(case: EnforcementCase) -> Score:
    text = " ".join([
        case.status, case.charging_agency, case.us_attorneys_office,
        case.charges_statutes, case.factual_allegations_or_admissions,
        case.victims_or_public_harm, case.trigger_or_referral,
        case.cooperators_whistleblowers_competitors_political,
        case.warrants_subpoenas_raids, case.jrf_relevance, " ".join(case.tags),
    ]).lower()

    points = 0
    reasons: list[str] = []

    healthcare = case.healthcare or any(term in text for term in HEALTHCARE_TERMS)
    if healthcare:
        points += 5
        reasons.append("healthcare HIGH ALERT")

    if any(s in case.status.lower() for s in HIGH_VALUE_STATUSES):
        points += 2
        reasons.append("significant procedural event")

    power_hits = sorted(term for term in POWER_TERMS if term in text)
    if power_hits:
        points += min(5, len(power_hits))
        reasons.append("government-power / accountability indicators")

    if case.cooperators_whistleblowers_competitors_political.strip():
        points += 2
        reasons.append("cooperator / whistleblower / political dimension")

    if case.warrants_subpoenas_raids.strip():
        points += 2
        reasons.append("confirmed coercive investigative process")

    if case.trigger_or_referral.strip():
        points += 1
        reasons.append("documented investigative trigger/referral")

    if case.proof_posture.value in {"admitted", "proven"}:
        points += 1
        reasons.append("adjudicated/admitted factual record")

    priority = "HIGH" if points >= 7 else "MEDIUM" if points >= 4 else "LOW"
    if healthcare:
        priority = "HIGH"

    return Score(points, priority, healthcare, reasons)
