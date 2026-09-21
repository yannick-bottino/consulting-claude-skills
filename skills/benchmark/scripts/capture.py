#!/usr/bin/env python3
"""
capture.py — Deterministic screenshot capture for benchmark evidence.

Usage:
  python scripts/capture.py --check
  python scripts/capture.py --plan <capture-plan.json> --out <screenshots-dir> [options]

Options:
  --viewport WxH        Desktop viewport (default 1440x900)
  --scale N             Device scale factor (default 2)
  --timeout MS          Per-page navigation timeout (default 20000)
  --manifest PATH       Manifest output (default <out>/capture-manifest.json)
  --consent PATH        Consent handler file (default <script dir>/consent.json)
  --web-width N         Max width of the web derivative (default 1200)
  --web-quality N       JPEG quality of the web derivative (default 72)
  --no-derivatives      Skip web derivatives (originals only)
  --no-caption          Skip the caption bar on derivatives
  --force               Recapture targets whose files already exist
  --only-status S       Recapture only targets whose current manifest status is S
                        (failed, blocked, comma-separated). Implies --force on them.
  --limit N             Stop after N targets (smoke tests)

The manifest is MERGED, never overwritten: a partial re-run keeps the entries of the
targets it did not touch. Overwriting it destroyed the record of successful captures
whenever a partial plan was passed, which is exactly what a retry pass needs to do.

Captures are sequential by design: one browser, one context per actor. Parallel
contexts give faster runs and inconsistent screenshots (different lazy-load
timings, different consent states). Consistency wins for a client deliverable.

Exit codes: 0 = ran (see manifest for per-target status), 2 = fatal setup error.
Never returns non-zero for a blocked site: screenshots are evidence, not a gate.
"""

import argparse
import hashlib
import json
import os
import sys
import datetime

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Injected before every capture: kills motion so two runs of the same page match.
FREEZE_CSS = """
*, *::before, *::after {
  animation-duration: 0s !important;
  animation-delay: 0s !important;
  transition-duration: 0s !important;
  transition-delay: 0s !important;
  scroll-behavior: auto !important;
}
"""

HIDE_FIXED_JS = """
() => {
  const hidden = [];
  document.querySelectorAll('body *').forEach(el => {
    const s = window.getComputedStyle(el);
    if ((s.position === 'fixed' || s.position === 'sticky') && s.display !== 'none') {
      const r = el.getBoundingClientRect();
      if (r.height > 0 && r.width > 0) {
        hidden.push(el);
        el.setAttribute('data-capture-hidden', '1');
        el.style.setProperty('display', 'none', 'important');
      }
    }
  });
  return hidden.length;
}
"""

LAZY_LOAD_JS = """
async () => {
  const step = Math.round(window.innerHeight * 0.8);
  const max = document.body.scrollHeight;
  for (let y = 0; y < max; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 120));
  }
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 250));
}
"""


def check_availability():
    """Print capture=playwright|none, mirroring scrape.py --check."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("capture=none")
        print("Playwright not installed. Run scripts/setup-scraper.sh", file=sys.stderr)
        return 1
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            b.close()
    except Exception as exc:
        print("capture=none")
        print("Chromium not installed: %s" % exc, file=sys.stderr)
        return 1
    try:
        import PIL  # noqa: F401
        print("capture=playwright derivatives=pillow")
    except ImportError:
        print("capture=playwright derivatives=none")
    return 0


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def dismiss_consent(page, consent, timeout=2500):
    """Return the handler name that dismissed the banner, or None."""
    for handler in consent.get("handlers", []):
        for sel in handler.get("selectors", []):
            try:
                loc = page.locator(sel).first
                if loc.count() and loc.is_visible(timeout=600):
                    loc.click(timeout=timeout)
                    page.wait_for_timeout(600)
                    return handler["name"]
            except Exception:
                pass
        if handler.get("search_frames"):
            for frame in page.frames[1:]:
                for sel in handler.get("selectors", []):
                    try:
                        loc = frame.locator(sel).first
                        if loc.count() and loc.is_visible(timeout=400):
                            loc.click(timeout=timeout)
                            page.wait_for_timeout(600)
                            return handler["name"] + "/iframe"
                    except Exception:
                        pass

    for _lang, labels in consent.get("text_buttons", {}).items():
        for label in labels:
            try:
                loc = page.get_by_role("button", name=label, exact=False).first
                if loc.count() and loc.is_visible(timeout=400):
                    loc.click(timeout=timeout)
                    page.wait_for_timeout(600)
                    return "text:%s" % label
            except Exception:
                pass

    killed = 0
    for sel in consent.get("kill_selectors", []):
        try:
            killed += page.evaluate(
                "(s) => { const n = document.querySelectorAll(s); n.forEach(e => e.remove()); return n.length; }",
                sel,
            )
        except Exception:
            pass
    return "dom-removal" if killed else None


def detect_blocker(page, consent):
    """Classify a page that loaded but shows no usable content."""
    try:
        body = (page.inner_text("body", timeout=3000) or "")[:4000].lower()
        title = (page.title() or "").lower()
    except Exception:
        return "unreadable"
    haystack = title + " " + body
    for blocker, markers in consent.get("blocker_markers", {}).items():
        for m in markers:
            if m in haystack:
                return blocker
    if len(body.strip()) < 120:
        return "empty-page"
    return None


def make_derivative(src, dest, caption_lines, max_width, quality, draw_caption=True):
    """Downscale to a report-sized JPEG and stamp the provenance caption."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None

    img = Image.open(src).convert("RGB")
    if img.width > max_width:
        ratio = max_width / float(img.width)
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

    # Very tall full-page shots are unreadable in a report and heavy to inline.
    max_height = max_width * 3
    if img.height > max_height:
        img = img.crop((0, 0, img.width, max_height))

    if draw_caption and caption_lines:
        bar = 22 * len(caption_lines) + 16
        canvas = Image.new("RGB", (img.width, img.height + bar), "#111318")
        canvas.paste(img, (0, 0))
        draw = ImageDraw.Draw(canvas)
        font = None
        for candidate in ("arial.ttf", "DejaVuSans.ttf", "Helvetica.ttc"):
            try:
                font = ImageFont.truetype(candidate, 14)
                break
            except Exception:
                continue
        if font is None:
            font = ImageFont.load_default()
        y = img.height + 8
        for i, line in enumerate(caption_lines):
            draw.text((12, y), line, fill="#FFFFFF" if i == 0 else "#A8B0BC", font=font)
            y += 22
        img = canvas

    img.save(dest, "JPEG", quality=quality, optimize=True)
    return dest


