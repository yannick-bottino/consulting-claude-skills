# Iteration Loop (Phase 7)

Operational reference. Read by the orchestrator after the scorecard is written. A benchmark is not delivered in one pass: Phase 6 measures, Phase 7 corrects, then re-scores.

## Contents
1. Decide whether to iterate
2. Classify the gaps
3. Targeted corrections by gap type
4. Regenerate deliverables
5. Re-validate and re-score
6. Convergence decision
7. Final delivery summary

---

## 1. Decide whether to iterate

Read `score_pct` from `outputs/{mission-slug}/benchmark-scorecard.md`. Thresholds are percentages of the applicable total, never raw points: the denominator varies with `benchmark_nature` and deliverable scope (see `references/scorecard.md` section 1).

| score_pct | Action |
|-----------|--------|
| >= 90% | STOP. Deliverable. Go to section 7 |
| 75% to 89% | Iterate on the top 3 gaps |
| < 75% | Iterate, and tell the consultant which limits are structural |

A section scored 0 by hard fail (C4 sourcing integrity, or S2 for `maturity`) forces an iteration whatever the total: correct it before anything else.

If the consultant asked for an iteration explicitly, iterate regardless of the score.

Hard limit: 3 iterations total. Past that, tell the consultant and deliver as is.

---

## 2. Classify the gaps

For each gap in the scorecard gap table, assign one class:

- **Corrigeable**: the data exists but is unexploited, mis-formatted, or the text needs rewriting.
- **Structurel**: the data is not public (quote-only B2B offers, opaque actor, unpublished indicator). Document it, stop scoring it as a gap.

Correct only the corrigeable gaps. Re-listing a structural gap at every iteration burns iterations without moving the score.

Take the top 3 corrigeable gaps by score impact (lowest scoring section first).

---

## 3. Targeted corrections by gap type

### C2 "À retenir" quality
Re-read the actor JSON (dimensions, insights, catalog). Rewrite `a_retenir` as one sentence, 30 words or fewer, stating a competitive judgment. Update both the actor JSON and the actor Markdown file.

### C3 Insights quality
Re-run a targeted search on the actor, then complete the JSON and the Markdown. Re-validate with `validate_benchmark.py`.

### C4 Sourcing integrity
For each unsourced claim: find the source, or downgrade the claim. A quantitative claim with no source is removed or marked per Step 5 of `references/data-sources.md`. Never keep an unsourced figure in a deliverable to protect a score.

### C5 Market landscape
Re-read `market_position` and `category` across actor JSONs. Fill the missing placements. Write the inclusion rationale and the exclusion reasons, one line each.

### C6 Recommendation
Re-read `pricing-synthesis.md`, `targets-analysis.md`, and the actor JSONs, then attach the missing evidence: actor count for STANDARD, rival name for SINGULARITÉ, structural barrier for UNICITÉ.

### H1 HTML report
Check that the source data exists in `benchmark.json` first. A missing HTML section caused by missing data is a data gap, not an HTML gap: fix the data. Then regenerate the section per `references/html-report-spec.md`.

### Sector sections (S1, S2)
Run targeted searches built from the mission vocabulary, not from a hardcoded sector. Template:

```
WebSearch: "[actor]" [metric or offer term from the dimension label] [year]
WebSearch: "[actor]" [official term used by the sector for this indicator] [geography]
```

For `offer`, the metric term comes from the pricing dimension and the reference unit in mission-config (reference product, period, volume). For `maturity`, it comes from the indicator names in the sector search module.

If the value stays unreachable after 2 attempts, mark it with a reasoned marker and reclassify the gap as structural.

### Screenshots not captured
Try the capture path once. If the tool is unavailable, record it as structural and stop penalising it.

---

## 4. Regenerate deliverables

Regenerate in this order. Dependencies flow downward.

1. Actor JSONs (already corrected in section 3)
2. `pricing-synthesis.md`, or the sector-equivalent synthesis, only if an actor value changed
3. `exec-summary.md`, only if insights or positioning changed
4. `recommendation.md`, only if pricing or targets changed
5. `benchmark.json`, always (full reassembly from the actor JSONs)
6. `benchmark-report.html`, always, if `html-report` is in deliverables

Do not regenerate a synthesis file when no source data under it changed. Check before rewriting.

---

## 5. Re-validate and re-score

```bash
python {skill_path}/scripts/validate_benchmark.py benchmark "outputs/{mission-slug}/benchmark.json"
```

Then rebuild the scorecard with `references/scorecard.md`, including the "Comparaison avec l'itération précédente" block. Compare percentages, not raw points: the denominator can differ between iterations if the deliverable scope changed.

---

## 6. Convergence decision

| Condition | Action |
|-----------|--------|
| score_pct >= 90% | Converged. Go to section 7 |
| Improved, < 90%, all remaining gaps structural | Converged. Document the limits, go to section 7 |
| Improved, < 90%, corrigeable gaps remain | Next iteration, back to section 2 (3 iterations maximum) |
| Not improved after an iteration | Stop. Tell the consultant the remaining gaps are structural |

---

## 7. Final delivery summary

> "Benchmark livré après {N} itérations.
>
> **Score final :** {XX}% ({XX}/{total applicable}, nature {benchmark_nature})
>
> | # | Score | Delta | Corrections |
> |---|-------|-------|-------------|
> | 1 | {XX}% | — | Run initiale |
> | 2 | {XX}% | +{XX} pts | [corrections appliquées] |
>
> **Livrables dans `outputs/{mission-slug}/` :**
> - {liste des fichiers}
>
> **Gaps structurels non résolus :**
> - {liste avec raisons}
>
> Ces fichiers sont prêts pour la production PPT via le skill dédié."
