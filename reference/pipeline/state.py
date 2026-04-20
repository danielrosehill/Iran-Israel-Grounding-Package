from __future__ import annotations

from datetime import datetime, timezone
from typing import TypedDict

from .schemas import Evidence, SitrepDraft, TriageResult


class GroundingState(TypedDict, total=False):
    now: datetime
    triage: TriageResult
    evidence: list[Evidence]
    sitrep: SitrepDraft


def initial_state() -> GroundingState:
    return GroundingState(
        now=datetime.now(timezone.utc),
        evidence=[],
    )
