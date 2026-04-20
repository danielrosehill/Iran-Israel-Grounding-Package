"""Generic data shapes. Deliberately minimal — extend for your use case."""
from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

Urgency = Literal["flash", "priority", "routine", "background"]


class TriageResult(BaseModel):
    urgency: Urgency
    flagged: bool = Field(
        description="True if the window warrants full retrieval + write; false = heartbeat.",
    )
    hot_topics: list[str] = Field(default_factory=list)
    justification: str


class Evidence(BaseModel):
    source_name: str
    source_tier: str
    url: str
    fetched_at: datetime
    title: str
    body_excerpt: str
    published_at: Optional[datetime] = None


class SitrepSection(BaseModel):
    key: str
    title: str
    body: str


class SitrepSourceRef(BaseModel):
    name: str
    url: str


class SitrepDraft(BaseModel):
    """Generic output shape. Consumers should extend as needed."""
    title: str
    bluf: str
    topline: str
    sections: list[SitrepSection]
    sources: list[SitrepSourceRef]
    urgency: Urgency
    issued_at_utc: datetime
