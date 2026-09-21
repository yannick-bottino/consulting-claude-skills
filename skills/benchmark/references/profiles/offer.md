# Profile: `offer`

Nature of comparison: commercial offers competing for the same buyer. Compares what each actor sells, to whom, on what terms, at what price.

Formerly `benchmark_type: commercial`. That value is still read as an alias.

## 1. Dimension sub-fields

Injected into `{dimension_sub_fields}` in the actor research prompt. Every configured dimension must carry all four:

```text
- `description` — what the actor offers for this dimension
- `content` — what is included (specifics, details)
- `targets_tov` — who it is for and how they communicate about it
- `pricing` — price points, conditions, transparency
```

## 2. Deliverable set (Phase 3)

This table is the **maximum** for this nature, not an obligation. Q5 decides what the mission actually produces: an entry absent from `deliverables` is neither produced nor scored. "Applies" below means "belongs to this nature when ordered".

| Section | `deliverables` key | Applies | File written |
|---------|--------------------|---------|--------------|
| Comparison synthesis | `comparison-synthesis` | Yes, on price | `pricing-synthesis.md` |
| Target population | `targets-analysis` | If in scope | `targets-analysis.md` |
| Executive summary | `exec-summary` | Yes | `exec-summary.md` |
| Market landscape | `market-landscape` | Yes | `market-landscape.md` |
| Recommendation | `recommendation` | Yes | `recommendation.md` |

The key is what `deliverables`, the validator and the scorecard read. The file name is what the nature calls it. Never invent a key: a key nothing reads means a section nothing scores.

## 3. Comparable metric families

What goes into `comparables[]` (see `references/output-schemas.md`):

| `metric` | Typical unit | Notes |
|----------|--------------|-------|
| `price` | currency per period | One row per variant x period. The backbone of this nature |
| `fee` | currency, one-off or recurring | Setup, delivery, excess usage, penalties |
| `included_volume` | usage unit | Kilometres, seats, credits, GB, hours |
| `inclusion` | boolean | Insurance, maintenance, support level, warranty |
| `commitment` | duration | Minimum term, notice period |
| `transparency` | 1 to 3 | 1 quote only, 2 indicative published, 3 full simulator online |

## 4. Recommendation frame

`references/recommendation-framework.md`: STANDARD (table stakes present in most of the panel), SINGULARITÉ (advantage on shared ground, name the rival), UNICITÉ (segments others structurally cannot serve).

## 5. Scorecard sector sections

**S1. Pricing coverage (/10)** — cells of the comparison table (actors x periods) holding either a sourced price or a reasoned missing-data marker. Score = 10 x (qualifying cells / total cells). A bare `[N/D]` does not qualify.

**S2. Offer catalog coverage (/10)** — per actor, 1 point if the offer catalog holds at least one priced line with a source. Score = 10 x (passing actors / total actors).

## 6. Capture intents

Priority order for `capture_targets`: `pricing`, `offer`, `funnel_step`, `home`.

The pricing shot is the one that matters. Prefer a selector on the price table or the simulator result over a full page.

## 7. Actor schema blocks

Uses `vehicle_catalog` (offer catalog, name kept for v2 compatibility), `comparison_table`, `optional_services`, and the `pricing_matrix` projection at benchmark level.

## 8. Structured blocks (injected into the actor prompt as `{nature_structured_fields}`)

Three blocks, all of them projections of `comparables[]`, collected as structure because a table reads better than prose in a deliverable. Reference product, periods and units come from `comparability`, never from a sector example.

**Offer catalog** (`projections.catalog`, legacy key `vehicle_catalog`)
1. Go to the pricing or product-selection page already scraped in Step 2
2. Identify the actor's own product tiers or categories, in the actor's own words
3. Per tier: example products, the price for each period declared in `comparability.periods`, and the included volume when the market has one
4. Priority: the tier matching `comparability.reference_product`. That is the mission's reference, and it is the only cell that must be comparable across the whole panel
5. If a configurator exists, run it once on the reference product and the shortest period, and note the exact result
6. A price not displayed publicly gets a reasoned marker, never a blank
7. One entry per tier

**Published comparison table** (`projections.comparison`)
Some actors publish their own comparison against alternatives. When one exists, extract it as a boolean matrix whose criteria are the actor's, not yours, and record the criteria labels verbatim. If none exists after 2 attempts, set the note to a reasoned marker and move on.

**Optional services** (`projections.options`)
Paid add-ons and their price format (`inclus`, per period, one-off, on request, or a reasoned marker). Collect what the actor lists; do not go looking for services the market does not have.
