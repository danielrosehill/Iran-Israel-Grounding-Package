---
name: url-to-markdown
description: Convert an article URL into clean markdown for ingestion into this grounding package. Use when the user wants to quote, archive, or analyse the body text of a whitelisted source without the surrounding HTML cruft. Picks the right tool from a curated toolkit based on whether offline/hosted is required and what the source type is (news article, government PDF, JS-heavy page).
---

# url-to-markdown

Curated toolkit for turning a URL into clean markdown. None of the tools ship with this repo — install on demand.

## Decision tree

| Situation | Tool | Why |
| --- | --- | --- |
| Default — any news article | **Jina Reader** (hosted) | Best markdown output, handles metadata (title, author, date), zero install. |
| Offline / self-hosted / no third-party calls | **Mozilla Readability** (via `go-readability` single binary, or `readability-lxml` Python CLI) | Battle-tested Firefox Reader View algorithm; single dependency; no network beyond fetching the URL itself. |
| Readability mis-extracts (list pages, unusual layouts, non-English) | **trafilatura** (Python) | Different algorithm, often wins where Readability loses. Markdown output built in. |
| Source is a PDF / .docx / .pptx (government report, ISW white paper) | **markitdown** (Microsoft, Python) | Handles non-HTML primary documents the other tools can't. |
| Page is JS-rendered and Readability returns empty | **imperium-crawl** (from the `rss-discover` toolkit) to fetch rendered HTML, then pipe into Readability or trafilatura | Two-step: render, then extract. |

## The tools

### Jina Reader (default)

- Hosted, free tier (higher limits with API key).
- Usage: prepend `https://r.jina.ai/` to the target URL.
  ```bash
  curl -H "Authorization: Bearer $JINA_API_KEY" \
       https://r.jina.ai/https://understandingwar.org/research/middle-east/iran-update-special-report-april-18-2026/
  ```
- Unauthenticated works too; API key just raises rate limits.

### Mozilla Readability

Three viable ports:

1. **go-readability** (single binary, fastest install):
   ```bash
   go install github.com/go-shiori/go-readability/cmd/go-readability@latest
   go-readability <url>   # HTML; add tooling to convert to markdown (pandoc)
   ```
2. **readability-lxml** (Python, ships with a CLI):
   ```bash
   pip install readability-lxml
   python -m readability.readability -u <url>
   ```
3. **@mozilla/readability** (canonical JS library) — library only, needs jsdom wrapper. Skip unless you're already in Node.

### trafilatura

```bash
pip install trafilatura
trafilatura -u <url> --output-format markdown
```

### markitdown

```bash
pip install 'markitdown[all]'
markitdown path/or/url --output out.md
```

### Rendered-page fallback

If a URL returns near-empty markdown from the above tools, the page is JS-rendered. Fetch rendered HTML with `imperium-crawl` (see the `rss-discover` skill), then pipe to Readability or trafilatura.

## Secrets handling

Keys live in `.env` at the repo root. `.env` is gitignored; `.env.example` documents the shape.

### Setup

```bash
cp .env.example .env
$EDITOR .env   # fill in JINA_API_KEY and any others
```

Load into the current shell before running a tool:

```bash
set -a; source .env; set +a
```

### Upgrade path: KDE keyring (libsecret)

On this workstation (KDE/Plasma), the secure alternative is `secret-tool`:

```bash
# Store once
secret-tool store --label='Jina Reader API key' service jina key api

# Retrieve at runtime
export JINA_API_KEY=$(secret-tool lookup service jina key api)
```

Wrap the export in a small loader (e.g. `scripts/load-secrets.sh`) if multiple tools need it. Do **not** commit anything that calls `secret-tool store` with a literal secret on the command line — that leaks into shell history.

### What not to do

- No hard-coded keys in skill files, scripts, or `sources.md`.
- No keys in git history (if one leaks, rotate it upstream; don't bother scrubbing history).
- No `.env` checked in — the `.gitignore` already blocks it.
