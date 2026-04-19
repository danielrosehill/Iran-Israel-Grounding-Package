# Iran-Israel-Grounding-Package

A curated whitelist of URLs and sources for AI agents grounding analysis of the **Iran–Israel–US geopolitical conflict (2026)**.

- `AGENTS.md` — instructions for AI agents fetching this repo
- `sources.md` — the full whitelisted source list
- `grounding-set.md` — the recommended curated subset (default grounding surface)
- `.claude/skills/generate-sitrep/` — skill that produces a UTC-timestamped SITREP in a format customised for Iran–Israel–US war monitoring
- `pipeline-design.md` — LangGraph pipeline design (triage → deep research → SITREP → analyst) that consumes this whitelist

## Suggested pairing

Pairs with **[Geopol-Forecast-Council](https://github.com/danielrosehill/Geopol-Forecast-Council)** as its grounding layer — the SITREP produced by this pipeline slots directly into the Council's five-model panel forecast stage, replacing its ad-hoc RSS+Sonar+Tavily grounding with a curated whitelist.
