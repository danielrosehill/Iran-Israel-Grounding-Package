"""LangGraph composition — triage → [gate] → research → writer → END."""
from __future__ import annotations

import logging

from langgraph.graph import END, START, StateGraph

from .nodes import research as research_node
from .nodes import triage as triage_node
from .nodes import writer as writer_node
from .state import GroundingState

log = logging.getLogger(__name__)


def _gate(state: GroundingState) -> str:
    triage = state["triage"]
    if not triage.flagged and triage.urgency == "background":
        log.info("gate: heartbeat — skipping write path")
        return "skip"
    return "proceed"


def build_graph(
    triage=triage_node.run,
    research=research_node.run,
    writer=writer_node.run,
):
    g = StateGraph(GroundingState)
    g.add_node("triage", triage)
    g.add_node("research", research)
    g.add_node("writer", writer)

    g.add_edge(START, "triage")
    g.add_conditional_edges("triage", _gate, {"proceed": "research", "skip": END})
    g.add_edge("research", "writer")
    g.add_edge("writer", END)
    return g.compile()
