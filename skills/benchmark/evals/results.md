# Eval Results

One row per eval run. Append, never overwrite: the value is in the trend.

---

## Run 1 — 2026-07-29 — reduced `offer` mission, 2 actors

**Case:** eval 7 reduced. Swiss shared-mobility offers, `nature: offer`, `sector: mobilite`, `locale: CH / CHF / fr`, deliverables `actor-sheets` + `pricing-synthesis` + `screenshots`. Actors: Sharego, Alpaloc. Executed end to end: mission config, scrape, actor JSONs with comparables, actor validation, capture pass, assembly, benchmark validation.

**Scope of what this run tests, and what it does not**

| Creator criterion | Tested | Verdict |
|---|---|---|
| 1. Executes the process in SKILL.md order | No | The executor was the skill's author. Self-reported compliance proves nothing. Needs a fresh session |
| 2. Loads the reference files its steps point to | No | Same reason |
| 3. Uses the connector correctly | Yes (scripts, schemas, validator, capture, applicability math) | 10 defects found, listed below |

The machinery was exercised for real: live scraping, live capture, real validation runs. The process-compliance half of the eval is still owed and needs the prompt in `templates/eval-prompt.md` pasted into a fresh session.

### Defects found

| # | Severity | Defect | Status |
|---|---|---|---|
| 1 | Blocking | The actor research prompt never mentioned `comparables` or `comparability`. The v3 long-format model was defined, wired into Phase 3a and Phase 4, but no subagent was ever told to produce rows, and no actor-level carrier existed in the schema. The model was unreachable from the pipeline meant to feed it | Fixed |
| 2 | Blocking | A dead URL became evidence. `https://www.sharego.example/fr/abonnements` is a 404. `scrape.py` returned it as content, the actor file cited it as a source with a retrieval date, and `capture.py` filed the capture as `status: ok`. The HTML report would have displayed a competitor's 404 page in a browser frame, captioned as the pricing grid | Fixed |
| 3 | Major | On CMP-heavy sites, `scrape.py` returned the consent declaration instead of the page. Measured on Sharego: 219 lines of cookie policy and cookie tables, zero usable content in the first 90 lines. Consent was handled in `capture.py` only | Fixed |
| 4 | Major | The validator demanded `vehicle_catalog` and `optional_services` on v3 actors, where those are projections generated at assembly. A correct v3 actor lost 6 points of coverage for not hand-authoring generated fields | Fixed |
| 5 | Major | The benchmark validator ignored `deliverables` and warned about `market_landscape`, `roue_concurrentielle` and `recommendation` on a mission that ordered none of them. Same non-applicability defect as the original fixed /80 scorecard | Fixed |
| 6 | Major | Scorecard C5 and C6 were unconditional core sections, but both map to optional deliverables. A mission ordering only actor sheets was scored on a market landscape it never ordered | Fixed |
| 7 | Minor | Actor-level comparables were not validated at all: row checks ran only at assembly. A subagent could emit malformed rows and pass its own quality gate | Fixed |
| 8 | Minor | `confidence: absent` carrying a value was not caught. The run produced exactly that error (`euc-price-1m` with `value_text: "sur simulation"`), which is the drift the enum exists to prevent | Fixed |
| 9 | Minor | Template 5 duplicated `reference_product`, currency and periods between `comparability` and `scope`. Two homes for the same three facts, in the same file | Fixed |
| 10 | Minor | Template 5's default `deliverables` omitted `screenshots`, and Step 1.4 skips the capture pass when it is absent. A consultant following the template got no screenshots after asking for them | Fixed |

### Notable non-defect

Crawl4AI reports the redirect status (301), not the final one, so a 404 reached through a redirect is invisible to a status check in `scrape.py`. Detection there is content-based, using the `blocker_markers` in `scripts/consent.json`. `capture.py` gets the real final status from Playwright and uses it directly. Same outcome, two mechanisms, one reason: the tools do not expose the same truth.

### Verification after fixes

