"""Writer — synthesise a grounded SitrepDraft from triage + evidence.

Swap DEFAULT_WRITER_PROMPT for your own, or pass prompt= into build().
The prompt should specify exactly the output shape so the LLM returns
valid JSON matching SitrepDraft (or your extension of it).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from ..llm import complete_json
from ..schemas import SitrepDraft
from ..state import GroundingState

log = logging.getLogger(__name__)


DEFAULT_WRITER_PROMPT = """You are the writer node of a grounding pipeline.

You will receive:
  (a) a triage assessment (urgency, hot topics, justification)
  (b) a list of evidence items from a whitelisted source set

Produce a situation report grounded STRICTLY in the evidence provided.
Do not invent facts, names, dates, or numbers. If sources contradict,
report the contradiction. If a topic lacks coverage, say so in a "Gaps"
section rather than speculating.

Tone: neutral, concise, analytical — the voice of an intelligence SITREP,
not commentary. Avoid hedging that adds no information.

Return STRICT JSON matching this schema:

  title         — short intel-style headline
  bluf          — 1-2 sentence bottom line up front
  topline       — one paragraph (4-6 sentences) of the key developments
  sections      — array of {key, title, body}. Markdown in body. Cite
                  sources inline as [Source Name].
  sources       — array of {name, url} covering every source cited
  urgency       — echo triage.urgency
"""


def _render_evidence_block(evidence) -> str:
    if not evidence:
        return "(no evidence collected)"
    out = []
    for i, ev in enumerate(evidence, 1):
        when = ev.published_at.isoformat() if ev.published_at else "?"
        out.append(
            f"[{i}] {ev.source_name} ({ev.source_tier}) — {when}\n"
            f"    {ev.title}\n"
            f"    URL: {ev.url}\n"
            f"    Excerpt: {ev.body_excerpt[:500]}"
        )
    return "\n\n".join(out)


def build(prompt: str = DEFAULT_WRITER_PROMPT, model: type = SitrepDraft):
    """Return a writer node bound to the given prompt and pydantic output model.

    The prompt must instruct the LLM to emit fields matching `model`.
    Defaults to SitrepDraft; pass your own subclass to extend the shape
    (e.g. add tags, scoring) without rewriting the node.
    """

    def _node(state: GroundingState) -> GroundingState:
        triage = state["triage"]
        evidence = state.get("evidence", [])
        now = datetime.now(timezone.utc)

        user = (
            f"CURRENT TIME (UTC): {now.isoformat()}\n\n"
            f"TRIAGE:\n"
            f"  urgency: {triage.urgency}\n"
            f"  flagged: {triage.flagged}\n"
            f"  hot_topics: {triage.hot_topics}\n"
            f"  justification: {triage.justification}\n\n"
            f"EVIDENCE (grounded SITREP must cite these):\n{_render_evidence_block(evidence)}\n"
        )
        data = complete_json(prompt, user, temperature=0.4, max_tokens=6000)
        data["urgency"] = triage.urgency
        data.setdefault("issued_at_utc", now.isoformat())
        draft = model.model_validate(data)
        log.info("writer: title=%r urgency=%s sections=%d",
                 draft.title, draft.urgency, len(draft.sections))
        return {**state, "sitrep": draft}

    return _node


run = build()
