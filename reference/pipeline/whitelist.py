"""Parse grounding-set.md into structured source lists.

Sources are tiered by the markdown section they appear under. The parser
is topic-agnostic — it uses the heading structure, not the topic content.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


_DEFAULT_GROUNDING_SET = (
    Path(__file__).resolve().parents[2] / "grounding-set.md"
)
GROUNDING_SET_PATH = Path(
    os.environ.get("GROUNDING_SET_PATH", str(_DEFAULT_GROUNDING_SET))
)


@dataclass
class Source:
    name: str
    url: str
    tier: str
    is_rss: bool


# Heading → tier mapping. Extend or override for your own whitelist.
DEFAULT_TIER_MAP: dict[str, str] = {
    "Primary state — Israel / US / allies": "primary",
    "Primary state — Iran / Axis of Resistance": "primary",
    "Primary state — Lebanon / international bodies": "primary",
    "Wire & regional reporting": "wire",
    "OSINT synthesis": "osint",
    "Analysis — spanning the spectrum": "analysis",
    "Dissident & opposition": "dissident",
}


def _looks_like_feed(url: str) -> bool:
    u = url.lower()
    return (
        u.endswith((".xml", "/rss", "/feed", "/feed/"))
        or "/rss/" in u
        or "/feed/" in u
        or "rss2" in u
        or "?feed=" in u
    )


def parse_sources(
    path: Path | None = None,
    tier_map: dict[str, str] | None = None,
) -> list[Source]:
    tier_map = tier_map or DEFAULT_TIER_MAP
    md = (path or GROUNDING_SET_PATH).read_text()
    name_url = re.compile(
        r"\*\*(?P<name>[^*]+)\*\*[^`<]*(?:`(?P<url1>[^`]+)`|<(?P<url2>https?://[^>]+)>)"
    )
    current_tier: str | None = None
    out: list[Source] = []

    for line in md.splitlines():
        if line.startswith("## "):
            current_tier = tier_map.get(line.lstrip("# ").strip())
            continue
        if not current_tier:
            continue
        m = name_url.search(line)
        if not m:
            continue
        name = m.group("name").strip()
        url = (m.group("url1") or m.group("url2") or "").strip()
        if not url:
            continue
        try:
            urlparse(url)
        except Exception:
            continue
        out.append(Source(name=name, url=url, tier=current_tier, is_rss=_looks_like_feed(url)))
    return out


def whitelist_hosts(sources: list[Source] | None = None) -> set[str]:
    sources = sources or parse_sources()
    hosts: set[str] = set()
    for s in sources:
        host = urlparse(s.url).netloc.lower().removeprefix("www.")
        if host:
            hosts.add(host)
    return hosts


def assert_whitelisted(url: str, sources: list[Source] | None = None) -> None:
    hosts = whitelist_hosts(sources)
    host = urlparse(url).netloc.lower().removeprefix("www.")
    if host not in hosts and not any(host.endswith("." + h) for h in hosts):
        raise ValueError(f"URL not whitelisted: {url} (host={host})")


if __name__ == "__main__":
    srcs = parse_sources()
    for s in srcs:
        kind = "RSS" if s.is_rss else "   "
        print(f"[{s.tier:9}] {kind} {s.name} -- {s.url}")
    print(f"\n{len(srcs)} sources, {sum(1 for s in srcs if s.is_rss)} RSS")
