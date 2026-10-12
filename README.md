# JRF Federal Enforcement Watch

A durable backend for Justice Restoration Foundation's federal-enforcement monitoring workflow.

## Mission

Track meaningful U.S. federal criminal-enforcement developments, preserve a cumulative registry, flag due-process and prosecutorial-accountability issues, prioritize healthcare matters, and prepare concise outreach alerts for JRF.

This repository is the **system of record / analysis backend**. The existing ChatGPT automation remains the live intelligence layer that can browse current sources and email Lucky when a meaningful development appears.

## Core principles

- **Presumption of innocence:** indictments, complaints, and investigations are allegations unless proven or admitted.
- **Healthcare HIGH ALERT:** physicians, Medicare/Medicaid, laboratories, treatment centers, False Claims Act matters, OIG cases, raids, asset restraints, and parallel civil/criminal matters receive priority.
- **Primary sources first:** DOJ, U.S. Attorneys, FBI, OIGs, SEC/CFTC/FTC, court dockets and charging documents.
- **No private-client / Article II information.**
- **No public posting or replying.**
- **Public professional contacts only** for outreach research.
- **Meaningful alerts only:** do not create noise.

## What the code does

1. Scans configured public feeds/pages for new candidate enforcement items.
2. Normalizes reviewed matters into a consistent case schema.
3. Deduplicates matters by case number, subject, source URL, and fingerprint.
4. Scores priority and JRF/P2P relevance.
5. Maintains CSV/JSON registries.
6. Builds Markdown alert reports.
7. Can optionally email HIGH-priority alerts when SMTP secrets are configured.

The source scanner is intentionally conservative. It discovers candidate links and metadata; human/AI review should verify allegations, statutes, procedural posture, and contact information before an item becomes an authoritative registry entry.

## Repository layout

```
config/
  sources.yaml
data/
  registry.csv
  candidates.jsonl
src/jrf_watch/
  models.py
  scoring.py
  registry.py
  sources.py
  reporting.py
  notifier.py
scripts/
  scan_sources.py
  ingest_case.py
  build_report.py
tests/
  test_scoring.py
.github/workflows/
  monitor.yml
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]

python scripts/scan_sources.py
python scripts/build_report.py
pytest
```

## Add a reviewed case

Prepare a JSON file following `examples/case.example.json`, then:

```bash
python scripts/ingest_case.py examples/case.example.json
```

The ingest command validates the record, calculates priority, deduplicates it, and updates `data/registry.csv`.

## Optional email alerts

The notifier supports SMTP but is **off by default**. Configure secrets/environment variables:

- `JRF_SMTP_HOST`
- `JRF_SMTP_PORT`
- `JRF_SMTP_USER`
- `JRF_SMTP_PASSWORD`
- `JRF_ALERT_FROM`
- `JRF_ALERT_TO`
- `JRF_EMAIL_ENABLED=true`

Never store passwords or API keys in this repository.

## Current operating model

**ChatGPT automation** → current-source research + factual verification + Lucky alerts  
**This repository** → durable schema + registry + scoring + dedupe + audit trail + reporting

This avoids pretending a simple scraper can reliably interpret complaints, indictments, plea agreements, docket events, or allegations without contextual review.

## JRF/P2P tags

The scoring engine recognizes issues such as due process, prosecutorial discretion, government overreach, cooperating-witness incentives, whistleblower misuse, parallel civil/criminal pressure, forfeiture, raids, mandatory minimums, public corruption, healthcare enforcement, political sensitivity, and trial/plea leverage.

## Disclaimer

This project is an internal research and outreach tool, not a legal determination that any person was wrongfully prosecuted. Allegations must remain clearly distinguished from proven or admitted facts.
