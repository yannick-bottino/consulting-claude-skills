# Screenshot Capture Spec

Operational reference. Read before Step 1.4 (capture pass) and before generating the HTML report.

A screenshot in a benchmark is evidence, not decoration. It carries a claim, a URL and a date, or it does not ship.

## Contents
1. Capture levels
2. Intent taxonomy
3. Nomination (actor subagents)
4. Capture plan format
5. Running the capture
6. Manifest and statuses
7. Evidence and legal rules
8. Conditional vision extraction
9. Weight budget

---

## 1. Capture levels

Same three-level logic as the scraper. Detect once, at Phase 0.

| Level | Tool | When |
|-------|------|------|
| 1 | `scripts/capture.py` (Playwright) | Default whenever Bash and Chromium are available |
| 2 | Firecrawl `screenshot` action | No local browser (claude.ai, restricted Cowork). One request per target, no interaction support |
| 3 | None | Report shows a discreet link to the official page. Never a placeholder frame |

```bash
python {skill_path}/scripts/capture.py --check
# capture=playwright derivatives=pillow | capture=playwright derivatives=none | capture=none
```

Level 1 is sequential by design: one browser, one context per actor. Parallel contexts run faster and produce visually inconsistent screenshots (different lazy-load timings, different consent states). In a client deliverable, consistency beats speed.

---

## 2. Intent taxonomy

Intents are generic. The profile (`references/profiles/<nature>.md`) maps which intents matter and what each one must show. Never invent a sector-specific intent name.

| Intent | What it must show |
|--------|-------------------|
| `home` | Hero and headline promise, above the fold |
| `offer` | The offer or product page central to the benchmark |
| `pricing` | The price grid, simulator, or rate table. Prefer a selector on the table itself |
| `funnel_step` | One step of the subscription or quote path, when the path is a differentiator |
| `proof` | The page carrying a certification, a published report, a commitment, a third-party attribution |
| `comparison` | A comparison table published by the actor itself |

A target may repeat an intent with a suffix (`funnel_step`, `funnel_step-2`). Keep at most 3 targets per actor unless the mission asks otherwise: beyond that, the report turns into a gallery and nobody reads it.

---

## 3. Nomination (actor subagents)

Actor subagents do **not** launch browsers. They nominate, because they are the only ones who know which URL proves which claim. Each nomination is emitted in the actor JSON as `capture_targets`.

Nomination rules:
- Only URLs the subagent actually visited or scraped. Never a guessed URL.
- Attach the claim the screenshot proves, and the `comparable_ref` when it backs a figure.
- Provide `selector_hint` when the evidence is a specific block (a price table, a certification badge). A selector capture beats a full page every time.
- Mark `full_page: true` only when the whole page is the evidence.

---

## 4. Capture plan format

The orchestrator merges all nominations into `outputs/{mission-slug}/capture-plan.json`:

```json
{
  "mission_slug": "…",
  "locale": "fr-FR",
  "targets": [
    {
      "actor_slug": "…",
      "actor_name": "…",
      "intent": "pricing",
      "url": "https://…",
      "selector": ".pricing-table",
      "full_page": false,
      "actions": [{"click": "button:has-text('Mensuel')"}, {"wait_ms": 800}],
      "claim": "419 EUR/mois sur 1 mois",
      "comparable_ref": "c12"
    }
  ]
}
```

`actions` runs before the shot: use it for a price toggle, a tab, or a duration selector. Every action failure is silent by design, the capture still happens.

---

## 5. Running the capture

```bash
python {skill_path}/scripts/capture.py \
  --plan "outputs/{mission-slug}/capture-plan.json" \
  --out "outputs/{mission-slug}/actors/screenshots"
```

Defaults: viewport 1440x900, device scale factor 2, 20 s navigation timeout, web derivative at 1200 px wide, JPEG quality 72, caption bar stamped.

Determinism applied to every page before the shot: trackers blocked, animations and transitions frozen, reduced motion, full scroll to trigger lazy loading then back to top, fixed and sticky elements hidden on full-page shots, consent banner dismissed through `scripts/consent.json`.

