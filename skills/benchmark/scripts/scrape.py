#!/usr/bin/env python3
"""
scrape.py — Universal web scraper for benchmark skill.
Returns clean Markdown from a URL, using the best available tool.

Priority:
  1. Crawl4AI (local, JS rendering) — if installed
  2. Jina Reader (r.jina.ai) — free cloud API, zero setup
  3. Fallback error message

Usage:
  python3 scrape.py <url>
  python3 scrape.py <url> --check   # just check which scraper is available
"""

import sys
import asyncio
import json
import os
import re
import subprocess

# Fix Windows cp1252 crash: Rich (used by Crawl4AI) tries to encode Unicode chars
# (e.g. → \u2192) via the Windows console codec cp1252 which doesn't support them.
# Reconfiguring stdout/stderr to UTF-8 before any Rich/Crawl4AI import solves this.
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Below this, extracted text is not usable content and saying so beats returning noise.
MIN_USABLE_CHARS = 200
# The block cut must keep at least this share of what the line filter kept.
BLOCK_CUT_MIN_RATIO = 0.35
# Above the floor but this thin means the page did not really yield its content.
THIN_CONTENT_CHARS = 1200

# A consent declaration is not page content. On CMP-heavy sites (Cookiebot and
# friends) the cookie policy and its tables can be the whole extraction, which
# buries the offer and burns tokens for nothing.
CONSENT_LINE_RE = re.compile(
    r"(cookies? (sont|are)|d(é|e)claration relative aux cookies|cookie declaration"
    r"|politique de confidentialit(é|e)|privacy policy"
    r"|Cookie HTTP|Stockage local HTML|HTML Local Storage"
    r"|votre (é|e)tat .*actuel|identifiant de votre consentement"
    r"|consent (id|date)|retirez consentement|modifiez consentement"
    r"|n(é|e)cessaires \(\d+\)|pr(é|e)f(é|e)rences \(\d+\)|statistiques \(\d+\)|marketing \(\d+\))",
    re.IGNORECASE,
)


def load_consent() -> dict:
    """consent.json is the single home for CMP selectors and blocker markers."""
    try:
        with open(os.path.join(SCRIPT_DIR, "consent.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def load_consent_selectors() -> list:
    return load_consent().get("kill_selectors", [])


def classify_page(text: str) -> str:
    """Return a blocker class (not-found, waf, captcha, login...) or empty string.

    Content-based on purpose: Crawl4AI reports the redirect status, not the final
    one, so a 404 reached through a 301 is indistinguishable by status code.

    Scans the whole text. A 6000-char window made detection depend on page layout:
    the same 404 was caught on one site and missed on another.
    """
    haystack = text.lower()
    for blocker, markers in load_consent().get("blocker_markers", {}).items():
        for m in markers:
            if m in haystack:
                return blocker
    return ""


def _line_filter(lines: list) -> str:
    """Drop consent lines. Deterministic: same input, same amount removed."""
    kept = [l for l in lines if not CONSENT_LINE_RE.search(l)]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()


def strip_consent(md: str) -> str:
    """Remove the consent declaration, without ever emptying the page.

    Two strategies, and the safer one wins. The line filter is deterministic and
    cannot remove more than the consent lines themselves. The block cut also
    removes the descriptive CMP paragraphs a line filter cannot catch, but how
    much it removes depends on where the last marker falls, which varies from page
    to page: it left 19k characters on one page of a site and under the rejection
    floor on another. So the block cut is only kept when it preserves most of what
    the line filter found.
    """
    lines = md.split("\n")
    filtered = _line_filter(lines)
    if not filtered:
        return ""

    limit = int(len(lines) * 0.6)
    last = -1
    for i, line in enumerate(lines[:limit]):
        if CONSENT_LINE_RE.search(line):
            last = i
    if last < 0:
        return filtered

    cut_out = _line_filter(lines[last + 1:])

    # Guard: the block cut must not be the thing that empties the page.
    if len(cut_out) >= max(MIN_USABLE_CHARS, int(len(filtered) * BLOCK_CUT_MIN_RATIO)):
        return "<!-- consent-stripped:block -->\n" + cut_out
    return "<!-- consent-stripped:lines (block cut rejected, would have kept %d of %d chars) -->\n%s" % (
        len(cut_out), len(filtered), filtered)


def finalize(md: str, url: str) -> str:
    """Strip consent, then refuse to pass off an error page or an empty page as content.

    Classification runs on the stripped text, not the raw one: a CMP declaration
    can be 100 kB, which pushes the real page message far out of any scan window.
    """
    out = strip_consent(md)
    blocker = classify_page(out)
    if blocker:
        return "[SCRAPE ERROR — %s for %s: page not usable, do not cite this URL]" % (blocker, url)
    body = re.sub(r"<!--.*?-->", "", out).strip()
    if MIN_USABLE_CHARS <= len(body) < THIN_CONTENT_CHARS:
        warning = ("<!-- thin-content:%d chars — the page is probably JS-hydrated. Do not "
                   "conclude the data is absent from this actor: try another URL, or "
                   "capture the page. -->" % len(body))
        out = warning + "\n" + out
    if len(body) < MIN_USABLE_CHARS:
        raw_body = re.sub(r"<!--.*?-->", "", md).strip()
        return ("[SCRAPE ERROR — no usable content for %s (%d usable chars out of %d raw; "
                "the page is probably JS-hydrated, or its content is entirely inside the "
                "consent dialog)]" % (url, len(body), len(raw_body)))
    return out


def check_crawl4ai() -> bool:
    """Returns True if Crawl4AI is installed."""
    try:
        import crawl4ai  # noqa: F401
        return True
    except ImportError:
        return False


async def scrape_with_crawl4ai(url: str) -> str:
    """Scrape using Crawl4AI with Fit Markdown mode (removes boilerplate)."""
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
    selectors = ",".join(load_consent_selectors())
    result = None
    for kwargs in ({"excluded_selector": selectors} if selectors else {}, {}):
        try:
            config = CrawlerRunConfig(**kwargs)
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url, config=config)
            break
        except TypeError:
            continue
    if result is None:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)

    # A 404 served with a styled error page looks like a successful scrape.
    # Surface the status or the whole pipeline treats a dead URL as evidence.
    status = getattr(result, "status_code", None)
    if status and int(status) >= 400:
        return "[SCRAPE ERROR — HTTP %s for %s: the page does not exist or is not accessible]" % (status, url)

    if result.success:
        # Try to get fit_markdown first, then raw markdown
        if hasattr(result, 'markdown_v2') and result.markdown_v2:
            md = getattr(result.markdown_v2, 'fit_markdown', None) or getattr(result.markdown_v2, 'raw_markdown', None)
            if md:
                return finalize(md, url)
        if hasattr(result, 'fit_markdown') and result.fit_markdown:
            return finalize(result.fit_markdown, url)
        if hasattr(result, 'markdown') and result.markdown:
            md = result.markdown if isinstance(result.markdown, str) else str(result.markdown)
            return finalize(md, url)
        return "[SCRAPE ERROR — Crawl4AI returned empty content]"
    else:
        err = getattr(result, 'error_message', 'unknown error')
        return f"[SCRAPE ERROR — Crawl4AI failed: {err}]"


