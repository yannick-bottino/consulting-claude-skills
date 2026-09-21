---
type: check
layer: 1-universal
status: active
source: the fact-checker skill. Embedded here, not referenced.
---

# Check: factual accuracy

Verify claims systematically, against the world, using evidence. This is world-truth. Whether a claim matches the company's own numbers and offers is a different check (Company fit). Flag and suggest, do not rewrite on your own.

## Process

1. Identify the claim. Extract each specific factual assertion. Separate fact from opinion. Note implicit claims and anything measurable.
2. Determine required evidence. What would prove it, what would disprove it, what source would be authoritative. Decide if it is verifiable at all or is opinion.
3. Evaluate the evidence. Check authoritative sources, prefer primary data, weigh source credibility, note dates, check context. Use the web where you can.
4. Rate the claim (scale below).
5. Provide the correct version if the claim is wrong, and any missing context.

## Rating scale

- TRUE: accurate, supported by reliable evidence.
- MOSTLY TRUE: accurate but missing important context or a minor detail is off.
- MIXED: contains both true and false elements.
- MOSTLY FALSE: misleading or largely inaccurate.
- FALSE: demonstrably wrong.
- UNVERIFIABLE: cannot be confirmed or denied with available evidence. Do not pass an unverifiable claim as true, flag it.

## Source quality, high to low

1. Peer-reviewed studies.
2. Official government or primary statistics.
3. Reputable, fact-checked news organizations.
4. Qualified expert statements in the field.
5. General news sites (verify with a second source).
6. Social media and blogs (lowest, verify independently).

## Patterns to watch

- Statistical manipulation: cherry-picked data, misleading scales, correlation stated as causation, inappropriate comparisons.
- Context removal: quote mining, dropped qualifiers, ignored timeframes, removed caveats.
- False equivalence: comparing incomparable things, treating all sources as equal.
- Invented precision: a confident statistic ("83% of teams...") with no source.
- Wrong claims about what a tool, model, law, or product actually does.

## What a finding looks like

Quote the claim, give the rating and the one-line reason, and give the corrected version as the fix. For example:

```
Factual accuracy · blocker
  Quote:  "Claude Code can run fully autonomously for a week with no human input."
  Breaks: factual-accuracy.md, UNVERIFIABLE / overstated, no source supports this
  Fix:    "Claude Code can run long multi-step tasks, but still checks in for approvals."
```

## Grading

- Aligned: every checkable claim is TRUE or MOSTLY TRUE.
- Drift: a MOSTLY TRUE claim missing context, or an UNVERIFIABLE claim that should be softened or sourced.
- Misaligned: any FALSE or MOSTLY FALSE claim, or invented statistics, in something about to ship.
