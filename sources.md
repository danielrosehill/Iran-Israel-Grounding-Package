# Whitelisted Sources

Grounding sources for the Iran–Israel–US geopolitical conflict (2026). See `AGENTS.md` for usage rules.

All entries in this file are public, open-web sources. No private feeds, paid API keys, or subscriber-only URLs are listed — agents can fetch everything here without credentials (paywalled article pages may still gate full text, but the feed URL itself is public). If you are contributing, **do not add** private Inoreader share links, personal API tokens, authenticated Telegram join links, or any URL that requires the maintainer's session.

## Recommended grounding stack

For an agent grounding on this topic, combine the following layers rather than relying on any single one:

1. **Primary state sources** — IDF, Gov of Israel, Lebanese Army, Iran MFA, US State, NATO, IAEA, UN Security Council. Use for official positions, casualty figures, and confirmed strikes. Cross-check adversary claims against the other side's primary source.
2. **Wire services** — Reuters / AP proxies (via Times of Israel, Arab News, etc.), IRNA, SANA, Saba (both), NNA Lebanon. Use for fast factual signal.
3. **OSINT synthesis** — ISW/CTP Iran Update (daily anchor), Bellingcat, ACLED, Long War Journal, Aviationist, Naval News, Oryx, Geoconfirmed. Use to corroborate or contradict primary claims with geolocation and munitions evidence.
4. **Think-tank analysis** — Washington Institute, INSS, FDD, Crisis Group, Chatham House, Carnegie MEC, MEI, Quincy Institute. Deliberately span the hawk↔restraint spectrum; do not ground on a single ideological lane.
5. **Regional voices** — Al Jazeera, Al Arabiya, Al-Monitor, Middle East Eye, Al-Manar, Al-Mayadeen, Tasnim, Press TV. Read adversarial outlets **against each other** — Al-Manar vs. Arutz Sheva, Tasnim vs. FDD — to surface framing.
6. **Dissident / opposition** — Iran International, Radio Farda, IranWire, HRANA, CHRI, Syrian Observatory. Use for inside-regime reporting unavailable in state media; note funding/bias.
7. **Search-layer MCPs** (see below) — use when the whitelist does not already contain coverage of a specific incident or when you need cross-source triangulation in real time.

### Polling cadence (suggested)

- **Minutes**: IDF Spokesperson Telegram, Al-Masirah, Tasnim, ISW Iran Update during active kinetic windows.
- **Hourly**: wire services (Reuters proxies, IRNA, SANA, Saba), Al Jazeera, Times of Israel, Haaretz.
- **Daily**: ISW/CTP Iran Update Special Report, think-tank feeds, UN/IAEA announcements.
- **Weekly**: academic commentary (MERIP, POMEPS, LSE MEC), long-form analysis.

## Recommended search MCP tools

When the whitelist lacks coverage, or an agent needs real-time triangulation beyond static RSS, use the following search-layer MCP servers. Install per the user's MCP Jungle conventions.

- **Perplexity API (`perplexity-ask`)** — live web search with LLM-synthesized answers and citations. Best for: "what happened in the last N hours" queries where you need a cited summary rather than raw docs. Install: `claude mcp add perplexity-ask -- npx -y server-perplexity-ask` with `PERPLEXITY_API_KEY` env. Use sparingly — it's a paid API and answers are already synthesized (verify citations against whitelisted sources before grounding on them).
- **Tavily (`tavily-mcp`)** — search + extract optimized for agentic retrieval; returns raw snippets plus full-text extraction. Best for: pulling structured results you can then re-fetch and cite from whitelisted domains. Install: `claude mcp add tavily-mcp -- npx -y tavily-mcp@latest` with `TAVILY_API_KEY`. Supports `tavily_search`, `tavily_extract`, `tavily_crawl`, `tavily_map`.
- **Exa AI (`exa-mcp-server`)** — neural search with strong recall on long-tail and niche sources (think-tank PDFs, primary docs, academic pages). Best for: finding the primary document behind a news claim (e.g. the IAEA board report behind a Reuters headline). Install: `claude mcp add exa -- npx -y exa-mcp-server` with `EXA_API_KEY`. Supports domain filters — scope to `.gov.il`, `.gov.lb`, `nato.int`, `iaea.org`, `un.org`, etc. to stay within the spirit of the whitelist.

### Usage rules for search MCPs

1. Treat search-MCP results as **leads**, not citations. Always re-fetch the underlying URL and cite it directly.
2. Prefer Exa with domain filters scoped to whitelisted domains before issuing an open-web query.
3. Do not ground on Perplexity's synthesized answer text — ground on the URLs it cites, and only after confirming those URLs are on the whitelist or are primary documents.
4. Log which MCP was used for which claim; bias profiles differ (Perplexity over-indexes on recent news, Exa on long-tail primary docs, Tavily on structured web).

