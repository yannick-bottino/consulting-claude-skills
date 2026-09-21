# Benchmark Quality Scorecard (Phase 6)

Operational reference. Read by the orchestrator after Phase 5 to produce `outputs/{mission-slug}/benchmark-scorecard.md`.

## Contents
1. Applicability model
2. Core sections (always scored)
3. Conditional section (HTML)
4. Sector sections by profile
5. Output template (Template 8)
6. Handoff to Phase 7

---

## 1. Applicability model

A scorecard is never scored out of a fixed total. Build the denominator from the sections that apply to this mission.

| Block | Count | Applies when |
|-------|-------|--------------|
| Core, always applicable | 4 | C1 completeness, C2 à retenir, C3 insights, C4 sourcing integrity |
| C5 market landscape | 1 | `market-landscape` is in `deliverables` |
| S1 sector section | see 4 | The comparison synthesis is ordered (`comparison-synthesis`) |
| C6 recommendation | 1 | `recommendation` is in `deliverables` |
| H1 HTML report | 1 | `html-report` is in `deliverables` |
| Sector | 2 | The mission's `benchmark_nature` profile defines them (section 4) |

Only C1 to C4 are unconditional: they measure the quality of what the mission produced whatever it produced. Every other section maps to a deliverable the consultant can legitimately not order, and scoring a mission on a deliverable it never asked for is the same defect as a fixed denominator.

Each section is scored out of 10.

```
applicable_total = 10 x (number of applicable sections)
score_pct        = round(100 x sum_of_scores / applicable_total)
```

Rules:
- Never score a non-applicable section 0. Write `N/A` in the score column and exclude it from `applicable_total`.
- A nature with no sector sections (`generic`) scores on core, plus HTML if in scope. Do not invent sector sections at run time.
- Report `benchmark_nature`, `sector`, the applicable section list, and `applicable_total` in the scorecard header. Phase 7 thresholds read `score_pct`, never the raw total.
- Score what the deliverable contains, not what exists on disk. A file that exists but is empty scores 0 on its section.

---

## 2. Core sections (always scored)

### C1. Actor data completeness (/10)
Required fields = the schema required fields in `references/output-schemas.md` plus the sub-fields block of the mission's profile (`references/profiles/<nature>.md` section 1).

Score = 10 x (actors with every required field populated / total actors).

A field holding only a missing-data marker counts as populated only if the marker carries a reason, per Step 5 of `references/data-sources.md` (example: `[N/D — offre uniquement sur devis B2B]` passes, a bare `[N/D]` does not).

### C2. "À retenir" quality (/10)
Per actor, 1 point if all three hold: one sentence, 30 words or fewer, and it states a competitive judgment rather than summarising data. Score = 10 x (passing actors / total actors).

### C3. Insights quality (/10)
Per actor, 1 point if there are at least 2 positive insights and at least 1 negative, each carrying an explanation clause and each traceable to a populated field or source in the actor JSON. Score = 10 x (passing actors / total actors).

### C4. Sourcing integrity (/10)
Take every quantitative claim and every third-party attribution across the actor files.

Score = 10 x (claims carrying a source reference, plus a verbatim where rule D3 requires one / total claims).

A screenshot with an `ok` entry in `capture-manifest.json` counts as a source for the figure it displays: the capture is dated, URL-stamped and hashed, which is what a verbatim provides (see `references/capture-spec.md` section 7).

Hard fail: if any figure has no traceable origin at all, score this section 0 and flag it as a blocking gap regardless of the other sections. A fabricated figure is not a gap to iterate on, it is a defect to remove.

### C5. Market landscape (/10) — only if `market-landscape` is in deliverables
2 points each:
- every actor is placed on the segment axis defined in mission-config;
- every actor is placed in a category;
- each included actor has a one-line inclusion rationale;
- excluded actors are listed with a concrete reason (not "hors scope");
- no row or column of the matrix is left empty without a stated reason.

### C6. Recommendation (/10) — only if `recommendation` is in deliverables
2 points each:
- every STANDARD item carries the actor count that justifies it;
- every SINGULARITÉ item names the rival competitor on the same terrain;
- every UNICITÉ segment names a structural barrier, not a preference or a price gap;
- every claim traces to a produced file (`pricing-synthesis.md`, `targets-analysis.md`, `actors/*.json`);
- no generic strategy advice: each item cites an actor, a figure, or a named segment.

---

## 3. Conditional section (HTML)

### H1. HTML report (/10) — only if `html-report` is in deliverables
2 points each:
- opens in a browser with no console error;
- every section whose source data exists in `benchmark.json` renders that data;
- every section whose source data is absent is hidden, not rendered empty;
- no placeholder frame, no lorem, no empty visual block;
- every figure displayed exists in `benchmark.json` (nothing computed only inside the HTML).

---

## 4. Sector sections by profile

Two sections per nature, defined in `references/profiles/<nature>.md` section 5. Read the mission's profile and score its two sections here.

| `benchmark_nature` | S1 | S2 |
|---|---|---|
| `offer` | Pricing coverage | Offer catalog coverage |
| `maturity` | Quantified metrics coverage | Certifications and commitments verification |
| `generic` | none | none |

`generic` scores on core sections only, and the scorecard header says so. Never invent sector sections at run time: if two would genuinely fit, that is the signal to write a real profile (rule G2).

---

## 5. Output template (Template 8)

Save to `outputs/{mission-slug}/benchmark-scorecard.md`.

```markdown
# Benchmark Quality Scorecard — [Mission] — [Date]

**Nature :** [benchmark_nature] · **Secteur :** [sector] · **Sections applicables :** [N] · **Total applicable :** [N0]

| Section | Score | Max | Notes |
|---------|-------|-----|-------|
| C1 Actor data completeness | X | 10 | [observation chiffrée] |
| C2 À retenir quality | X | 10 | [acteurs en échec, raison] |
| C3 Insights quality | X | 10 | [observation] |
| C4 Sourcing integrity | X | 10 | [claims sans source] |
| C5 Market landscape | X ou N/A | 10 | [N/A si hors deliverables] |
| C6 Recommendation | X ou N/A | 10 | [N/A si hors deliverables] |
| H1 HTML report | X ou N/A | 10 | [N/A si hors deliverables] |
| S1 [libellé du profil] | X ou N/A | 10 | [observation] |
| S2 [libellé du profil] | X ou N/A | 10 | [observation] |
| **TOTAL** | **XX** | **[N0]** | **[XX]%** |

## Gaps classés

| # | Section | Gap | Type | Action |
|---|---------|-----|------|--------|
| 1 | [section] | [gap précis] | corrigeable / structurel | [action ciblée] |

## Comparaison avec l'itération précédente

*(Si un scorecard précédent existe, le lire et comparer en pourcentage, pas en points bruts : le dénominateur peut différer.)*
- Itération précédente : [XX]% ([XX]/[N0])
- Cette itération : [XX]% ([XX]/[N0])
- Delta : [+/-XX] points de pourcentage
```

---

## 6. Handoff to Phase 7

`score_pct` and the classified gap table are the only inputs Phase 7 needs. Do not restate corrective actions here: `references/iteration-loop.md` owns the correction protocol.
