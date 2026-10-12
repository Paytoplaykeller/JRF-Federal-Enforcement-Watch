from jrf_watch.models import EnforcementCase
from jrf_watch.scoring import score_case


def test_healthcare_is_always_high_alert():
    case = EnforcementCase(
        subject="Dr. Example",
        status="indictment",
        charges_statutes="18 U.S.C. § 1347",
        factual_allegations_or_admissions="Alleged Medicare fraud",
        healthcare=True,
    )
    score = score_case(case)
    assert score.priority == "HIGH"
    assert score.healthcare_high_alert is True


def test_government_power_indicators_raise_priority():
    case = EnforcementCase(
        subject="Example",
        status="criminal complaint",
        warrants_subpoenas_raids="Search warrant and asset seizure confirmed",
        cooperators_whistleblowers_competitors_political="Cooperating witness documented",
        jrf_relevance="Due process and prosecutorial discretion",
    )
    score = score_case(case)
    assert score.priority == "HIGH"