- Same 404 URL: `scrape.py` returns an explicit `[SCRAPE ERROR — ...]`, `capture.py` returns `blocked / http-404`.
- Same real page: 219 consent lines stripped, product and pricing navigation preserved (15 content markers).
- `example.com` still scrapes normally: no false positive from the error detection.
- Eval mission revalidated: both actors and the assembled benchmark at 100% coverage, 0 FAIL, 0 WARN.
- Regression suites: 9/9 price-detection cases across 6 currencies, 9/9 comparables validation cases.

### Next actions

1. Run the process-compliance half in a fresh session with the prompt from `templates/eval-prompt.md`, on the same reduced case. Criteria 1 and 2 are still unverified.
2. Nomination discipline has no enforcement point. The rule says "only URLs the subagent actually visited", and this run violated it with a plausible-looking guess that nothing caught until the capture. Candidate rule: a URL may only be cited as a source if a scrape of it returned usable content.
3. SKILL.md is at 5 553 words. The Phase 0 extraction identified in the last review is still pending.

---

## Run 2 — 2026-07-29 — three fresh-session agents, no build context

Three agents, each given only the skill path, a test input and a budget. None had any knowledge of the skill's construction. None were allowed to modify it.

| Agent | Case | Coverage |
|---|---|---|
| A | `offer`, Swiss shared mobility, 2 actors, Phase 0 to 4 | Process compliance, scripts, schemas |
| B | `maturity`, data and AI at two French insurers, Phase 0 to 4 | Profile routing, method fit |
| C | Phase 5 and 6 on the already-validated mission of run 1 | HTML report, scorecard, 154 lines of never-executed spec |

**Verdict A:** the process skeleton holds. One step out of order in the whole run, and it was forced by an instruction of the skill that destroys its own evidence register.
**Verdict B:** the skeleton holds, and every piece of content injected into it is offer-shaped. The `maturity` profile is an island. 31 places counted.
**Verdict C:** the HTML shell is clean (169 KB, no console error, responsive, no placeholder). What it contains does not stand in front of a client, and the spec forced the agent to arbitrate a data-integrity question alone.

### What the three found in common

1. Abstractions declared but not wired into the files SKILL.md actually loads.
2. Two contradictory sources of truth, in each of the three areas.
3. Validations that reassure wrongly: structural PASS at 100% on a benchmark whose central metric was entirely absent.

### Defects and status

