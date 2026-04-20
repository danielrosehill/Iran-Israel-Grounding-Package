"""CLI — prints a JSON SitrepDraft to stdout (no publishing).

Wire your own publishing step into this file after graph.invoke() returns,
or call build_graph() from your own entry point.
"""
from __future__ import annotations

import logging
from pathlib import Path

import typer
from dotenv import load_dotenv

from .graph import build_graph
from .state import initial_state

app = typer.Typer(add_completion=False)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-7s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pipeline.cli")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@app.command()
def run():
    """Run triage → research → writer. Print JSON to stdout."""
    graph = build_graph()
    state = graph.invoke(initial_state())

    if "sitrep" not in state:
        log.info("heartbeat — no SITREP produced")
        print(state["triage"].model_dump_json(indent=2))
        return

    print(state["sitrep"].model_dump_json(indent=2))


@app.command()
def triage():
    """Run only the triage node."""
    from .nodes.triage import run as triage_run
    state = triage_run(initial_state())
    print(state["triage"].model_dump_json(indent=2))


if __name__ == "__main__":
    app()
