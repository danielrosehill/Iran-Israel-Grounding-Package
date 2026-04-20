"""Research — urgency-scoped retrieval from whitelisted feeds."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import feedparser

from ..schemas import Evidence
from ..state import GroundingState
from ..whitelist import Source, assert_whitelisted, parse_sources

log = logging.getLogger(__name__)


# Tunable by-urgency knobs. Override by editing or by passing a custom dict
# into build().
DEFAULT_WINDOW_HOURS: dict[str, int] = {
    "flash": 6, "priority": 12, "routine": 24, "background": 48,
}
DEFAULT_ITEMS_PER_FEED: dict[str, int] = {
    "flash": 15, "priority": 10, "routine": 8, "background": 5,
}
DEFAULT_TIER_SELECTION: dict[str, set[str]] = {
    "flash": {"primary", "osint", "wire"},
    "priority": {"primary", "osint", "wire", "analysis"},
    "routine": {"primary", "wire", "osint", "analysis", "dissident"},
    "background": {"primary", "wire", "osint", "analysis", "dissident"},
}


def build(
    window_hours: dict[str, int] | None = None,
    items_per_feed: dict[str, int] | None = None,
    tier_selection: dict[str, set[str]] | None = None,
):
    win = window_hours or DEFAULT_WINDOW_HOURS
    per = items_per_feed or DEFAULT_ITEMS_PER_FEED
    tiers = tier_selection or DEFAULT_TIER_SELECTION

    def _node(state: GroundingState) -> GroundingState:
        triage = state["triage"]
        urgency = triage.urgency
        cutoff = datetime.now(timezone.utc) - timedelta(hours=win.get(urgency, 24))

        all_sources = parse_sources()
        selected = [s for s in all_sources if s.tier in tiers.get(urgency, set()) and s.is_rss]
        log.info("research: urgency=%s window=%dh feeds=%d", urgency, win.get(urgency, 24), len(selected))

        evidence: list[Evidence] = []
        for s in selected:
            try:
                assert_whitelisted(s.url, all_sources)
                parsed = feedparser.parse(s.url)
                count = 0
                cap = per.get(urgency, 8)
                for e in parsed.entries:
                    if count >= cap:
                        break
                    dt = None
                    for key in ("published_parsed", "updated_parsed"):
                        if getattr(e, key, None):
                            dt = datetime(*getattr(e, key)[:6], tzinfo=timezone.utc)
                            break
                    if dt and dt < cutoff:
                        continue
                    url = getattr(e, "link", "").strip()
                    if not url:
                        continue
                    try:
                        assert_whitelisted(url, all_sources)
                    except ValueError:
                        continue
                    title = getattr(e, "title", "").strip()
                    summary = getattr(e, "summary", "")[:900].strip()
                    if not title:
                        continue
                    evidence.append(Evidence(
                        source_name=s.name,
                        source_tier=s.tier,
                        url=url,
                        title=title,
                        body_excerpt=summary,
                        fetched_at=datetime.now(timezone.utc),
                        published_at=dt,
                    ))
                    count += 1
            except Exception as ex:
                log.warning("research feed failed: %s — %s", s.name, ex)

        log.info("research: gathered %d evidence items", len(evidence))
        return {**state, "evidence": evidence}

    return _node


run = build()
