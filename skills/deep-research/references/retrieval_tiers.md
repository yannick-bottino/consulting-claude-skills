# Retrieval Tiers

The skill adapts to its environment by probing capabilities at P0 (no hooks required — works in Cowork and Claude Code alike). It picks the best retrieval tier available and degrades gracefully. It NEVER fails for lack of a scraper; it falls back.

SEARCH and SCRAPE are two different problems. SEARCH = discover URLs. SCRAPE = turn a URL into clean full-page markdown. You need both. Snippet-only research (skipping the scrape) is the main quality leak in a weak harness.

## Tier selection (decided by `scripts/probe_env.py`)

| Tier | Detected condition | SEARCH layer | SCRAPE layer | Typical env |
|------|-------------------|--------------|--------------|-------------|
| **T1 Full** | bash + open network + pip works | SearXNG / Brave / Tavily API | Crawl4AI (default) → Scrapling StealthyFetcher (anti-bot fallback) | Claude Code on your machine |
| **T2 Bridge** | bash + restricted/whitelisted network | native `web_search` | `web_fetch` + trafilatura/markdownify cleanup in `retrieve.py` | Cowork with Python but bridled egress |
| **T3 Native** | no reliable bash | native `web_search` | native `web_fetch` (full-page, never snippet-only) | Sandboxed app, universal fallback |

The probe writes the chosen tier to `research-notes/_env.md`. Subagents read it to know which retrieval calls are legal.

## What changes by tier — and what does NOT

Constant across all tiers (this is where quality actually comes from):
- The replanning loop (`replanning_loop.md`) runs identically.
- Full-page reads are mandatory in every tier. T3 uses native `web_fetch` on full pages; it is NOT snippet-only.
- The verification/counter-review passes (P6/P7) run identically.

Differs by tier:
- Throughput and anti-bot reach. T1 can scrape protected sites and parallelize hard; T3 is rate-limited by native tools.
- Query ceilings scale down on T3 (native tools are slower) — but the loop logic is the same.

## T1 setup (run on your own machine — will NOT run in the sandbox)

```bash
pip install crawl4ai scrapling trafilatura markdownify
crawl4ai-setup        # installs Playwright browsers for Crawl4AI
scrapling install     # fetches Scrapling's stealth browser deps

# SEARCH: pick ONE
#  - self-hosted SearXNG (zero per-query cost): set SEARXNG_URL
#  - Brave Search API:  set BRAVE_API_KEY
#  - Tavily:            set TAVILY_API_KEY
export SEARXNG_URL="http://localhost:8080"   # example
```

`retrieve.py` auto-detects which of these is configured and routes accordingly. If none of the T1 search backends is configured, the script degrades to T2 even on a capable machine.

## Why not semantic search / reranking on discovery

A web search engine is already a massive first-stage ranker over the open web. Bolting embeddings onto a handful of results adds little. Reranking earns its keep only on a CLOSED corpus (your own docs), where there is no upstream ranker. The one place it can help open-web research: reranking the chunks of pages you have ALREADY scraped, before they enter the synthesis context, purely to fit the token budget. That is a last-mile optimization (available as an optional step in T1), not the source of the quality gap. Do not invest here before the loop, the budget, and the scrape layer are solid.

## Scraper roles (T1)

- **Crawl4AI** — default engine. Async, Playwright-based, purpose-built for LLM-ready markdown with content filtering. Use for bulk full-page extraction.
- **Scrapling StealthyFetcher** — fallback when Crawl4AI is blocked (Cloudflare Turnstile etc.). Slower, heavier; use only on pages that refuse the default engine.

The skill shells out to `retrieve.py`, which exposes two operations the agent calls: `search "<query>"` and `scrape "<url>"`. The agent never imports these libraries directly.
