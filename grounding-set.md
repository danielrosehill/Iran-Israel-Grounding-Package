# Recommended Grounding Set

A curated subset of `sources.md` — broad enough to span the primary / wire / OSINT / analytical / adversarial layers, tight enough that an agent can poll or retrieve it without drowning.

Use this list as the default grounding surface for Iran–Israel–US conflict work. Drop down to individual categories in `sources.md` only when a specific angle (legal, academic, regional niche) needs depth that this set does not carry.

**Design rules**

- Every layer in `sources.md § Recommended grounding stack` is represented by at least one source here.
- Adversarial outlets are paired so the agent always sees both framings (IDF ↔ Tasnim; Al-Manar ↔ Arutz Sheva; Tasnim ↔ FDD).
- Think-tank selection deliberately spans the hawk ↔ restraint spectrum; no single ideological lane is overweight.
- Feeds are preferred over HTML where available — this set is polling-friendly.

## Primary state — Israel / US / allies

- **IDF (English)** — <https://www.idf.il/en/> — canonical IDF communiqués.
- **IDF Spokesperson (Telegram)** — <https://t.me/idfofficial> — real-time operational updates.
- **Israel MFA press room** — `https://mfa.gov.il/MFA/PressRoom/rss/Pages/default.aspx`
- **US Department of State — press releases** — `https://www.state.gov/feed/`
- **US CENTCOM news** — `https://www.centcom.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=808&isdashboardselected=0&max=20`
- **NATO newsroom** — `https://www.nato.int/cps/rss/en/natohq/rssFeed.xsl/rssFeed.xml`

## Primary state — Iran / Axis of Resistance

- **Iran MFA (English)** — <https://en.mfa.gov.ir/>
- **IRNA (state wire)** — `https://en.irna.ir/rss`
- **Tasnim News (IRGC-aligned)** — `https://www.tasnimnews.com/en/rss/feed/0/7/0/`
- **Al-Masirah (Houthi)** — <https://english.almasirah.net.ye/>
- **Al-Manar TV (Hezbollah)** — `https://english.almanar.com.lb/rss`

## Primary state — Lebanon / international bodies

- **Lebanese Armed Forces** — <https://www.lebarmy.gov.lb/en>
- **UNIFIL press** — <https://unifil.unmissions.org/>
- **IAEA — Iran focus** — `https://www.iaea.org/news/feed`
- **UN News — Middle East** — `https://news.un.org/feed/subscribe/en/news/region/middle-east/feed/rss.xml`

## Wire & regional reporting

- **Times of Israel — Israel & the Region** — `https://www.timesofisrael.com/israel-and-the-region/feed/`
- **Haaretz latest headlines** — `https://www.haaretz.com/srv/haaretz-latest-headlines`
- **Al Jazeera English** — `https://www.aljazeera.com/xml/rss/all.xml`
- **Al Arabiya English** — `https://english.alarabiya.net/feed/rss2/en.xml`
- **Arab News — Middle East** — `https://www.arabnews.com/cat/2/rss.xml`
- **Arutz Sheva** — `https://www.israelnationalnews.com/Rss.aspx?act=0.1` — pairs with Al-Manar for framing contrast.

## OSINT synthesis

- **ISW/CTP — Iran Update Special Report** — see `sources.md` for the WP REST query pattern; daily anchor.
- **Bellingcat** — `https://www.bellingcat.com/feed/`
- **ACLED** — `https://acleddata.com/feed/`
- **Long War Journal — Israel tag** — `https://www.longwarjournal.org/tags/israel/feed`
- **TLDR Iran SITREP** — `https://www.iransitrep.com/api/feed` — treat as lead, not citation.

## Analysis — spanning the spectrum

- **The Washington Institute** — `https://www.washingtoninstitute.org/policy-analysis/rss.xml` (hawk / Israel-aligned)
- **INSS (Tel Aviv)** — `https://www.inss.org.il/feed/` (Israeli national-security)
- **FDD** — `https://www.fdd.org/feed/` (hawk on Iran)
- **International Crisis Group** — `https://www.crisisgroup.org/rss?tid=91` (centrist / diplomatic)
- **Quincy Institute / Responsible Statecraft** — `https://responsiblestatecraft.org/feed/` (restraint school)

## Dissident & opposition

- **Iran International** — `https://www.iranintl.com/en/rss.xml`
- **IranWire** — `https://iranwire.com/en/feed/`
- **Syrian Observatory for Human Rights** — `https://www.syriahr.com/en/feed/`

---

## How an agent should use this set

1. **Baseline poll** — the whole set, hourly during non-kinetic periods. During active kinetic windows, shorten to 5–15 minutes for IDF Telegram, Al-Masirah, Tasnim, and ISW.
2. **Triangulate, don't aggregate** — before accepting a claim, check the counterpart source from the opposing framing layer (e.g. IDF claim → Tasnim / Al-Manar; Iranian strike claim → IDF / INSS).
3. **Primary beats wire** — if a wire story cites an IDF statement, IAEA report, or OFAC action, re-fetch the primary document from this list before citing.
4. **Fall through to `sources.md`** — only when this set leaves a gap (legal analysis, academic framing, niche regional angle).
5. **Fall through to search MCPs** — only when `sources.md` also leaves a gap. See `sources.md § Recommended search MCP tools` for usage rules.