def capture_target(page, target, args, consent, out_dir, today):
    """Capture one target. Returns a manifest entry, never raises."""
    slug = target["actor_slug"]
    intent = target["intent"]
    url = target["url"]
    base = "%s-%s" % (slug, intent)
    png_path = os.path.join(out_dir, base + ".png")
    web_path = os.path.join(out_dir, base + ".web.jpg")

    entry = {
        "actor_slug": slug,
        "actor_name": target.get("actor_name", slug),
        "intent": intent,
        "url": url,
        "claim": target.get("claim"),
        "comparable_ref": target.get("comparable_ref"),
        "status": "failed",
        "blocker": None,
        "path": None,
        "path_web": None,
        "selector_used": None,
        "consent_handler": None,
        "viewport": "%dx%d" % (args.vw, args.vh),
        "device_scale_factor": args.scale,
        "captured_at": today,
    }

    def drop_orphans():
        removed = []
        for p in (png_path, web_path):
            if os.path.exists(p):
                try:
                    os.remove(p)
                    removed.append(os.path.basename(p))
                except OSError:
                    pass
        return removed

    if os.path.exists(png_path) and not args.force:
        entry.update({"status": "ok", "path": png_path, "reused": True,
                      "path_web": web_path if os.path.exists(web_path) else None,
                      "bytes": os.path.getsize(png_path), "sha256": sha256_of(png_path)})
        return entry

    try:
        response = page.goto(url, timeout=args.timeout, wait_until="domcontentloaded")
    except Exception as exc:
        message = str(exc)
        # An expired certificate or an unresolvable host is structural: labelling it
        # "failed" makes the retry pass burn attempts on something that cannot change.
        for blocker, needles in (consent.get("navigation_blockers") or {}).items():
            if any(n.lower() in message.lower() for n in needles):
                entry["status"] = "blocked"
                entry["blocker"] = blocker
                return entry
        entry["blocker"] = "navigation: %s" % message[:120]
        return entry

    # A 404 served with the site's own styling captures cleanly and looks like
    # evidence. Trust the status code, not the pixels.
    http_status = response.status if response is not None else None
    entry["http_status"] = http_status
    if http_status and http_status >= 400:
        entry["status"] = "blocked"
        entry["blocker"] = "http-%d" % http_status
        entry["orphans_removed"] = drop_orphans()
        return entry

    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass

    entry["consent_handler"] = dismiss_consent(page, consent)

    blocker = detect_blocker(page, consent)
    if blocker:
        entry["status"] = "blocked"
        entry["blocker"] = blocker
        entry["orphans_removed"] = drop_orphans()
        return entry

    try:
        page.add_style_tag(content=FREEZE_CSS)
        page.evaluate(LAZY_LOAD_JS)
    except Exception:
        pass

    for action in target.get("actions", []) or []:
        try:
            if "click" in action:
                page.locator(action["click"]).first.click(timeout=4000)
            elif "wait_ms" in action:
                page.wait_for_timeout(int(action["wait_ms"]))
            elif "scroll_to" in action:
                page.locator(action["scroll_to"]).first.scroll_into_view_if_needed(timeout=4000)
            page.wait_for_timeout(400)
        except Exception:
            pass

    selector = target.get("selector") or target.get("selector_hint")
    full_page = bool(target.get("full_page", False))

    try:
        if selector:
            loc = page.locator(selector).first
            if loc.count():
                loc.scroll_into_view_if_needed(timeout=4000)
                page.wait_for_timeout(300)
                loc.screenshot(path=png_path)
                entry["selector_used"] = selector
            else:
                selector = None
        if not selector:
            if full_page:
                try:
                    page.evaluate(HIDE_FIXED_JS)
                except Exception:
                    pass
            page.screenshot(path=png_path, full_page=full_page)
    except Exception as exc:
        entry["blocker"] = "screenshot: %s" % str(exc)[:120]
        return entry

    entry["status"] = "ok"
    entry["path"] = png_path
    entry["bytes"] = os.path.getsize(png_path)
    entry["sha256"] = sha256_of(png_path)

    if not args.no_derivatives:
        caption = [
            "%s — %s" % (entry["actor_name"], intent),
            "%s · capturé le %s" % (url[:110], today),
        ]
        made = make_derivative(png_path, web_path, caption, args.web_width,
                               args.web_quality, draw_caption=not args.no_caption)
        if made:
            entry["path_web"] = web_path
            entry["bytes_web"] = os.path.getsize(web_path)

    return entry