def scrape_with_jina(url: str) -> str:
    """Scrape using Jina Reader free API (no JS rendering)."""
    jina_url = f"https://r.jina.ai/{url}"
    result = subprocess.run(
        ["curl", "-s", "--max-time", "20", "-A",
         "Mozilla/5.0 (compatible; benchmark/1.0)",
         "-w", "\n<!-- http-status:%{http_code} -->",
         jina_url],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        m = re.search(r"<!-- http-status:(\d+) -->", result.stdout)
        if m and int(m.group(1)) >= 400:
            return "[SCRAPE ERROR — HTTP %s for %s: the page does not exist or is not accessible]" % (m.group(1), url)
        return finalize(result.stdout, url)
    return f"[SCRAPE ERROR — Jina Reader failed for {url}]"


def detect_scraper() -> str:
    """Returns which scraper is available: 'crawl4ai', 'jina', or 'none'."""
    if check_crawl4ai():
        return "crawl4ai"
    # Quick connectivity check for Jina Reader
    result = subprocess.run(
        ["curl", "-s", "--max-time", "5", "-o", "/dev/null",
         "-w", "%{http_code}",
         "https://r.jina.ai/https://example.com"],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip() in ("200", "301", "302"):
        return "jina"
    return "none"


async def scrape(url: str) -> tuple[str, str]:
    """
    Scrape a URL and return (markdown_content, scraper_used).
    Falls back gracefully through the scraper hierarchy.
    Crawl4AI → Jina Reader → error message.
    """
    if check_crawl4ai():
        try:
            content = await scrape_with_crawl4ai(url)
            if content and not content.startswith("[SCRAPE ERROR"):
                return content, "crawl4ai"
            # Crawl4AI returned error → fall through to Jina
        except Exception as e:
            # Handles UnicodeEncodeError from Rich on Windows cp1252,
            # and any other runtime crash from Crawl4AI internals.
            print(f"<!-- crawl4ai-error:{type(e).__name__} — falling back to jina -->",
                  file=sys.stderr)
    content = scrape_with_jina(url)
    return content, "jina"


async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scrape.py <url> [--check]", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--check":
        scraper = detect_scraper()
        print(f"scraper={scraper}")
        return

    url = sys.argv[1]

    # Optional: --check flag after url
    if len(sys.argv) > 2 and sys.argv[2] == "--check":
        scraper = detect_scraper()
        print(f"scraper={scraper}")
        return

    content, scraper_used = await scrape(url)
    print(f"<!-- scraped-by:{scraper_used} url:{url} -->")
    print(content)


if __name__ == "__main__":
    asyncio.run(main())
