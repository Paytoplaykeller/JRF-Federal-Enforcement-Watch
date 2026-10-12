from __future__ import annotations

from pathlib import Path

from jrf_watch.reporting import build_markdown_report


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "registry.csv"
REPORTS = ROOT / "reports"


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    report = build_markdown_report(REGISTRY, high_only=True)
    output = REPORTS / "latest.md"
    output.write_text(report, encoding="utf-8")
    print(output)
    print(report)


if __name__ == "__main__":
    main()
