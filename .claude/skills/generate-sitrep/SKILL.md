---
name: generate-sitrep
description: Generate a situation report (SITREP) on the Iran–Israel–US conflict from the grounding sources in this repo. Use when the user asks for a SITREP, intel brief, situation update, conflict snapshot, or daily/hourly rollup on the war. Polls the recommended grounding set, triangulates across adversarial framings, and emits a structured UTC-timestamped SITREP in the format defined below.
---

# generate-sitrep

Produces a structured situation report on the Iran–Israel–US conflict, grounded in the curated sources defined in `grounding-set.md` (fall through to `sources.md` only when the default set leaves a gap).

## When to run

- User asks for a "SITREP", "sitrep", "intel brief", "situation update", "daily brief", "hourly brief", "war update", "conflict snapshot".
- User specifies a window ("last 6h", "since yesterday", "past 24h") — use that window. Default: last 24h.
- User specifies a theatre focus ("Lebanon front", "Red Sea / Houthi", "nuclear file", "sanctions") — narrow scope accordingly, but still cover the **Indicators & Warnings** section (escalation signal is cross-theatre by nature).

## Source discipline

1. **Default surface** = `grounding-set.md`. Poll that first, in the order: primary state → wire → OSINT → analysis → dissident.
2. **Triangulate always.** Every kinetic or casualty claim must be checked against the opposing-framing source before inclusion. Record the divergence explicitly in the *Narrative divergence* section — do not silently pick a side.
3. **Primary beats wire.** If Reuters/AP (via proxy outlets) cites an IDF statement, IAEA report, CENTCOM readout, or OFAC action — re-fetch the primary document and cite that.
4. **ISW / CTP Iran Update** is the daily synthesis anchor. Cite the latest Iran Update Special Report once per SITREP if published in-window.
5. **Iran SITREP (iransitrep.com)** is a lead surface only; never the sole citation for a claim.
6. **Fall through** to the broader `sources.md` inventory only when `grounding-set.md` has no coverage of a specific incident. Fall through to search-layer MCPs (Perplexity / Tavily / Exa) only when both have gaps — see `sources.md § Usage rules for search MCPs`.

## Output format

Emit the SITREP as markdown, saved to `outputs/sitreps/SITREP-<YYYY-MM-DD>-<HHMM>Z.md` (create the directory if missing). Also print it inline for the user.

All timestamps throughout the document are **UTC, ISO-8601, with explicit `Z` suffix** (e.g. `2026-04-19T14:32Z`). Never use local time. If a source reports a local time, convert to UTC and note the source timezone in parentheses on first use.

### Header

```
# SITREP — Iran–Israel–US Conflict
**Generated (UTC):** <YYYY-MM-DD HH:MMZ>
**Reporting window:** <start UTC> → <end UTC>
**Scope:** <theatre focus or "full">
**Confidence:** <overall Low / Medium / High — based on source agreement across the window>
```

### Section 1 — BLUF (Bottom Line Up Front)

Three bullets, each ≤ 25 words. The single most important kinetic event, diplomatic shift, and escalation signal of the window. If no movement on an axis, say so explicitly (`No material movement`) rather than padding.

### Section 2 — Kinetic events

Chronological table. One row per confirmed or credibly-claimed event.

| Time (UTC) | Theatre | Actor → Target | Event | Confirmation | Sources |
|---|---|---|---|---|---|

- **Theatre:** Israel-home / Lebanon / Syria / Iraq-Syria border / Iran-home / Red Sea / Yemen / Gulf / US-regional.
- **Confirmation:** `Confirmed` (primary source from both sides, or OSINT geolocation) / `One-sided` (only one belligerent has acknowledged) / `Claimed` (one side claims, the other denies or is silent) / `Disputed` (active contradiction).
- **Sources:** at least one primary where possible; cite URLs.

### Section 3 — Diplomatic & political

Bullets. Official statements, summit readouts, legislative actions, coalition moves. Include US / Israeli / Iranian / Lebanese / Gulf / European positions where relevant. Cite primary press releases over wire reporting.

### Section 4 — Nuclear file

Even when quiet, report status: IAEA statements, enrichment-level reporting, board resolutions, inspector access, any weaponisation-indicator claim. If the window contains no new nuclear-file signal, write `No new IAEA or enrichment signal in window.` — do not omit the section.

### Section 5 — Economic & sanctions

OFAC designations, Treasury actions, EU / UK sanctions, oil-export disruption signals, shipping/insurance market moves tied to the conflict. Cite the designation page or official gazette, not the news summary.

### Section 6 — Indicators & Warnings (I&W)

Escalation / de-escalation signals that do not yet rise to kinetic events but shift posture. Examples: reserve mobilisations, embassy evacuations, port closures, NOTAMs / airspace restrictions, carrier-group movements, Houthi threat statements, Hezbollah readiness signalling, Iranian drill announcements, US regional force-posture changes.

Emit each as: `<signal> — <source> — <direction: ↑ escalation / ↓ de-escalation / → posture> — <implication, ≤ 20 words>`.

### Section 7 — Narrative divergence

For each kinetic or casualty claim where opposing-framing sources diverge, record the divergence in a small table:

| Claim | Pro-Israel / US framing | Iran / Axis framing | OSINT / neutral framing | Assessment |
|---|---|---|---|---|

The **Assessment** column is the agent's best reading given the evidence — or `Insufficient evidence` if the claims cannot be reconciled from the window's sources.

### Section 8 — Gaps & unknowns

Bullets. Specific questions the SITREP could not answer with current sources, and which source class would be needed (primary government doc / OSINT geolocation / academic reporting / classified — i.e. unreachable). This section is explicit about what the agent does not know.

### Section 9 — Source reliability notes

Only include entries where a source behaved unusually in-window: a normally-reliable feed went stale, a source issued a correction, a feed produced what appears to be a disinfo / narrative-management item. Skip the section if nothing unusual occurred.

### Footer

```
---
Grounding: grounding-set.md (fall-through: sources.md)
Generated by: generate-sitrep skill (Iran-Israel-Grounding-Package)
```

## Style rules

- Dates / times: UTC ISO-8601 with `Z` suffix. Always.
- No hedging-for-hedging's-sake. If confidence is low, say `Low confidence` and name the reason. Do not use vague phrases like "reports suggest" without citation.
- No speculation beyond the I&W section. The rest of the document is event-grounded.
- Do not use emoji. Do not use celebratory, editorial, or advocacy language. This is an intel product, not commentary.
- Do not invent source coverage. If `grounding-set.md` has a gap, name the gap in *Gaps & unknowns*.
- Keep the whole SITREP under ~1200 words. Density over length.

## Cadence guidance

If the user asks for a recurring SITREP:

- **Hourly** during active kinetic windows — lean heavily on IDF Telegram, Al-Masirah, Tasnim, wire services.
- **Every 6 hours** during elevated-posture but non-kinetic periods.
- **Daily (anchored to the ISW Iran Update publication time, ~23:00 UTC)** for background monitoring.

Use the `loop` skill to schedule recurring runs; do not bake a schedule into this skill.
