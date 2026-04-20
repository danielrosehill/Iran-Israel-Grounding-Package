# Reference pipeline

A minimal runnable reference of the grounding pattern described in this
repo's root `README.md`. It is intentionally **generic** — it demonstrates
how to compose triage → research → writer against a whitelist, without any
project-specific coupling (no publishing, no tagging schema, no CAMEO
scoring, no database).

Use this as a starting point when adapting the pattern to a new topic.

## Shape

```
START → triage → [gate] → research → writer → END
                    ↓
                  (heartbeat: skip to END on quiet window)
```

- **triage** polls a small panel of feeds, returns `TriageResult`
  (urgency + flagged boolean + topics + justification).
- **research** pulls recent items from whitelisted feeds, scoped by urgency.
  Every URL is hard-gated against the whitelist's hostnames.
- **writer** synthesises a `SitrepDraft` grounded in the evidence, using a
  pluggable system prompt.
- **output** is a JSON `SitrepDraft` printed to stdout. Wire it into your
  own publishing step (HTTP POST, git commit, file write, Telegram, etc.).

## Run

```bash
cp .env.example .env                 # OPENROUTER_API_KEY
uv sync
uv run python -m pipeline.cli run    # full pipeline, prints JSON
uv run python -m pipeline.cli triage # triage only
uv run python -m pipeline.whitelist  # list parsed whitelist entries
```

## Adapting to another topic

1. Replace `../grounding-set.md` and `../sources.md` with your whitelist.
2. Edit `pipeline/nodes/triage.py::TRIAGE_FEEDS` for your top-tier panel.
3. Edit `pipeline/nodes/writer.py::DEFAULT_WRITER_PROMPT` or inject your
   own prompt via `build_writer(prompt=...)`.
4. Extend `SitrepDraft` if your downstream consumer needs structured fields
   beyond `title / bluf / topline / sections / sources`.
5. Add your publishing step outside the graph (`cli.py` is the place —
   after `graph.invoke(state)` returns).

## What this reference does NOT include

- No publishing. Your downstream consumer decides what to do with the JSON.
- No tagging taxonomy. Tags are project-specific editorial decisions.
- No event intensity / severity / CAMEO scoring. Add in your own writer
  prompt if you want them.
- No persistence or deduplication.
- No caching or retrieval-window state machine. The `README.md` in the
  repo root sketches a LangGraph-based loop with `last_report_ts`
  state for a longer-running deployment.

For a concrete, SITREP_ISR-specific adaptation of this pattern, see:
[`SITREP_ISR/agent/`](https://github.com/danielrosehill/SITREP_ISR/tree/main/agent)
