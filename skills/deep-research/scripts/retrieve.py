#!/usr/bin/env python3
"""Unified retrieval layer for deep-research: search() and scrape().

Two operations, called from the command line by the skill:

    python retrieve.py search "<query>" [--n 8]
    python retrieve.py scrape "<url>"

SEARCH discovers URLs. SCRAPE turns a URL into clean full-page markdown.
The script auto-routes by what is installed/configured (see retrieval_tiers.md):

  search backends (first configured wins): SearXNG -> Brave -> Tavily
  scrape engines (best available wins):    Crawl4AI -> Scrapling -> trafilatura -> raw

If nothing usable is present for an operation, the script prints a structured
NEEDS_NATIVE marker so the agent knows to fall back to native web_search/web_fetch
(T3) instead of failing.

This file degrades cleanly: missing libraries are caught, not fatal. The T1
engine calls (Crawl4AI / Scrapling) only run where those libs + browsers are
installed on the user's own machine; they will not run in a sandbox.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def _emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _have(mod: str) -> bool:
    import importlib.util
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


# --------------------------------------------------------------------------- #
# SEARCH                                                                       #
# --------------------------------------------------------------------------- #
def search_searxng(query: str, n: int) -> list[dict]:
    base = os.environ["SEARXNG_URL"].rstrip("/")
    qs = urllib.parse.urlencode({"q": query, "format": "json"})
    req = urllib.request.Request(f"{base}/search?{qs}",
                                 headers={"User-Agent": "deep-research/7"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    out = []
    for r in data.get("results", [])[:n]:
        out.append({"title": r.get("title", ""), "url": r.get("url", ""),
                    "snippet": r.get("content", "")})
    return out


def search_brave(query: str, n: int) -> list[dict]:
    qs = urllib.parse.urlencode({"q": query, "count": n})
    req = urllib.request.Request(
        f"https://api.search.brave.com/res/v1/web/search?{qs}",
        headers={"X-Subscription-Token": os.environ["BRAVE_API_KEY"],
                 "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    out = []
    for r in data.get("web", {}).get("results", [])[:n]:
        out.append({"title": r.get("title", ""), "url": r.get("url", ""),
                    "snippet": r.get("description", "")})
    return out


def search_tavily(query: str, n: int) -> list[dict]:
    body = json.dumps({"api_key": os.environ["TAVILY_API_KEY"],
                       "query": query, "max_results": n}).encode()
    req = urllib.request.Request("https://api.tavily.com/search", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.load(resp)
    out = []
    for r in data.get("results", [])[:n]:
        out.append({"title": r.get("title", ""), "url": r.get("url", ""),
                    "snippet": r.get("content", "")})
    return out


def do_search(query: str, n: int) -> None:
    backends = []
    if os.environ.get("SEARXNG_URL"):
        backends.append(("searxng", search_searxng))
    if os.environ.get("BRAVE_API_KEY"):
        backends.append(("brave", search_brave))
    if os.environ.get("TAVILY_API_KEY"):
        backends.append(("tavily", search_tavily))

    if not backends:
        _emit({"op": "search", "status": "NEEDS_NATIVE",
               "reason": "no search backend configured (SEARXNG_URL/BRAVE_API_KEY/TAVILY_API_KEY)",
               "query": query})
        return

    for name, fn in backends:
        try:
            results = fn(query, n)
            _emit({"op": "search", "status": "ok", "backend": name,
                   "query": query, "results": results})
            return
        except Exception as exc:  # noqa: BLE001 - backend down -> try next
            last = f"{name}: {exc}"
    _emit({"op": "search", "status": "NEEDS_NATIVE",
           "reason": f"all backends failed ({last})", "query": query})


# --------------------------------------------------------------------------- #
# SCRAPE                                                                       #
# --------------------------------------------------------------------------- #
def scrape_crawl4ai(url: str) -> str:
    import asyncio
    from crawl4ai import AsyncWebCrawler

    async def run() -> str:
        async with AsyncWebCrawler() as crawler:
            res = await crawler.arun(url=url)
            return res.markdown or ""
    return asyncio.run(run())


def scrape_scrapling(url: str) -> str:
    # StealthyFetcher: heavier, used when the default engine is blocked.
    from scrapling.fetchers import StealthyFetcher
    page = StealthyFetcher.fetch(url, headless=True, network_idle=True)
    text = page.get_all_text(ignore_tags=("script", "style"))
    return text or ""


def scrape_trafilatura(url: str) -> str:
    import trafilatura
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    return trafilatura.extract(downloaded, output_format="markdown",
                               include_links=True) or ""


def do_scrape(url: str) -> None:
    # Best engine first; fall through on failure or empty content.
    engines = []
    if _have("crawl4ai"):
        engines.append(("crawl4ai", scrape_crawl4ai))
    if _have("scrapling"):
        engines.append(("scrapling", scrape_scrapling))
    if _have("trafilatura"):
        engines.append(("trafilatura", scrape_trafilatura))

    if not engines:
        _emit({"op": "scrape", "status": "NEEDS_NATIVE",
               "reason": "no scraper installed (crawl4ai/scrapling/trafilatura)",
               "url": url})
        return

    errors = []
    for name, fn in engines:
        try:
            md = fn(url)
            if md and md.strip():
                _emit({"op": "scrape", "status": "ok", "engine": name,
                       "url": url, "chars": len(md), "markdown": md})
                return
            errors.append(f"{name}: empty")
        except Exception as exc:  # noqa: BLE001 - try next engine
            errors.append(f"{name}: {exc}")
    _emit({"op": "scrape", "status": "NEEDS_NATIVE",
           "reason": f"all engines failed/empty ({'; '.join(errors)})", "url": url})


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="Unified search/scrape retrieval")
    sub = ap.add_subparsers(dest="op", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--n", type=int, default=8)
    c = sub.add_parser("scrape")
    c.add_argument("url")
    args = ap.parse_args()

    if args.op == "search":
        do_search(args.query, args.n)
    elif args.op == "scrape":
        do_scrape(args.url)


if __name__ == "__main__":
    main()
