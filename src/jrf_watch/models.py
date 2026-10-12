from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class ProofPosture(str, Enum):
    ALLEGATION = "allegation"
    ADMITTED = "admitted"
    PROVEN = "proven"
    MIXED = "mixed"


class EnforcementCase(BaseModel):
    subject: str
    status: str
    charging_agency: str = ""
    us_attorneys_office: str = ""
    court: str = ""
    case_number: str = ""
    charges_statutes: str = ""
    factual_allegations_or_admissions: str = ""
    victims_or_public_harm: str = ""
    trigger_or_referral: str = ""
    cooperators_whistleblowers_competitors_political: str = ""
    warrants_subpoenas_raids: str = ""
    key_dates: str = ""
    potential_sentence: str = ""
    primary_source: Optional[HttpUrl] = None
    reporting_source: Optional[HttpUrl] = None
    jrf_relevance: str = ""
    proof_posture: ProofPosture = ProofPosture.ALLEGATION
    healthcare: bool = False
    public_professional_email: str = ""
    public_counsel_or_contact: str = ""
    counsel_email: str = ""
    public_phone: str = ""
    outreach_status: str = "RESEARCH"
    tags: List[str] = Field(default_factory=list)
    first_seen: date = Field(default_factory=date.today)
    last_updated: date = Field(default_factory=date.today)
    priority: str = "MEDIUM"

    def source_urls(self) -> list[str]:
        return [str(url) for url in (self.primary_source, self.reporting_source) if url is not None]