## News & Reporting

<!-- - [Name](https://example.com) — one-line justification -->

## Think Tanks & Analysis

- [Institute for the Study of War — Iran Update Special Report series](https://understandingwar.org/research/middle-east/) — daily ISW/CTP analysis of the Iran war; near-primary OSINT synthesis.
  - **Poll method:** ISW runs WordPress and exposes the REST API.
    - Latest series entries: `GET https://understandingwar.org/wp-json/wp/v2/posts?search=iran+update&orderby=date&order=desc&per_page=10`
    - Single post by slug: `GET https://understandingwar.org/wp-json/wp/v2/posts?slug=iran-update-special-report-april-18-2026`
    - RSS fallback: `https://understandingwar.org/feed/` (follow 301 to the canonical feed).
  - **Identification:** series posts have titles beginning `Iran Update Special Report, <date>` and slugs `iran-update-special-report-<month>-<day>-<year>`. Filter on that pattern when ingesting.
  - **Fields to retain:** `title.rendered`, `date_gmt`, `link`, `content.rendered` (strip HTML), `modified_gmt` for staleness checks.

## Primary Documents & Government

### Israel

- [IDF — Official site (English)](https://www.idf.il/en/) — canonical IDF statements, operational announcements, spokesperson releases.
- [IDF Spokesperson (Telegram, English)](https://t.me/idfofficial) — real-time operational updates; same channel already listed under Loose.
- [Israel Ministry of Foreign Affairs](https://www.gov.il/en/departments/ministry_of_foreign_affairs) — official diplomatic statements, treaty positions.
  - RSS: `https://mfa.gov.il/MFA/PressRoom/rss/Pages/default.aspx`
- [Israel Prime Minister's Office](https://www.gov.il/en/departments/prime_ministers_office) — PMO press releases, cabinet decisions.
- [Israel Ministry of Defense](https://www.gov.il/en/departments/ministry_of_defense) — procurement, defense policy, reserve call-ups.
- [Knesset (English)](https://main.knesset.gov.il/EN/) — legislative record, committee transcripts, war-cabinet oversight.
- [Israel National Cyber Directorate](https://www.gov.il/en/departments/israel_national_cyber_directorate) — cyber incident advisories.

### Lebanon

- [Lebanese Armed Forces (official)](https://www.lebarmy.gov.lb/en) — LAF communiqués, deployment announcements along the Blue Line.
- [Lebanese Presidency](https://www.presidency.gov.lb/English/Pages/default.aspx) — presidential statements.
- [Lebanese Council of Ministers / Grand Serail](https://www.pcm.gov.lb/arabic/default.aspx) — PM office, cabinet statements (Arabic primary).
- [Lebanese Ministry of Foreign Affairs](http://www.foreignaffairs.gov.lb/english/Pages/default.aspx) — diplomatic notes, UNIFIL coordination.
- [National News Agency (Lebanon)](http://nna-leb.gov.lb/en) — official state wire service.
- [UNIFIL](https://unifil.unmissions.org/) — peacekeeping mission press releases on Blue Line incidents.

### Iran (state)

- [Iran Ministry of Foreign Affairs (English)](https://en.mfa.gov.ir/) — official diplomatic positions.
- [President of Iran (official)](https://president.ir/en) — presidential statements, speeches.
- [IRNA (Islamic Republic News Agency, English)](https://en.irna.ir/) — state wire service.
  - RSS: `https://en.irna.ir/rss`
- [Tasnim News (English)](https://www.tasnimnews.com/en) — IRGC-aligned outlet, useful for hardline framing.
  - RSS: `https://www.tasnimnews.com/en/rss/feed/0/7/0/`
- [Mehr News (English)](https://en.mehrnews.com/) — state-aligned news agency.
  - RSS: `https://en.mehrnews.com/rss`
- [Fars News (English)](https://www.farsnews.ir/en) — IRGC-linked, hardline reporting.

### Yemen / Houthis

- [Al-Masirah (English)](https://english.almasirah.net.ye/) — Houthi-run broadcaster, primary source for Ansar Allah statements.
- [Saba News Agency (English)](https://www.saba.ye/en) — Houthi-controlled state wire (also listed under MENA).
- [Yemen News Agency — Saba (official gov-IRG)](https://www.sabanew.net/) — recognized-government counterpart wire.

### Lebanon — Hezbollah-aligned

- [Al-Manar TV (English)](https://english.almanar.com.lb/) — Hezbollah-owned broadcaster (also listed under MENA).
- [Al-Ahed News (English)](https://english.alahednews.com.lb/) — Hezbollah-aligned news site.
- [Al-Mayadeen (English)](https://english.almayadeen.net/) — pan-Arab, pro-Axis-of-Resistance line (also listed under MENA).

### United States

- [US Department of State — Press Releases](https://www.state.gov/press-releases/) — official US diplomatic statements.
  - RSS: `https://www.state.gov/feed/`
- [US Department of Defense — News](https://www.defense.gov/News/) — Pentagon readouts, press briefings (also listed under World militaries).
- [White House Briefing Room](https://www.whitehouse.gov/briefing-room/) — presidential statements, NSC readouts.
- [US Treasury — OFAC Recent Actions](https://ofac.treasury.gov/recent-actions) — sanctions designations (Iran, IRGC, Hezbollah, Houthis).
- [US CENTCOM](https://www.centcom.mil/) — operational press releases (also listed under World militaries).

### NATO & allies

- [NATO Newsroom](https://www.nato.int/cps/en/natohq/news.htm) — alliance statements, North Atlantic Council readouts.
  - RSS: `https://www.nato.int/cps/rss/en/natohq/rssFeed.xsl/rssFeed.xml` (already listed under World militaries).
- [SHAPE (NATO Allied Command Operations)](https://shape.nato.int/) — operational-level press releases.
- [UK Ministry of Defence — News](https://www.gov.uk/government/organisations/ministry-of-defence) — RSS: `https://www.gov.uk/government/organisations/ministry-of-defence.atom`.
- [UK Foreign, Commonwealth & Development Office](https://www.gov.uk/government/organisations/foreign-commonwealth-development-office) — RSS: `https://www.gov.uk/government/organisations/foreign-commonwealth-development-office.atom`.
- [French Ministry for Europe and Foreign Affairs](https://www.diplomatie.gouv.fr/en/) — statements on Lebanon, Iran, MEPP.
- [German Federal Foreign Office](https://www.auswaertiges-amt.de/en) — German positions on sanctions, JCPOA, Lebanon.

### International bodies

- [IAEA — Iran (verification and monitoring)](https://www.iaea.org/newscenter/focus/iran) — Board reports, DG statements on Iran nuclear file.
  - RSS: `https://www.iaea.org/news/feed`
- [UN Security Council — Meetings & Press](https://www.un.org/securitycouncil/) — resolutions, presidential statements.
- [UN OCHA — oPt](https://www.ochaopt.org/) — humanitarian situation reports for Gaza/West Bank.
- [ICC — Situations and cases](https://www.icc-cpi.int/situations-under-investigation) — ICC filings relevant to the situation in Palestine.

## Dissident & Opposition Media

### Iran — diaspora / opposition

- [Radio Farda (RFE/RL Persian)](https://www.radiofarda.com/) — US-funded Persian-language outlet covering domestic Iran.
  - RSS: `https://www.radiofarda.com/api/zrqiteuuir`
- [VOA Persian (Farsi)](https://ir.voanews.com/) — US government Persian-language service.
- [Manoto News](https://www.manoto.news/) — London-based Persian-language outlet, monarchist-leaning.
- [Iran International (English)](https://www.iranintl.com/en) — Persian-gulf-funded, opposition-aligned; YouTube/Telegram already listed.
  - RSS: `https://www.iranintl.com/en/rss.xml`
- [IranWire (English)](https://iranwire.com/en/) — founded by Maziar Bahari; citizen-journalism focus.
  - RSS: `https://iranwire.com/en/feed/`
- [National Council of Resistance of Iran (NCRI)](https://www.ncr-iran.org/en/) — MEK-affiliated; flag framing bias but useful for internal reporting.
- [Center for Human Rights in Iran](https://iranhumanrights.org/) — NY-based, documentation-focused.
  - RSS: `https://iranhumanrights.org/feed/`
- [HRANA — Human Rights Activists News Agency](https://www.en-hrana.org/) — inside-Iran stringer network, protest and detention tracking.

### Syria — post-Assad / opposition legacy

- [Syrian Observatory for Human Rights](https://www.syriahr.com/en/) — UK-based monitoring group, casualty and incident tracking.
  - RSS: `https://www.syriahr.com/en/feed/`
- [Syria Direct](https://syriadirect.org/) — independent outlet with inside-Syria reporters.

## OSINT

- [Bellingcat](https://www.bellingcat.com/) — open-source investigations, geolocation, munitions ID.
  - RSS: `https://www.bellingcat.com/feed/`
- [ACLED — Armed Conflict Location & Event Data](https://acleddata.com/) — event-level conflict data, regional briefs.
  - RSS: `https://acleddata.com/feed/`
- [Conflict Armament Research](https://www.conflictarm.com/) — field-level weapons tracing, Iran-linked arms flows.
- [Janes](https://www.janes.com/) — open-source defence intelligence (mostly paywalled; use for abstracts).
  - RSS: `https://www.janes.com/feeds/defence-news`
- [The Aviationist](https://theaviationist.com/) — airframe and strike-package analysis.
  - RSS: `https://theaviationist.com/feed/`
- [Naval News](https://www.navalnews.com/) — naval movements, Red Sea / Eastern Med.
  - RSS: `https://www.navalnews.com/feed/`
- [Critical Threats Project (AEI)](https://www.criticalthreats.org/) — ISW's co-publisher on Iran Update series.
  - RSS: `https://www.criticalthreats.org/feed`
- [Silah Report](https://silahreport.com/) — small-arms and munitions OSINT.
- [Oryx (blog)](https://www.oryxspioenkop.com/) — visually-confirmed equipment losses.
- [Geoconfirmed](https://geoconfirmed.org/) — geolocation aggregator for verified conflict footage.
- [TLDR Iran — Iran SITREP](https://www.iransitrep.com/) — automated daily intelligence briefing on the 2026 US–Israel–Iran conflict; numbered-day SITREPs.
  - RSS: `https://www.iransitrep.com/api/feed`
  - **Caveat:** automated/aggregated summarisation — treat as a lead surface, not a primary citation.

## Think Tanks & Analysis (additional)

- [The Washington Institute for Near East Policy](https://www.washingtoninstitute.org/) — policy analysis on Iran, Hezbollah, Gulf.
  - RSS: `https://www.washingtoninstitute.org/policy-analysis/rss.xml`
- [Institute for National Security Studies (INSS, Tel Aviv)](https://www.inss.org.il/) — IDF-adjacent Israeli think tank.
  - RSS: `https://www.inss.org.il/feed/`
- [Jerusalem Center for Public Affairs (JCPA)](https://jcpa.org/) — Israeli policy analysis.
  - RSS: `https://jcpa.org/feed/`
- [BESA Center (Bar-Ilan)](https://besacenter.org/) — Israeli security studies.
  - RSS: `https://besacenter.org/feed/`
- [Middle East Institute (MEI)](https://www.mei.edu/) — DC-based, broad regional coverage.
  - RSS: `https://www.mei.edu/rss.xml`
- [Carnegie Middle East Center](https://carnegie-mec.org/) — Beirut-based Carnegie branch.
  - RSS: `https://carnegie-mec.org/rss/publications.xml`
- [Chatham House — Middle East and North Africa](https://www.chathamhouse.org/about-us/our-departments/middle-east-and-north-africa-programme) — UK-based.
- [CSIS — Middle East Program](https://www.csis.org/programs/middle-east-program) — DC-based.
  - RSS: `https://www.csis.org/analysis/rss.xml`
- [IISS — Middle East](https://www.iiss.org/research/middle-east/) — London-based, Military Balance publisher.
- [Hudson Institute](https://www.hudson.org/) — DC, hawkish on Iran.
  - RSS: `https://www.hudson.org/rss`
- [Brookings — Middle East](https://www.brookings.edu/topic/middle-east/) — DC, centrist.
- [RUSI](https://rusi.org/) — UK defence and security.
  - RSS: `https://rusi.org/rss.xml`
- [Quincy Institute](https://quincyinst.org/) — restraint-school US foreign policy.
  - RSS: `https://quincyinst.org/feed/`

## Academic

- [MERIP — Middle East Report](https://merip.org/) — critical academic coverage.
  - RSS: `https://merip.org/feed/`
- [LSE Middle East Centre Blog](https://blogs.lse.ac.uk/mec/) — UK academic commentary.
  - RSS: `https://blogs.lse.ac.uk/mec/feed/`
- [POMEPS — Project on Middle East Political Science](https://pomeps.org/) — academic working papers.
  - RSS: `https://pomeps.org/feed`
- [War on the Rocks](https://warontherocks.com/) — practitioner-academic hybrid.
  - RSS: `https://warontherocks.com/feed/`
- [Lawfare](https://www.lawfaremedia.org/) — legal/national-security analysis.
  - RSS: `https://www.lawfaremedia.org/feed`

---

## Inoreader feed set

The following RSS feeds are the maintainer's curated Inoreader subscriptions, grouped by the folder they live in. Agents may poll these as live grounding signal. Format: `[Display name](site) — \`feed URL\``. Feeds with `@ino.to` addresses are Inoreader email-newsletter bridges — poll via the Inoreader API, not directly.

### Loose (unfoldered)

- ["Iran ballistic" - Google News](https://news.google.com/search?q=Iran+ballistic&&hl=en-IL&gl=IL&ceid=IL:en) — `https://news.google.com/news/rss/search?q=Iran%20ballistic&&hl=en-IL&gl=IL&ceid=IL:en`
- ["IRGC" - Google News](https://news.google.com/search?q=IRGC&&hl=en-IL&gl=IL&ceid=IL:en) — `https://news.google.com/news/rss/search?q=IRGC&&hl=en-IL&gl=IL&ceid=IL:en`
- [Alma Research and Education Center](https://israel-alma.org/) — `https://israel-alma.org/feed/`
- [Arutz Sheva News](https://www.israelnationalnews.com/) — `https://www.israelnationalnews.com/Rss.aspx?act=0.1`
- [idfnadesk](https://www.youtube.com/channel/UCawNWlihdgaycQpO3zi-jYg/videos) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCawNWlihdgaycQpO3zi-jYg`
- [Iran International ايران اينترنشنال](https://www.youtube.com/channel/UCat6bC0Wrqq9Bcq7EkH_yQw) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCat6bC0Wrqq9Bcq7EkH_yQw`
- [Iran International ایران اینترنشنال](https://t.me/IranintlTV) — `https://t.me/IranintlTV`
- [Iran | The Guardian](http://www.theguardian.com/world/iran) — `http://www.guardian.co.uk/world/iran/rss`
- [Iranwire](https://t.me/Farsi_Iranwire) — `https://t.me/Farsi_Iranwire`
- [Israel Defense Forces](https://t.me/idfofficial) — `https://t.me/idfofficial`
- [jerusalem (Bluesky search)](https://bsky.app/search?q=jerusalem) — `https://bsky.app/search?q=jerusalem`
- [JPost.com - Iran](https://www.jpost.com) — `https://www.jpost.com/Rss/RssFeedsIran`
- [OSINT mindset](https://t.me/osint_mindset) — `https://t.me/osint_mindset`
- [Responsible Statecraft](https://responsiblestatecraft.org/) — `https://responsiblestatecraft.org/feed/`
- [The RAND Blog](https://www.rand.org/blog.html) — `https://www.rand.org/blog.xml`
- [The Times of Israel](https://t.me/TheTimesOfIsrael2022) — `https://t.me/TheTimesOfIsrael2022`
- [The Times of Israel » Israel & the Region](https://www.timesofisrael.com/) — `https://www.timesofisrael.com/israel-and-the-region/feed/`
- [ישראל היום](https://t.me/israelhayomofficial) — `https://t.me/israelhayomofficial`

### Newsletters

- [Daily Alert](https://www.inoreader.com) — `dailyalert1@ino.to`
- [Iran Update](https://www.inoreader.com) — `iranupdate@ino.to`
- [Meir Amit Center](https://www.inoreader.com) — `meiramitcenterr@ino.to`

### Israeli - English

- [Arutz Sheva News](https://www.israelnationalnews.com/) — `https://www.israelnationalnews.com/Rss.aspx?act=.1`
- [Breaking Israel News](https://www.breakingisraelnews.com/) — `https://www.breakingisraelnews.com/feed/`
- [Haaretz latest headlines](https://www.haaretz.com/srv/all-headlines-rss) — `https://www.haaretz.com/srv/haaretz-latest-headlines`
- [Israellycool](https://www.israellycool.com/) — `https://www.israellycool.com/feed/`
- [JPost.com - Breaking News](https://www.jpost.com/) — `https://rss.jpost.com/rss/rssfeedsheadlines.aspx`
- [The Times of Israel](https://www.timesofisrael.com/) — `https://www.timesofisrael.com/feed/`
- [ynet - News](https://www.ynetnews.com/) — `https://www.ynet.co.il/Integration/StoryRss3082.xml`

### Israeli - Hebrew

- [Haarets](https://www.haaretz.co.il/cmlink/%D7%94%D7%90%D7%A8%D7%A5-%D7%97%D7%93%D7%A9%D7%95%D7%AA-1.1410478) — `https://www.haaretz.co.il/cmlink/1.1410478`
- [INTELLI TIMES](https://intellitimes.co.il/) — `https://intellitimes.co.il/feed/`
- [Israel Today](https://www.israelhayom.co.il/rss.xml) — `https://www.israelhayom.co.il/rss.xml`
- [Maariv](https://www.maariv.co.il) — `https://www.maariv.co.il/Rss/RssChadashot`
- [Mako](https://www.mako.co.il/news) — `https://rcs.mako.co.il/rss/31750a2610f26110VgnVCM1000005201000aRCRD.xml`
- [The Marker](https://www.themarker.com/cmlink/themarker-%D7%9B%D7%9C-%D7%97%D7%93%D7%A9%D7%95%D7%AA-%D7%94%D7%99%D7%95%D7%9D-1.144) — `https://www.themarker.com/cmlink/1.144`
- [Ynet](https://www.ynet.co.il/) — `https://www.ynet.co.il/Integration/StoryRss2.xml`

### MENA

- [Al Jazeera English](https://www.aljazeera.com/default.html) — `https://www.aljazeera.com/xml/rss/all.xml`
- [Al-Manar TV Lebanon](https://english.almanar.com.lb) — `https://english.almanar.com.lb/rss`
- [Home Page](https://english.alarabiya.net/en) — `https://english.alarabiya.net/feed/rss2/en.xml`
- [Khaleej Times](https://www.youtube.com/channel/UCaeG9NIqdx-xcZGt7ETfkpA) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCaeG9NIqdx-xcZGt7ETfkpA`
- [Middle-East](https://www.arabnews.com/) — `https://www.arabnews.com/cat/2/rss.xml`
- [Presstv](https://www.presstv.ir/) — `https://www.presstv.ir/rss/rss-102.xml`
- [rssfeed](https://english.almayadeen.net/feed.rss) — `https://english.almayadeen.net/feed.rss`
- [Syrian Arab News Agency](https://sana.sy/en) — `https://sana.sy/en/?feed=rss2`
- [Yemen News Agency - Saba](https://www.saba.ye/en) — `https://www.saba.ye/en/rsscatfeed14.htm`

### Analysis

- [Al-Monitor: The Pulse of The Middle East](https://www.al-monitor.com/) — `https://www.al-monitor.com/rss.xml`
- [Analysis MEED](https://www.meed.com/rss-feeds/) — `https://www.meed.com/classifications/analysis/feed`
- [European Council on Foreign Relations](https://ecfr.eu/) — `https://ecfr.eu/feed/`
- [Israel Archives - Just Security](https://www.justsecurity.org/tag/israel/) — `https://www.justsecurity.org/tag/israel/feed/`
- [Israel Behind the News](https://israelbehindthenews.com) — `https://israelbehindthenews.com/feed/`
- [Middle East Eye - RSS Feed](https://www.middleeasteye.net/rss) — `https://www.middleeasteye.net/rss`
- [openDemocracy](https://www.opendemocracy.net/) — `https://www.opendemocracy.net/xml/rss/home/index.xml`
- [RSS](https://www.crisisgroup.org/) — `https://www.crisisgroup.org/rss?tid=91`

### Think Tanks & Policy

- [Atlantic Council](https://www.atlanticcouncil.org/region/israel/) — `https://www.atlanticcouncil.org/region/israel/feed/`
- [FDD](https://www.fdd.org) — `https://www.fdd.org/feed/`

### OSINT

- [Breaking Defence - Israel](https://breakingdefense.com/tag/israel/) — `https://breakingdefense.com/tag/israel/feed/`
- [FDD](https://www.longwarjournal.org/tags/israel) — `https://www.longwarjournal.org/tags/israel/feed`
- [IntelNews.org - Israel](https://intelnews.org/) — `https://intelnews.org/tag/israel/feed/`
- [The Soufan Center](https://thesoufancenter.org/) — `https://thesoufancenter.org/feed/`
- [The War Zone](https://www.twz.com/) — `https://www.twz.com/feed`

### Defence

- [C4ISRNet](https://www.c4isrnet.com/) — `https://www.c4isrnet.com/arc/outboundfeeds/rss/?outputType=xml`
- [Israel](https://thedefensepost.com/tag/israel/) — `https://thedefensepost.com/tag/israel/feed/`

### World militaries

- [Air Force Link News](https://www.af.mil/) — `https://www.af.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=1&isdashboardselected=0&max=20`
- [Defense.gov Explore Feed](https://www.defense.gov/explore) — `https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=9&Site=945&max=10`
- [NATO Latest News](https://www.nato.int/) — `https://www.nato.int/cps/rss/en/natohq/rssFeed.xsl/rssFeed.xml`
- [RAF News](https://www.raf.mod.uk/) — `https://www.raf.mod.uk/news/articles/?rss=true`
- [U.S. Central Command News](https://www.centcom.mil/) — `https://www.centcom.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=808&isdashboardselected=0&max=20`
- [U.S. Cyber Command News](https://www.cybercom.mil/) — `https://www.cybercom.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=848&isdashboardselected=0&max=20`

### Orgs & UN

- [UN News](https://news.un.org/en/) — `https://news.un.org/feed/subscribe/en/news/region/middle-east/feed/rss.xml`
- [UN Press - Welcome to the United Nations](https://press.un.org/en) — `https://press.un.org/en/rss.xml`
- [UNSCO - The office of the United Nations Special Coordinator for the Middle East Peace Process](https://unsco.unmissions.org/news) — `https://unsco.unmissions.org/rss.xml`

### Jewish World

- [Daily News Alert from Israel - COP/JCPA](https://www.dailyalert.org/) — `https://www.dailyalert.org/rss/index.xml`
- [Jewish News » Jewish News](https://www.jewishnews.co.uk/) — `https://www.jewishnews.co.uk/feed/`
- [Jewish Telegraphic Agency](https://www.jta.org/) — `https://www.jta.org/feed`
- [JNS.org](https://www.jns.org/) — `https://www.jns.org/feed`
- [The Canadian Jewish News](https://thecjn.ca/) — `https://thecjn.ca/feed/`
- [The Jewish Chronicles - News](https://www.thejc.com/rss/news) — `https://www.thejc.com/rss/news`
- [The Media Line](https://themedialine.org/) — `https://themedialine.org/feed/`

### North America

- [ABC News: International](https://abcnews.go.com/International/) — `https://feeds.abcnews.com/abcnews/internationalheadlines`
- [CBC | Canada News](https://www.cbc.ca/canada/?cmp=rss) — `https://rss.cbc.ca/lineup/canada.xml`
- [CNN](https://www.youtube.com/channel/UCupvZG-5ko_eiXAupbDfxWw/videos) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCupvZG-5ko_eiXAupbDfxWw`
- [CTV News](https://www.youtube.com/channel/UCi7Zk9baY1tvdlgxIML8MXg) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCi7Zk9baY1tvdlgxIML8MXg`
- [Fox News](https://www.youtube.com/channel/UCXIJgqnII2ZOINSWNOGFThA/videos) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCXIJgqnII2ZOINSWNOGFThA`
- [FOXNews.com](https://www.foxnews.com/) — `https://feeds.feedburner.com/foxnews/latest`
- [Middle East News: News and Headlines from Iraq, Iran, Israel, Lebanon & More - The Washington Post](https://www.washingtonpost.com/world/middle-east?wprss=rss_middle-east) — `https://feeds.washingtonpost.com/rss/world/middle-east`
- [National Post - Canada](http://news.nationalpost.com/) — `https://nationalpost.com/category/news/feed.xml`
- [NBC News World News](https://feeds.nbcnews.com/feeds/worldnews) — `https://feeds.nbcnews.com/feeds/worldnews`
- [The Globe and Mail](https://www.theglobeandmail.com/) — `https://www.theglobeandmail.com/arc/outboundfeeds/rss/category/business/`
- [The New York Times](https://www.nytimes.com/pages/index.html?partner=rss&emc=rss) — `https://www.nytimes.com/services/xml/rss/nyt/HomePage.xml`
- [The New York Times](https://www.youtube.com/channel/UCqnbDFdCpuN8CMEg0VuEBqA/videos) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCqnbDFdCpuN8CMEg0VuEBqA`
- [USA TODAY](https://www.youtube.com/channel/UCP6HGa63sBC7-KHtkme-p-g/videos) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCP6HGa63sBC7-KHtkme-p-g`
- [Washington Post: Breaking News, World, US, DC News & Analysis](https://www.washingtonpost.com/?wprss=rss_homepage) — `https://feeds.washingtonpost.com/rss/world`

### Europe - English

- [Channel 4 News](https://www.channel4.com/news) — `https://www.channel4.com/news/feed`
- [Evening Standard - Home](https://www.standard.co.uk/rss/) — `https://www.standard.co.uk/rss`
- [Financial Times](http://www.ft.com/markets/emergingmarkets) — `https://www.ft.com/rss/markets/emerging`
- [Independent.ie - Irish News RSS Feed](http://www.independent.ie/irish-news/) — `http://www.independent.ie/national-news/rss`
- [Ireland: BreakingNews.ie](http://www.breakingnews.ie/ireland/) — `http://www.breakingnews.ie/free/rss/tcm_breaking_ireland_rss.asp`
- [Newstalk - Ireland's National Independent Talk Radio Broadcaster » News](http://www.newstalk.ie) — `http://www.newstalk.ie/feed/?cat=8`
- [The Independent - World](https://www.independent.co.uk/news/world/rss) — `https://independent.co.uk/news/world/rss`
- [The Irish Times - News](http://www.irishtimes.com/cmlink/the-irish-times-news-1.1319192) — `http://www.irishtimes.com/feeds/rss/breaking/index.rss`
- [The Telegraph - Telegraph online, Daily Telegraph, Sunday Telegraph](https://www.telegraph.co.uk/) — `https://www.telegraph.co.uk/rss`
- [World News - Breaking international news and headlines | Sky News](https://news.sky.com/world) — `https://feeds.skynews.com/feeds/rss/world.xml`
- [World news | The Guardian](https://www.theguardian.com/world) — `https://feeds.guardian.co.uk/theguardian/world/rss`

### Europe - non-English

- [La Repubblica](https://www.youtube.com/channel/UC9ePmjVRHLL8x8vq5fOKflg) — `https://www.youtube.com/feeds/videos.xml?channel_id=UC9ePmjVRHLL8x8vq5fOKflg`

### Russia & Post-Soviet

- [RT - Daily news](http://rt.com/) — `https://rt.com/rss/`
- [TASS](https://tass.com/) — `https://tass.com/rss/v2.xml`
- [The Moscow Times - News, Business, Culture & Multimedia from Russia](https://themoscowtimes.com/russia) — `https://themoscowtimes.com/feeds/main.xml`

### Turkiye

- [Anadolu Ajansı Güncel Haberler](https://www.aa.com.tr/en/live/) — `https://www.aa.com.tr/en/rss/default?cat=live`
- [DAILYSABAH](https://www.dailysabah.com/) — `https://www.dailysabah.com/rssFeed/11`

### Caucasus

- [AzerNews - All news](https://www.azernews.az/) — `https://www.azernews.az/feeds/index.rss`
- [AzerNews - News from Azerbaijan, Business, Energy, Analysis](https://www.azernews.az/) — `https://www.azernews.az/feed.php`
- [Trend News Agency](http://www.trend.az/) — `http://en.trend.az/rss/trend_all_en.rss`

### South Asia

- [Hindustan Times - india-news](https://www.hindustantimes.com/) — `https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml`
- [NDTV News - Recent](https://www.ndtv.com/) — `https://feeds.feedburner.com/NDTV-LatestNews`
- [The Hindu - International](https://www.thehindu.com/) — `https://www.thehindu.com/news/international/?service=rss`
- [The Indian Express](http://indianexpress.com/) — `http://www.indianexpress.com/rss/`
- [World News, News of World, Top World News, World Breaking Headlines - Times of India](https://timesofindia.indiatimes.com/articlelist/296589292.cms) — `https://timesofindia.indiatimes.com/rssfeeds/296589292.cms`

### Asia

- [China Daily](http://www.chinadaily.com.cn/) — `https://feedx.top/rss/chinadaily.xml`
- [Japan Today: Japan News and Discussion](https://www.japantoday.com/) — `https://www.japantoday.com/feed`
- [Japan Today: Japan News and Discussion - World](https://www.japantoday.com/) — `https://www.japantoday.com/feed/category/world`
- [Nippon TV News 24 Japan](https://www.youtube.com/channel/UCJD2Br_xC-3vY4nkJ9YPYDA) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCJD2Br_xC-3vY4nkJ9YPYDA`
- [NK News - North Korea News](https://www.nknews.org/) — `https://feeds.feedburner.com/Nknewsorg`
- [South China Morning Post - News feed](https://www.scmp.com/rss/91/feed) — `https://www.scmp.com/rss/91/feed`
- [The Japan Times » News](https://www.japantimes.co.jp/) — `https://www.japantimes.co.jp/news/feed/`
- [The Korea Herald](https://www.koreaherald.com/) — `https://www.koreaherald.com/common/rss_xml.php?ct=102`
- [YonhapNews](https://www.yna.co.kr/) — `https://en.yna.co.kr/RSS/news.xml`

### Sub-Saharan Africa

- [eNCA - eNews Channel Africa](https://www.enca.com/rss.xml) — `https://www.enca.com/rss.xml`
- [Mail & Guardian RSS Feed](http://mg.co.za/feeds/rss.aspx) — `http://www.mg.co.za/feeds/rss.aspx`
- [News South Africa Extended](http://www.iol.co.za/news-south-africa-extended-1.679178) — `http://www.iol.co.za/cmlink/news-south-africa-extended-1.679178`
- [News24 South Africa](http://www.news24.com/) — `http://feeds.news24.com/articles/news24/SouthAfrica/rss`

### Oceania

- [ABC News (Australia)](https://www.youtube.com/channel/UCVgO39Bk5sMo66-6o6Spn6Q/videos) — `https://www.youtube.com/feeds/videos.xml?channel_id=UCVgO39Bk5sMo66-6o6Spn6Q`
- [The Sydney Morning Herald News Headlines](http://www.smh.com.au/) — `https://www.smh.com.au/rss/feed.xml`

### Telegram

- [South First Responders](https://t.me/southfirstresponders) — `https://t.me/southfirstresponders`
