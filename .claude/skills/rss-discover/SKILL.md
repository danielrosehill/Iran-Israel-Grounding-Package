---
name: rss-discover
description: Toolkit for discovering, validating, and synthesising RSS/Atom feeds for sources considered for this grounding package. Use when the user wants to find the feed URL for a site, check whether a candidate source publishes a feed at all, synthesise a feed for sites that don't, or bulk-scan for topic-level news. Picks the appropriate tool from a curated toolkit based on the task.
---

# rss-discover

Curated toolkit of feed-discovery and news-extraction tools for vetting candidate sources before they enter `sources.md`.

None of the tools listed here ship with this repo. The skill is a **decision tree + usage reference** — install on demand.

## Decision tree

| Task | Tool | Why |
| --- | --- | --- |
| "Does site X have an RSS feed?" — one-off lookup | **rsslookup** (hosted) or **feedscout** (library) | Fastest path. rsslookup.com is a free hosted tool; for scripted use, feedscout's platform rules handle YouTube/GitHub/WordPress natively. |
| Bulk-verify a list of candidate URLs, get feed metadata + item counts | **feedscout** via a small Node wrapper | Library, validates feeds and returns format + title + siteUrl. |
| Site blocks bots / is behind Cloudflare / needs stealth | **imperium-crawl** | 29-tool CLI with stealth engine, Cloudflare bypass, ARIA-snapshot scraping. Overkill for normal sites but the right tool for hardened Iranian/regime-aligned targets. |
| Site has **no** feed at all (common for .gov.ir, military, Farsi regime sites) | **newsworker** (Python) | Synthesises a feed from HTML by detecting date patterns in news blocks. Use when RSS simply doesn't exist. |
| Want topic-level aggregation across unknown sources ("Iran missile strikes last 24h") | **Universal-News-Scraper** | Topic auto-discovery via Bing RSS, keyword + date filters, JSON/CSV export. |

Skip `hera-rss-crawler` (PHP, tiny) unless a PHP env is already available.

## The tools

### rsslookup — mratmeyer/rsslookup

- Stack: TypeScript, SaaS + OSS
- Hosted: <https://www.rsslookup.com/>
- Repo: <https://github.com/mratmeyer/rsslookup>
- Use: paste a URL in the browser, get feed. For scripting, hit the hosted form or self-host (TanStack Start + Cloudflare Workers).
- Strengths: popular-site rules (YouTube, Reddit, StackExchange), clean UX.
- Weakness: no CLI binary; self-hosting requires Upstash Redis.

### feedscout — macieklamberski/feedscout

- Stack: TypeScript library (npm `feedscout`)
- Repo: <https://github.com/macieklamberski/feedscout>
- Install: `npm install feedscout`
- Minimal wrapper:
  ```js
  import { discoverFeeds } from 'feedscout'
  const feeds = await discoverFeeds(process.argv[2])
  console.log(JSON.stringify(feeds, null, 2))
  ```
- Methods: `platform` (YouTube/GitHub/WP patterns), `html` (`<link rel=alternate>`), `headers` (HTTP Link), `guess` (common paths). Each can be toggled.
- Strengths: platform-aware — resolves channel URLs to their YouTube/WP feed forms without fetching the page. Highest-quality discovery in this set.

### imperium-crawl — ceoimperiumprojects/imperium-crawl

- Stack: TypeScript CLI, npm `imperium-crawl`
- Repo: <https://github.com/ceoimperiumprojects/imperium-crawl>
- Install: `npm install -g imperium-crawl`
- Use when: target site has anti-bot defences, Cloudflare challenge pages, or requires JS rendering. Includes stealth levels, session encryption, Playwright-backed interaction.
- Caution: heavy dependency tree; only reach for this when lighter tools fail.

### newsworker — ivbeg/newsworker

- Stack: Python library (pypi `newsworker`)
- Repo: <https://github.com/ivbeg/newsworker>
- Install: `pip install newsworker`
- Use:
  ```python
  from newsworker.finder import FeedsFinder
  f = FeedsFinder()
  print(f.find_feeds(url, extractrss=True, noverify=False))
  ```
- Strength: **synthesises a feed from pages that don't publish one** by finding dated news blocks. Essential for Iranian/regime sites that expose news but no RSS.
- Caveat: quality depends on the site's HTML having recognisable dates. Treat output as a heuristic, not a canonical feed.

### Universal-News-Scraper — Ilias1988/Universal-News-Scraper

- Stack: Python CLI
- Repo: <https://github.com/Ilias1988/Universal-News-Scraper>
- Use: topic-level aggregation across many sources. Uses Bing RSS for auto-discovery; filters by keyword + date; exports JSON/CSV.
- Fit for this repo: ad-hoc sweeps like "what outlets are covering IRGC negotiations today" when the whitelist is too narrow.

## Workflow for adding a new source to `sources.md`

1. User proposes a site or feed URL.
2. Run discovery:
   - Normal site → **feedscout** (or rsslookup hosted for a quick check).
   - Hardened site → **imperium-crawl**.
   - No feed exists → **newsworker** to synthesise one; document as `type: synthesised-html` in the sources entry.
3. Validate: fetch the feed, confirm ≥1 recent item, note last pub date.
4. Classify viewpoint (neutral / Israeli / Iran-axis state / diaspora-opposition) — important for this repo.
5. Append under the right section of `sources.md`:
   `- [Name](site-url) — \`feed-url\` — viewpoint: <tag>`
6. Never auto-append. This package's value is its curated whitelist — confirm with the user.