Re-running skips targets whose file already exists. Use `--force` to recapture. This makes the capture pass resumable like the rest of the skill.

**Consent handling is data, not code.** When a banner survives a mission, add its handler to `scripts/consent.json` and the fix applies to every future mission. Do not patch the script.

---

## 6. Manifest and statuses

`capture.py` writes `outputs/{mission-slug}/actors/screenshots/capture-manifest.json`. It is the only source of truth for what exists.

| Status | Meaning | Downstream |
|--------|---------|-----------|
| `ok` | File captured or reused | Displayed in the report |
| `blocked` | Page reachable but unusable: `captcha`, `waf`, `login`, `geoblock`, `empty-page` | Structural gap, documented, never retried in a loop |
| `failed` | Transient navigation or screenshot error | Retried once at most, then structural gap |
| `skipped` | Behind a login, a paywall, or a personal account | Never attempted, documented |

Structural blockers are never retried: `captcha`, `waf`, `geoblock`, `http-4xx`, `cert-expired`. Retrying them burns a pass and changes nothing. An expired TLS certificate is the awkward case: the scraper may well read the page (Crawl4AI ignores certificate errors) while the browser refuses it, so the URL stays citable under rule S4 while its visual proof is impossible. Say so in the sources section rather than retrying.

Retry only `failed`, and only with:

```bash
python {skill_path}/scripts/capture.py --plan "outputs/{mission-slug}/capture-plan.json" \
  --out "outputs/{mission-slug}/actors/screenshots" --only-status failed
```

Never build a reduced plan by hand to retry a subset. The manifest is merged, not overwritten, so a full plan with `--only-status` is both safe and sufficient.

Each entry carries `path`, `path_web`, `sha256`, `viewport`, `captured_at`, `consent_handler`, `selector_used`, plus the nominated `claim` and `comparable_ref`.

**The manifest is authoritative, always.** `actors[].screenshots` and `benchmark.json` are copies of it, and a copy goes stale the moment a target is recaptured. Rules:

- Re-fold the manifest into `actors[].screenshots` after **every** capture pass, including a partial retry.
- Re-fold again at assembly (Step 4.1) before writing `benchmark.json`.
- On any disagreement between a copy and the manifest, the manifest wins and the copy is regenerated. Never reconcile by hand.
- A capture that ends `blocked` or `failed` carries no path. If a file from an earlier attempt is still on disk, it is an orphan: the manifest does not reference it and nothing may display it. A stale PNG with a valid hash is more dangerous than no file at all, because it looks verifiable.

---

## 7. Evidence and legal rules

- Every derivative carries a caption bar: actor, intent, full URL, capture date. Never remove it, never crop a competitor's branding out of a shot. A screenshot presented without its source is an unsourced claim (rule D2).
- A screenshot of a displayed price **is** an acceptable verbatim for that figure (rule D3): reference it in `sources[]` with its path and date.
- Never capture content behind a login, a paywall, or a personal account. Mark it `skipped` and say so.
- Never reuse a screenshot from a previous mission: prices and pages change, and a stale capture presented as current is a fabrication.

---

## 8. Conditional vision extraction

Reading a screenshot with vision costs roughly 700 to 1500 tokens. Run it only where text extraction failed:

Run vision on a `pricing` or `proof` shot when, and only when, the corresponding field is empty, missing-marked, or listed in `uncertain_fields`. Skip it entirely when the value was already extracted from text.

When vision yields a value, record it with `confidence: "observed"` and a source entry pointing at the screenshot path plus the origin URL.

---

## 9. Weight budget

The HTML report is self-contained, so every displayed screenshot is inlined base64 with a 33% overhead.

- Inline **web derivatives only** (`path_web`), never the original PNG.
- Target under 250 KB per derivative. A 1200 px full-page shot of a dense landing page lands around 90 to 200 KB.
- Budget: 10 actors x 3 shots x 150 KB x 1.33 is roughly 6 MB of HTML. Above 12 MB, drop to the top 2 intents per actor and say so in the report.
- Originals stay on disk at full resolution for deck production. They are never inlined.
