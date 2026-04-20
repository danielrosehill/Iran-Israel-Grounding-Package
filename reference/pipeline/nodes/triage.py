"""Triage — poll a top-tier feed panel, classify urgency.

Edit TRIAGE_FEEDS for your topic. The default set below is illustrative
(the Iran-Israel-US topic the parent repo is focused on); swap it out
for a different one before adapting to a new subject.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import feedparser

from ..llm import complete_json
from ..schemas import TriageResult
from ..state import GroundingState

log = logging.getLogger(__name__)

# (display name, feed URL) — illustrative top-tier panel for this repo's topic.
TRIAGE_FEEDS: list[tuple[str, str]] = [
    ("Times of Israel — Region", "https://www.timesofisrael.com/israel-and-the-region/feed/"),
    ("Haaretz", "https://www.haaretz.com/srv/haaretz-latest-headlines"),
    ("Al Jazeera English", "https://www.aljazeera.com/xml/rss/all.xml"),
    ("Tasnim", "https://www.tasnimnews.com/en/rss/feed/0/7/0/"),
    ("Al-Manar", "https://english.almanar.com.lb/rss"),
    ("Long War Journal — Israel tag", "https://www.longwarjournal.org/tags/israel/feed"),
    ("Bellingcat", "https://www.bellingcat.com/feed/"),
    ("Iran International", "https://www.iranintl.com/en/rss.xml"),
]


DEFAULT_TRIAGE_PROMPT = """You are the triage node of a grounding pipeline. \
Given recent headlines from whitelisted sources, assess the window:

- Is anything escalatory, kinetic, or materially new relative to baseline?
- What urgency level is warranted?

Urgency scale:
  flash       — read now. Kinetic escalation, strike exchange, leader death,
                nuclear/CBRN signal, treaty rupture.
  priority    — read today. Named operation, diplomatic break, mobilisation.
  routine     — read this week. Policy shifts, ongoing posture, notable analysis.
  background  — reference. Slow day, retrospective, no real escalation.

Return STRICT JSON:
  urgency: "flash" | "priority" | "routine" | "background"
  flagged: boolean            (true if a full write-up is warranted)
  hot_topics: string[]        (2-6 short phrases)
  justification: string       (2-3 sentences)
"""


def _fetch_headlines(hours: int = 24) -> list[tuple[str, str, str, str]]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    rows: list[tuple[str, str, str, str]] = []
    for name, url in TRIAGE_FEEDS:
        try:
            parsed = feedparser.parse(url)
            for e in parsed.entries[:15]:
                dt = None
                for key in ("published_parsed", "updated_parsed"):
                    if getattr(e, key, None):
                        dt = datetime(*getattr(e, key)[:6], tzinfo=timezone.utc)
                        break
                if dt and dt < cutoff:
                    continue
                title = getattr(e, "title", "").strip()
                summary = getattr(e, "summary", "")[:280].strip()
                if title:
                    rows.append((name, dt.isoformat() if dt else "", title, summary))
        except Exception as ex:
            log.warning("triage feed failed: %s — %s", name, ex)
    return rows


def build(prompt: str = DEFAULT_TRIAGE_PROMPT):
    """Return a triage node bound to the given system prompt."""

    def _node(state: GroundingState) -> GroundingState:
        headlines = _fetch_headlines()
        log.info("triage fetched %d headlines across %d feeds", len(headlines), len(TRIAGE_FEEDS))
        block = "\n".join(
            f"- [{src}] ({when}) {title}  {summary[:160]}"
            for (src, when, title, summary) in headlines[:120]
        )
        user = f"Window: last 24 hours, {len(headlines)} headlines.\n\n{block}"
        data = complete_json(prompt, user, temperature=0.2, max_tokens=700)
        triage = TriageResult.model_validate(data)
        log.info("triage: urgency=%s flagged=%s", triage.urgency, triage.flagged)
        return {**state, "triage": triage}

    return _node


run = build()
