# Evaluation Rubric

How to prove the skill's output quality instead of asserting it. Self-graded "outperforms X" labels are marketing — discount them. Quality is shown by scoring real reports against a fixed rubric, ideally head-to-head with a provider deep-research product on the same queries.

This rubric scores the ARTIFACT (the report). It is separate from triggering accuracy (whether the skill activates at the right time), which `skill-creator`'s `run_loop.py` optimizes via the description field. Do not conflate the two.

## The 6 dimensions (score each 0.0–1.0)

| # | Dimension | What it measures | How to score |
|---|-----------|------------------|--------------|
| 1 | **Factual accuracy** | Do claims match what the cited sources actually say? | Spot-check 10 claims against their sources. score = correct / 10 |
| 2 | **Citation accuracy** | Does each cited source genuinely support its claim? (the biggest differentiator) | Of the 10, how many citations actually back the claim. score = supported / 10 |
| 3 | **Coverage / completeness** | Are all facets of the question addressed? | Did the original sub-questions all get answered? Penalize unflagged gaps. |
| 4 | **Source quality** | Primary / authoritative vs SEO content farms | Share of official+academic sources; penalize over-reliance on aggregators. |
| 5 | **Reasoning depth / insight** | Genuine synthesis + contradiction handling vs a list of facts | Are conflicts surfaced and adjudicated? Is there cross-source synthesis? |
| 6 | **Tool efficiency** | Query count + pages read vs result quality | Did it spend appropriately for the tier, or over/under-search? |

Report score = mean of the six. Track dimensions 1 and 2 separately too — they are the ones users notice when a report is subtly wrong.

## How to run an evaluation

1. Fix a set of 15–20 representative queries (your real consulting topics: market scans, competitive landscapes, reg briefs).
2. Run this skill on each. If comparing, run a provider deep-research product on the same queries.
3. Score each report on the six dimensions. Use an LLM-as-judge pass for a first cut (one call emitting per-dimension scores + a pass/fail is more consistent than multiple judges), THEN read ~10 reports yourself — humans catch hallucinations and source bias a judge misses.
4. Start small: large effects (e.g. fixing the loop) show up on ~20 queries. You do not need hundreds.

## Thresholds that should change your priorities

- **Citation accuracy < 0.8** → fix the verifier (P6/P7) before anything else. A confident report with wrong citations is worse than a hedged one.
- **Coverage lagging a provider by a wide margin** → the loop is not searching broadly/deeply enough. Raise query ceiling and subagents/round for the tier.
- **Losing only on polish/readability** → it is a synthesis-prompt/template fix, not an architecture problem. Cheap to fix.
- **Tool efficiency low + quality high** → you are over-spending; tighten ceilings. Quality high + efficiency high → ship it.

## benchmark.json (for skill-creator's eval-viewer)

When iterating with `skill-creator`, encode the query set as assertions so `generate_review.py` can render outputs for human review. Keep assertions about STRUCTURE and TRACEABILITY (objectively checkable), not about subjective prose quality:

```json
{
  "eval_cases": [
    {
      "prompt": "Competitive landscape of the EU carbon accounting software market, 2026",
      "assertions": [
        "Report cites at least 12 sources with a references section",
        "Every numeric claim has a citation marker",
        "At least 30% of approved sources are official or academic",
        "A Key Controversies / contradictions section is present",
        "Residual gaps are stated explicitly if any sub-question is unanswered",
        "Each major section carries a confidence marker (High/Medium/Low)"
      ]
    }
  ]
}
```

These assertions check the skill's discipline (citations, governance, gap-honesty), which is automatable. The six-dimension judgement above stays human-in-the-loop.
