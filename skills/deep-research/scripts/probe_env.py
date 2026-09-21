#!/usr/bin/env python3
"""Probe the runtime environment and pick a retrieval tier.

Writes the result to <notes_dir>/_env.md (default: research-notes/_env.md).
No hooks, no side effects beyond the env file. Works in Cowork and Claude Code.

Tiers:
  T1 Full   : bash + open network + pip + a configured search backend + a scraper lib
  T2 Bridge : bash + python, but no open-network scraper stack (or no search backend)
  T3 Native : python missing / unreliable -> agent must use native web_search/web_fetch

The agent still makes the final call; this is a recommendation it can override
(e.g. force T3 if it knows the sandbox blocks egress regardless of probe result).
"""
import importlib.util
import os
import socket
import sys
from datetime import date

NOTES_DIR = sys.argv[1] if len(sys.argv) > 1 else "research-notes"

# Candidate hosts used only to sense whether arbitrary egress is allowed.
# A real fetch is not made; we only test TCP reachability quickly.
PROBE_HOSTS = [("duckduckgo.com", 443), ("api.search.brave.com", 443)]


def has_module(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def open_network() -> bool:
    """True if we can open a socket to at least one arbitrary host."""
    for host, port in PROBE_HOSTS:
        try:
            with socket.create_connection((host, port), timeout=4):
                return True
        except OSError:
            continue
    return False


def search_backend() -> str | None:
    if os.environ.get("SEARXNG_URL"):
        return "searxng"
    if os.environ.get("BRAVE_API_KEY"):
        return "brave"
    if os.environ.get("TAVILY_API_KEY"):
        return "tavily"
    return None


def decide() -> dict:
    py = sys.version_info >= (3, 9)
    crawl4ai = has_module("crawl4ai")
    scrapling = has_module("scrapling")
    trafilatura = has_module("trafilatura")
    net = open_network()
    backend = search_backend()

    if py and net and backend and (crawl4ai or scrapling):
        tier = "T1"
        reason = f"open net + search backend={backend} + scraper present"
    elif py:
        tier = "T2"
        reason = "python available; no full T1 scraper stack/backend -> bridge via native fetch + cleanup"
    else:
        tier = "T3"
        reason = "python unreliable -> native web_search/web_fetch only"

    return {
        "tier": tier,
        "reason": reason,
        "python_ok": py,
        "open_network": net,
        "search_backend": backend,
        "crawl4ai": crawl4ai,
        "scrapling": scrapling,
        "trafilatura": trafilatura,
    }


def main() -> None:
    info = decide()
    os.makedirs(NOTES_DIR, exist_ok=True)
    path = os.path.join(NOTES_DIR, "_env.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"# Retrieval environment (probed {date.today().isoformat()})\n\n")
        fh.write(f"**TIER: {info['tier']}** — {info['reason']}\n\n")
        fh.write("| capability | value |\n|---|---|\n")
        for k in ("python_ok", "open_network", "search_backend",
                  "crawl4ai", "scrapling", "trafilatura"):
            fh.write(f"| {k} | {info[k]} |\n")
        fh.write("\nSubagents: read the TIER above before issuing retrieval calls. "
                 "T1 -> retrieve.py search/scrape. T2 -> retrieve.py with native fetch. "
                 "T3 -> native web_search + web_fetch (full-page, never snippet-only).\n")
    print(f"[probe] tier={info['tier']} backend={info['search_backend']} "
          f"net={info['open_network']} -> {path}")


if __name__ == "__main__":
    main()
