# Profile: `generic`

Fallback nature. Use when the subject fits neither `offer` nor `maturity`, and do not force it into one of them.

Being explicit about running generic is the point: the consultant sees that the skill is comparing without a specialised frame, and the scorecard scores only what applies.

## 1. Dimension sub-fields

```text
- `description` — what the actor does on this dimension, factually
- `evidence` — the sourced elements supporting the description (figures, quotes, published documents)
- `implication` — what it means competitively, one opinionated sentence
```

Three sub-fields, not four: without a known nature, a fourth field invites padding.

## 2. Deliverable set (Phase 3)

This table is the **maximum** for this nature, not an obligation. Q5 decides what the mission actually produces: an entry absent from `deliverables` is neither produced nor scored. "Applies" below means "belongs to this nature when ordered".

| Section | `deliverables` key | Applies | File written |
|---------|--------------------|---------|--------------|
| Comparison synthesis | `comparison-synthesis` | Only if `comparability.metrics` is declared | `comparison-synthesis.md` |
| Target population | `targets-analysis` | Only if the consultant asks | `targets-analysis.md` |
| Executive summary | `exec-summary` | Yes | `exec-summary.md` |
| Market landscape | `market-landscape` | Yes | `market-landscape.md` |
| Recommendation | `recommendation` | Yes, reframed (section 4) | `recommendation.md` |

## 3. Comparable metric families

Free. The mission declares them in `comparability.metrics`, each with a name, a unit and a scope. A metric with no declared unit does not go into `comparables[]`: it goes in prose.

## 4. Recommendation frame

- **STANDARD** — what the panel does uniformly
- **ÉCART** — where the client differs, in either direction, evidence attached
- **LEVIER** — the one move the benchmark supports, with what would have to be true for it to work

## 5. Scorecard sector sections

None. Score on core sections only (plus HTML if in deliverables), and state in the scorecard header that the mission ran on the generic profile.

Do not invent sector sections at run time. If two sections would genuinely fit, that is the signal to write a real profile.

## 6. Capture intents

Priority order: `home`, `offer`, `proof`.

## 7. Actor schema blocks

None of the commercial blocks. `comparables[]` plus the core actor fields carry everything.

## 8. When to promote this into a real profile

After the second mission of the same kind. Write `references/profiles/<nature>.md` following this file's structure, add the detection row in SKILL.md Phase 0, the sub-fields in `scripts/validate_benchmark.py`, and an eval. That is rule G2.

## 9. Structured blocks (injected into the actor prompt as `{nature_structured_fields}`)

None. Without a known method there is no justified structure beyond `comparables[]`.

If a mission on this profile keeps wanting the same table twice, that is the signal to write a real profile (section 8).
