from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable
from urllib.parse import urljoin

import feedparser
import httpx
import yaml
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class Candidate:
    source_name: str
    title: str
    url: str
    published: str = ""
    summary: str = ""
    discovered_at: str = ""

    def as_dict(self) -> dict[str, str]:
        return self.__dict__.copy()


def load_source_config(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as fh:
        return (yaml.safe_load(fh) or {}).get("sources", [])


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def scan_feed(source: dict) -> list[Candidate]:
    parsed = feedparser.parse(source["url"])
    items: list[Candidate] = []
    for entry in parsed.entries[:source.get("max_items", 25)]:
        url = entry.get("link", "")
        if not url:
            continue
        items.append(Candidate(
            source_name=source["name"],
            title=entry.get("title", "").strip(),
            url=url,
            published=entry.get("published", entry.get("updated", "")),
            summary=entry.get("summary", "")[:1200],
            discovered_at=_now(),
        ))
    return items


def scan_page(source: dict) -> list[Candidate]:
    response = httpx.get(
        source["url"],
        headers={"User-Agent": "JRF-Federal-Enforcement-Watch/0.1 (+research)"},
        follow_redirects=True,
        timeout=source.get("timeout", 20),
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    selector = source.get("link_selector", "a")
    include = [s.lower() for s in source.get("include_terms", [])]
    exclude = [s.lower() for s in source.get("exclude_terms", [])]

    seen: set[str] = set()
    items: list[Candidate] = []
    for anchor in soup.select(selector):
        href = anchor.get("href")
        title = " ".join(anchor.stripped_strings)
        if not href or not title:
            continue
        haystack = f"{title} {href}".lower()
        if include and not any(term in haystack for term in include):
            continue
        if exclude and any(term in haystack for term in exclude):
            continue
        url = urljoin(source["url"], href)
        if url in seen:
            continue
        seen.add(url)
        items.append(Candidate(source["name"], title[:500], url, discovered_at=_now()))
        if len(items) >= source.get("max_items", 25):
            break
    return items


def scan_sources(source_defs: Iterable[dict]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for source in source_defs:
        if source.get("enabled", True) is False:
            continue
        try:
            if source.get("kind", "page") == "feed":
                candidates.extend(scan_feed(source))
            else:
                candidates.extend(scan_page(source))
        except Exception as exc:
            candidates.append(Candidate(
                source_name=source.get("name", "unknown"),
                title=f"[SCAN ERROR] {type(exc).__name__}: {exc}",
                url=source.get("url", ""),
                discovered_at=_now(),
            ))
    return candidates
