# Iran-Israel-Grounding-Package

A curated whitelist of URLs and sources for AI agents grounding analysis of the **Iran–Israel–US geopolitical conflict (2026)**.

- `AGENTS.md` — instructions for AI agents fetching this repo
- `sources.md` — the full whitelisted source list
- `grounding-set.md` — the recommended curated subset (default grounding surface)
- `.claude/skills/generate-sitrep/` — skill that produces a UTC-timestamped SITREP in a format customised for Iran–Israel–US war monitoring
- `pipeline-design.md` — LangGraph pipeline design (triage → deep research → SITREP → analyst) that consumes this whitelist

## Suggested pathways

- **Pathway A — Monitoring loop**: full graph on a 3h cadence, triage-gated deep research, stream of SITREPs. Pairs with [Geopol-Forecaster](https://github.com/danielrosehill/Geopol-Forecaster) (actor simulation).
- **Pathway B — One-shot retrieval**: skip triage/scheduler, caller supplies `(frames, window)`, graph runs once. Pairs with [Geopol-Forecast-Council](https://github.com/danielrosehill/Geopol-Forecast-Council) (panel forecast).

See `pipeline-design.md` for the handoff contract, tool-stack minimalism notes, and the trailing-hours retrieval-window problem.
