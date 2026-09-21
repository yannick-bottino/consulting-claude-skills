# Profile: `maturity`

Nature of comparison: how advanced each actor is on a subject assessed against a grid. Sustainability and ESG, data and AI, cyber, accessibility, digital maturity. Compares evidence of practice, not offers.

Formerly `benchmark_type: rse`. That value is still read as an alias, mapping to `nature: maturity` with the sustainability sector module.

The sector supplies the indicators. The nature supplies the method. Never hardcode indicator names here: they live in the sector search module.

## 1. Dimension sub-fields

Injected into `{dimension_sub_fields}` in the actor research prompt:

```text
- `maturity_level` — qualitative assessment (ad hoc / initié / structuré / leader)
- `key_metrics` — quantified KPIs with named and dated sources
- `certifications` — labels, certifications, third-party scores relevant to the dimension
- `commitments` — published targets with a timeline
```

## 2. Deliverable set (Phase 3)

This table is the **maximum** for this nature, not an obligation. Q5 decides what the mission actually produces: an entry absent from `deliverables` is neither produced nor scored. "Applies" below means "belongs to this nature when ordered".

| Section | `deliverables` key | Applies | File written |
|---------|--------------------|---------|--------------|
| Comparison synthesis | `comparison-synthesis` | Yes, on indicators | `maturity-synthesis.md` |
| Target population | `targets-analysis` | No by default | — |
| Executive summary | `exec-summary` | Yes | `exec-summary.md` |
| Market landscape | `market-landscape` | Yes, segment axis = maturity tiers | `market-landscape.md` |
| Recommendation | `recommendation` | Yes, reframed (section 4) | `recommendation.md` |

The key is what `deliverables`, the validator and the scorecard read. The file name is what the nature calls it.

`maturity-synthesis.md` replaces the pricing synthesis: same role, an actors x indicators matrix with the reference year, the unit, and the verification status of each cell.

## 3. Comparable metric families

| `metric` | Typical unit | Notes |
|----------|--------------|-------|
| `indicator` | percentage, absolute, ratio | One row per indicator x year. Year is mandatory: a maturity figure without a year is worthless |
| `certification` | status | Obtained, in progress, member, none. Never upgrade a status (rule D3) |
| `commitment` | target plus deadline | Store the published wording, not a paraphrase |
| `coverage` | percentage of scope | What share of the business the figure covers. A 100% figure on 10% of the scope is not a leader signal |
| `verification` | none, self, third-party review, third-party audit | The distinction that rule D3 exists to protect |

## 4. Recommendation frame

Standard / Singularité / Unicité does not transpose: there is no buyer to win on a maturity grid. Use instead:

- **SOCLE** — practices present across the panel, and expected by regulation or by the market. What the client must have, not what differentiates.
- **ÉCART** — where the client trails the panel, quantified against a named actor and a named indicator. One line per gap, with the distance.
- **TERRAIN D'AVANCE** — dimensions where the panel is weak or silent and where the client can credibly lead, with the proof it would need to publish to make the claim defensible.

Every item names an actor, an indicator and a year. Generic maturity advice is worth nothing.

## 5. Scorecard sector sections

**S1. Quantified metrics coverage (/10)** — per actor, 1 point if `key_metrics` holds at least 2 quantified indicators, each with a named and dated source. Score = 10 x (passing actors / total actors).

**S2. Certifications and commitments verification (/10)** — every certification, label, score and third-party attribution carries a verbatim and passes the Layer 2 escalation check of `references/methodology.md`. Score = 10 x (compliant claims / total claims).

Score 0 for S2 if any claim conflates a methodology review with a data audit (Layer 3). That error is what this nature exists to prevent.

## 6. Capture intents

Priority order: `proof`, `home`, `offer`.

The `proof` shot is the point: the page showing the certification, the published report, the dated commitment. Prefer a selector on the badge or the figure. A capture is often the only durable trace, since sustainability pages are rewritten frequently.

## 7. Actor schema blocks

None of the commercial blocks apply: no `vehicle_catalog`, no `comparison_table`, no `optional_services`, no `pricing_matrix`. The validator and the scorecard exclude them for this nature.

## 8. Structured blocks (injected into the actor prompt as `{nature_structured_fields}`)

None. A maturity assessment has no catalog, no comparison table and no optional services.

`comparables[]` carries every indicator, certification, commitment, coverage and verification-level row, with its year. Producing an empty projection block here would be noise, and filling one would be fabrication.

The single structured requirement specific to this nature: **every indicator row carries its year**, and a figure whose year cannot be established is recorded with `confidence: interpreted` and the reason in `note`.