| # | Severity | Defect | Status |
|---|---|---|---|
| 11 | Blocking | Regression from run 1's own fix: the consent block cut was non-deterministic. It left 19 201 chars on one page of a site and under the rejection floor on another, which cost agent A the central price of its benchmark | Fixed: the line filter is the default, the block cut applies only when it keeps at least 35% of it |
| 12 | Blocking | `classify_page` scanned the first 6 000 chars only, so an error page was detected or missed depending on layout | Fixed: scans the whole stripped text |
| 13 | Blocking | Step 1.4 point 4 destroyed the evidence register. It asked to retry only the failed targets; `capture.py` took whole plans and rewrote the manifest with only the targets it was given, so a partial retry erased the successful captures | Fixed: `--only-status`, and the manifest is merged, never overwritten |
| 14 | Blocking | `benchmark.json` and `capture-manifest.json` disagreed on this very mission (`ok` against `blocked/http-404`). The spec named both as source of truth. The other reading ships a competitor's 404 page to the client | Fixed: the manifest wins, re-folding is mandatory at Step 1.4 and Step 4.1, and the validator now fails on any disagreement |
| 15 | Major | The actor prompt, under HARD CONSTRAINT "omit no section", named a car model, a LMD/LCD comparison table and winter tyres, and carried a textile reasoning table as a non-negotiable behavioural rule | Fixed: sector material moved to the sector module (`{sector_reasoning_triggers}`), nature material to the profile (`{nature_structured_fields}`) |
| 16 | Major | The prompt's JSON example showed `offer` sub-fields while the injected block and the validator required the mission's. A subagent following the example failed validation | Fixed: `{dimension_subfields_example}` |
| 17 | Major | SKILL.md sent Phase 3e to Standard/Singularité/Unicité while the profile said that frame does not transpose, and never said the profile overrides | Fixed: the profile owns the frame; `recommendation-framework.md` and Template 7 are labelled `offer`-only |
| 18 | Major | Q5 and the profile disagreed on the deliverable scope: two readings, 3 or 6 deliverables | Fixed: Q5 decides, the profile describes the maximum, and the canonical keys are listed |
| 19 | Major | `maturity-synthesis` was a deliverable key nothing read, so that section could never be scored | Fixed: one canonical key `comparison-synthesis`, file name resolved by the profile |
| 20 | Major | Step 5b (multi-year freshness protocol) was gated on a sector module while describing a method, against the skill's own rule G2 | Fixed: gated on `benchmark_nature == maturity` |
| 21 | Major | The roue axes were hardcoded to four commercial values in SKILL.md while `output-schemas.md` said dimension ids | Fixed: dimension ids, per the schema |
| 22 | Major | The validator demanded `market_position` (a car-rental field) and `target` (B2B/B2C) from a maturity benchmark | Fixed: both conditional on the `offer` nature |
| 23 | Major | Structural PASS at 100% read as "deliverable complete" while the central metric was empty and 2 captures of 3 had failed | Fixed: the validator prints a substance block (share of rows carrying a value, metrics absent for every actor, usable screenshots) and Phase 4 must read it |
| 24 | Minor | `SKILL.md` pointed to `output-schemas.md` for Template 5, which contains no template | Fixed |
| 25 | Minor | `capture-spec.md` and the actor prompt referenced a "Step 2.6" that no longer exists | Fixed |
| 26 | Minor | An expired TLS certificate was labelled `failed`, so the retry pass burned attempts on something structural. Crawl4AI reads such a page, Playwright refuses it | Fixed: navigation errors are classified from `consent.json`, `cert-expired` is `blocked` |
| 27 | Minor | Duplicate metric names in `comparability.metrics` made every row citing them ambiguous, with nothing to catch it | Fixed: FAIL on duplicates |
| 28 | Minor | A search-engine snippet had no defined status: rule S1 mandates search, rule S4 disqualifies unfetched URLs. Agent A dropped the benchmark's central price rather than publish it | Fixed: a snippet is a lead, recorded with `confidence: interpreted` and no `source_ref`, never `observed`, never discarded |
| 29 | Minor | Repeated scrape failure on one domain had no rule, so it read as "the actor publishes nothing" | Fixed: thin-content signal in the scraper plus a systemic-failure rule in `data-sources.md` |
| 30 | Minor | Files from an earlier attempt survived a status change to blocked, giving an orphan PNG with a valid hash | Fixed: orphans are removed when a target ends blocked |

### Verification after fixes

- The exact page that broke agent A now returns its content with an explicit `thin-content` marker instead of an empty error; the rich page of the same site keeps its 24 content lines.
- A partial retry no longer erases the manifest: the successful capture survives, verified on a two-target plan.
- The stale screenshot copy of run 1 is now caught by the validator as a FAIL naming the manifest as authoritative.
- The substance block reports "metric 'price' is absent for every actor" on a benchmark that passes structurally.
- Coherence sweep green: syntax, JSON, no control characters, every prompt variable documented, zero sector hardcode in the prompt and in SKILL.md, all pointers resolve, all cross-file step references valid.

### Still owed

1. Criteria 1 and 2 of the creator's eval are now covered by agents A and B. What is not covered: the parallel subagent dispatch, the outline agent and the quality evaluator, which all three runs substituted with inline work.
2. SKILL.md grew from 5 553 to 6 113 words. The Phase 0 extraction is overdue.
3. `dimension-library.md` still offers only offer-shaped dimensions: a `maturity` mission on any sector other than sustainability has no dimension source.