def run(args):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FATAL: Playwright not installed. Run scripts/setup-scraper.sh", file=sys.stderr)
        return 2

    plan = load_json(args.plan)
    targets = plan.get("targets", [])
    if args.limit:
        targets = targets[: args.limit]
    if not targets:
        print("No targets in plan — nothing to capture.")
        return 0

    consent = load_json(args.consent)
    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)
    today = datetime.date.today().isoformat()

    manifest_path = args.manifest or os.path.join(out_dir, "capture-manifest.json")
    previous = {}
    if os.path.exists(manifest_path):
        try:
            for e in load_json(manifest_path).get("captures", []):
                previous[(e.get("actor_slug"), e.get("intent"))] = e
        except Exception:
            previous = {}

    if args.only_status:
        wanted = {x.strip() for x in args.only_status.split(",")}
        before = len(targets)
        targets = [t for t in targets
                   if (previous.get((t.get("actor_slug"), t.get("intent"))) or {}).get("status") in wanted]
        args.force = True
        print("--only-status %s: %d of %d targets selected" % (args.only_status, len(targets), before))
        if not targets:
            print("Nothing to retry.")
            return 0

    by_actor = {}
    for t in targets:
        by_actor.setdefault(t["actor_slug"], []).append(t)

    entries = []
    blocked_domains = consent.get("block_domains", [])

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
        try:
            for slug, actor_targets in by_actor.items():
                context = browser.new_context(
                    viewport={"width": args.vw, "height": args.vh},
                    device_scale_factor=args.scale,
                    locale=plan.get("locale", "fr-FR"),
                    reduced_motion="reduce",
                    user_agent=plan.get("user_agent"),
                )
                if blocked_domains:
                    context.route(
                        "**/*",
                        lambda route: route.abort()
                        if any(d in route.request.url for d in blocked_domains)
                        else route.continue_(),
                    )
                page = context.new_page()
                for t in actor_targets:
                    entry = capture_target(page, t, args, consent, out_dir, today)
                    entries.append(entry)
                    mark = {"ok": "OK", "blocked": "BLOCKED", "failed": "FAILED"}.get(entry["status"], "?")
                    print("  %-8s %s/%s  %s" % (mark, slug, t["intent"], entry.get("blocker") or ""))
                context.close()
        finally:
            browser.close()

    # Merge, never overwrite: entries this run did not touch survive.
    merged = dict(previous)
    for e in entries:
        merged[(e["actor_slug"], e["intent"])] = e
    entries = list(merged.values())

    manifest = {
        "mission_slug": plan.get("mission_slug"),
        "generated_at": today,
        "viewport": "%dx%d" % (args.vw, args.vh),
        "device_scale_factor": args.scale,
        "counts": {
            "total": len(entries),
            "ok": sum(1 for e in entries if e["status"] == "ok"),
            "blocked": sum(1 for e in entries if e["status"] == "blocked"),
            "failed": sum(1 for e in entries if e["status"] == "failed"),
        },
        "captures": entries,
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    c = manifest["counts"]
    print("\n%d captures: %d ok, %d blocked, %d failed" % (c["total"], c["ok"], c["blocked"], c["failed"]))
    print("Manifest: %s" % manifest_path)
    return 0


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--plan")
    ap.add_argument("--out")
    ap.add_argument("--viewport", default="1440x900")
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=20000)
    ap.add_argument("--manifest")
    ap.add_argument("--consent", default=os.path.join(SCRIPT_DIR, "consent.json"))
    ap.add_argument("--web-width", type=int, default=1200, dest="web_width")
    ap.add_argument("--web-quality", type=int, default=72, dest="web_quality")
    ap.add_argument("--no-derivatives", action="store_true", dest="no_derivatives")
    ap.add_argument("--no-caption", action="store_true", dest="no_caption")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only-status", dest="only_status")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    if args.check:
        return check_availability()
    if not args.plan or not args.out:
        ap.error("--plan and --out are required (or use --check)")

    try:
        args.vw, args.vh = (int(x) for x in args.viewport.lower().split("x"))
    except Exception:
        ap.error("--viewport must be WxH, e.g. 1440x900")

    return run(args)


if __name__ == "__main__":
    sys.exit(main())
