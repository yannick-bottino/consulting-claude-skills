# Benchmark — Output JSON Schema

## File Structure Per Mission

Each benchmark mission produces the following files in `outputs/[mission-slug]/`:

```
outputs/
└── [mission-slug]/                      ← e.g., "lmd-france-velora" or "assurance-emprunteur-ca"
    ├── mission-config.json              ← Phase 0 output: mission parameters
    ├── research-outline.json            ← Phase 1.05 output: pre-populated actor data (NEW)
    ├── research-brief.md                ← Phase 1.05 output: brief injected into subagents
    ├── benchmark.json                   ← Phase 4 output: full structured data (feeds PPT skill)
    ├── exec-summary.md                  ← Phase 3c output
    ├── pricing-synthesis.md             ← Phase 3a output
    ├── targets-analysis.md              ← Phase 3b output
    ├── market-landscape.md              ← Phase 3d output (NEW)
    ├── recommendation.md                ← Phase 3e output (NEW)
    ├── benchmark-report.html            ← Phase 5 output
    ├── benchmark-scorecard.md           ← Phase 6 output
    ├── capture-plan.json                ← Step 1.4 input: merged capture targets
    └── actors/
        ├── [actor-slug].json            ← Phase 2 output: per-actor structured data
        ├── [actor-slug].md              ← Phase 2 output: per-actor Markdown
        └── screenshots/                 ← Step 1.4 output
            ├── capture-manifest.json    ← source of truth for what was captured
            ├── [slug]-[intent].png      ← original, full resolution, for decks
            └── [slug]-[intent].web.jpg  ← captioned derivative, inlined in the HTML
```

**Mission slug format:** `[market-keyword]-[client-slug]`
Examples: `lmd-france-velora`, `assurance-emprunteur-banque-solaris`, `telco-b2b-kaptel`

---

## benchmark.json — Full Schema

**Naming rule for projections.** The JSON key is stable forever, the human label is mission data. `projections.catalog` is the key whatever the market; its `label` is resolved in cascade: the nature profile gives a default, the sector search module may override it, and `comparability.reference_product` is the last resort. That is what lets a downstream consumer target one path on any sector, while a textile deliverable reads "Mix matières par fibre" and a mobility one reads "Véhicules & pricing". Nothing in the code ever knows the word "vehicle".

```json
"projections": {
  "catalog":    { "label": "resolved per mission", "rows": [] },
  "comparison": { "label": "resolved per mission", "criteria": [], "rows": [] },
  "options":    { "label": "resolved per mission", "rows": [] }
}
```

Legacy keys `vehicle_catalog`, `comparison_table` and `optional_services` are still read, and still written for the `offer` nature so existing consumers keep working. New code targets `projections`.

**Source of truth from v3: `comparables[]`.** Every comparable figure lives there, in long format, whatever the benchmark nature. It is what makes the skill work on a subject nobody anticipated: a new metric is a new row, not a new schema block.

These blocks are **projections** of `comparables[]`, generated for the `offer` nature only, and kept so existing downstream consumers (PPT generation, v2 readers) keep working:

- `actors[].vehicle_catalog`, `actors[].comparison_table`, `actors[].optional_services`
- `pricing_matrix`
- `recommendation.pricing_chart`

Rules for projections: never edit a projection by hand, regenerate it from `comparables[]`. A value present in a projection and absent from `comparables[]` is a defect. Other natures omit the projections entirely, and they are excluded from scoring (see `references/scorecard.md`).

A v2 file with no `comparables[]` stays valid: the validator reads it in legacy mode.

```json
{
  "schema_version": "3.0",
  "benchmark_nature": "string — offer | maturity | generic",
  "sector": "string — the market domain, free text",
  "locale": {
    "output_language": "string — ISO 639-1, language every deliverable is written in (default fr)",
    "country": "string — ISO 3166-1 alpha-2, drives the statistical office in public-statistics.md",
    "currency": "string — ISO 4217, drives price formatting and the comparability contract",
    "statistical_office": "string | null — resolved office name, for citation"
  },
  "mission": {
    "name": "string — human-readable mission name",
    "slug": "string — kebab-case, used as folder name",
    "client": "string",
    "market": "string — market description",
    "date": "YYYY-MM-DD — analysis date",
    "consultant": "string | null"
  },
  "scope": {
    "actors": ["string — actor names"],
    "actor_categories": {
      "[category name]": ["actor names in this category"]
    },
    "segment_axis": {
      "id": "string — axis identifier",
      "label": "string — axis label for the landscape map",
      "segments": [{ "id": "string", "label": "string" }],
      "focus": "string — segment id the mission focuses on"
    },
    "geographies": ["string"],
    "reference_product": "string | null — reference offer used for comparability",
    "reference_unit": "string | null — volume or usage unit of the comparison",
    "durations": ["string — e.g., '1m', '3m', '6m', '12m'"]
  },
  "comparability": {
    "_comment": "What makes two actors comparable. Mandatory from v3. Two values that do not share this contract must never sit in the same column.",
    "reference_product": "string | null — the offer, profile, or scope being compared",
    "currency": "string | null — ISO code, e.g. EUR, USD, GBP",
    "periods": ["string — comparison periods, e.g. '1m', '12m', '2025'"],
    "scope": "string — tax basis, volume, geography, anything that changes the figure",
    "metrics": [
      {
        "name": "string — metric id used in comparables[].metric",
        "unit": "string — e.g. EUR/mois, %, tCO2e, seats",
        "scope": "string | null — overrides the global scope for this metric"
      }
    ],
    "notes": "string | null — known non-comparabilities left in the data"
  },
  "comparables": [
    {
      "_comment": "Long format. One row per observation. Replaces per-nature blocks: the same table holds prices by period, indicators by year, tiers by seat count.",
      "id": "string — stable id, referenced by screenshots and recommendations",
      "actor": "string — must match scope.actors",
      "variant": "string | null — product line, profile, tier, fiber, whatever varies inside an actor",
      "metric": "string — must match a comparability.metrics[].name",
      "period": "string | null — '1m', '12m', '2025'",
      "value": "number | null — numeric value when there is one",
      "value_text": "string | null — non-numeric value: 'inclus', 'sur devis', 'B Corp'",
      "unit": "string | null — inherited from the metric when omitted",
      "scope": "string | null — overrides comparability.scope for this row",
      "confidence": "observed | estimated | interpreted | absent",
      "source_ref": "string | null — id or description of the source in actors[].sources",
      "captured_at": "YYYY-MM-DD | null",
      "note": "string | null — the reason, when confidence is estimated or absent"
    }
  ],
  "dimensions": [
    {
      "id": "string — kebab-case identifier",
      "label": "string — display label",
      "description": "string — what this dimension covers"
    }
  ],
  "actors": [
    {
      "id": "string — kebab-case slug",
      "name": "string — official name",
      "category": "string — must match a key in scope.actor_categories",
      "target": "B2B | B2C | B2B+B2C",
      "tagline": "string | null",
      "quote": "string | null — large display quote from official site/marketing (e.g. «Plus de flexibilité pour votre mobilité»). [N/D] if not found.",
      "market_position": {
        "duration_segment": "string — segment id from scope.segment_axis, or 'multi' when the actor spans several",
        "b2b_b2c": "B2B | B2C | B2B+B2C"
      },
      "key_figures": "string | null — sourced summary",
      "vehicle_catalog": [
        {
          "category": "string — vehicle category name (e.g. VP - Économique, SUV Compact, Utilitaire)",
          "examples": ["string — example model names"],
          "price_1m": "string | null — e.g. '419€' or '[N/D]'",
          "price_3m": "string | null",
          "price_6m": "string | null",
          "price_12m": "string | null",
          "km_included": "string | null — e.g. '500km/mois'",
          "source": "string | null — URL or document reference"
        }
      ],
      "comparison_table": {
        "note": "string — '[N/D — non publié par cet acteur]' if not available",
        "vs_achat": {
          "engagement_long_terme": "boolean | null",
          "assurance_incluse": "boolean | null",
          "entretien_inclus": "boolean | null",
          "flexibilite_duree": "boolean | null",
          "vehicule_recent": "boolean | null"
        },
        "vs_lcd": {
          "engagement_long_terme": "boolean | null",
          "assurance_incluse": "boolean | null",
          "entretien_inclus": "boolean | null",
          "flexibilite_duree": "boolean | null",
          "vehicule_recent": "boolean | null"
        },
        "vs_lld": {
          "engagement_long_terme": "boolean | null",
          "assurance_incluse": "boolean | null",
          "entretien_inclus": "boolean | null",
          "flexibilite_duree": "boolean | null",
          "vehicule_recent": "boolean | null"
        }
      },
      "optional_services": [
        {
          "name": "string — service name (e.g. Pneus hiver, Livraison/restitution, Km supplémentaires)",
          "price": "string — 'inclus' | 'X€/mois' | 'X€ forfait' | 'sur devis' | '[N/D]'"
        }
      ],
      "dimensions": {
        "[dimension_id]": {
          "_comment": "sub-fields depend on benchmark_nature — see references/profiles/<nature>.md. Below: offer",
          "description": "string — offer description",
          "content": "string — what's included",
          "targets_tov": "string — target segments and tone",
          "pricing": "string — pricing info"
        }
      },
      "a_retenir": "string — 1-sentence synthesis",
      "insights_positive": ["string — positive differentiators"],
      "insights_negative": ["string — warnings or negatives"],
      "sources": [
        {
          "description": "string — what this source supports",
          "url": "string | null",
          "document": "string | null — local file path if client doc",
          "page": "string | null",
          "retrieved_date": "YYYY-MM-DD | null"
        }
      ],
      "data_quality": {
        "has_missing_data": "boolean",
        "has_estimated_data": "boolean",
        "notes": "string | null"
      },
      "uncertain_fields": ["string — field paths marked as uncertain, e.g. 'dimensions.pricing.pricing', 'key_figures'"],
      "comparables": [
        {
          "_comment": "Rows produced by the actor subagent, same shape as the benchmark-level array. Merged into benchmark.comparables at assembly (Step 4.1), which is why an actor carrying them must not author the projection blocks by hand.",
          "id": "string — unique and stable, referenced by screenshots via comparable_ref",
          "actor": "string — this actor's name",
          "metric": "string — declared in comparability.metrics",
          "period": "string | null",
          "value": "number | null",
          "value_text": "string | null",
          "unit": "string | null",
          "scope": "string | null",
          "confidence": "observed | estimated | interpreted | absent",
          "source_ref": "string | null — entry in this actor's sources",
          "captured_at": "YYYY-MM-DD | null",
          "note": "string | null"
        }
      ],
      "capture_targets": [
        {
          "intent": "home | offer | pricing | funnel_step | proof | comparison",
          "url": "string — a URL the subagent actually visited, never a guess",
          "selector_hint": "string | null — CSS selector of the evidence block",
          "full_page": "boolean — true only when the whole page is the evidence",
          "actions": [{"click": "selector"}, {"wait_ms": 800}, {"scroll_to": "selector"}],
          "claim": "string — what this capture proves, one line",
          "comparable_ref": "string | null — id of the comparable this backs"
        }
      ],
      "screenshots": [
        {
          "intent": "string — mirrors the nominated intent",
          "url": "string",
          "status": "ok | blocked | failed | skipped",
          "blocker": "string | null — captcha | waf | login | geoblock | empty-page | error detail",
          "path": "string | null — original PNG",
          "path_web": "string | null — captioned derivative, inlined in the report",
          "sha256": "string | null",
          "captured_at": "YYYY-MM-DD | null",
          "claim": "string | null"
        }
      ]
    }
  ],
  "pricing_matrix": {
    "reference_vehicle": "string | null",
    "reference_km_per_month": "integer | null",
    "data": [
      {
        "actor": "string — actor name",
        "prices": {
          "1m": "string | null — e.g., '489€/mois'",
          "3m": "string | null",
          "6m": "string | null",
          "12m": "string | null",
          "24m": "string | null"
        },
        "km_included": "string | null",
        "conditions": "string | null — extra fees, exclusions",
        "transparency_index": "1 | 2 | 3",
        "source_url": "string | null"
      }
    ]
  },
  "key_insights": ["string — 3-5 top-level findings with data"],
  "strategic_recommendation": "string | null",
  "market_landscape": {
    "segment_axis": {
      "id": "string — mirrors scope.segment_axis.id",
      "label": "string",
      "focus": "string — segment id in focus"
    },
    "segments": {
      "[segment id from scope.segment_axis]": ["string — actor names operating in this segment"]
    },
    "categories": {
      "[category name]": ["string — actor names in this category"]
    }
  },
  "roue_concurrentielle": {
    "center_common": ["string — facts true for all actors in the benchmark"],
    "differentiators_positive": [
      {
        "actor": "string — actor name",
        "axis": "string — one of the configured dimension ids (dimensions[].id)",
        "label": "string — short differentiator label (max 10 words)"
      }
    ],
    "differentiators_negative": [
      {
        "actor": "string — actor name",
        "axis": "string — one of the configured dimension ids (dimensions[].id)",
        "label": "string — short weakness/risk label (max 10 words)"
      }
    ]
  },
  "recommendation": {
    "standard": {
      "label": "Ce que le client DOIT proposer",
      "items": ["string — table-stakes feature present in ≥80% of actors"]
    },
    "singularite": {
      "label": "Cœur de proposition du client",
      "differentiator": "string — central differentiating theme in one phrase",
      "items": ["string — specific advantage with evidence"]
    },
    "unicite": {
      "label": "Seule solution pour certaines cibles",
      "segments": [
        {
          "segment": "string — target segment name",
          "barrier": "string — why other actors cannot serve this segment",
          "why_client_wins": "string — why the client is the only viable option"
        }
      ]
    },
    "pricing_chart": [
      {
        "actor": "string — actor name",
        "price_1m": "number | null — monthly price in euros for 1-month contract",
        "price_3m": "number | null",
        "price_6m": "number | null",
        "price_12m": "number | null",
        "is_client": "boolean — true if this is the benchmarked client"
      }
    ]
  },
  "data_quality": {
    "retrieval_date": "YYYY-MM-DD",
    "actors_with_missing_data": ["string — actor names"],
    "actors_with_estimated_data": ["string — actor names"],
    "data_gaps": ["string — description of significant gaps"]
  }
}
```

---

## Markdown → JSON Field Mapping

| Markdown section | JSON path |
|-----------------|-----------|
| Actor `## [NAME]` header | `actors[].name` |
| **Catégorie :** | `actors[].category` |
| **Statut :** B2B/B2C | `actors[].target` |
| **Tagline :** | `actors[].tagline` |
| **Chiffres clés :** | `actors[].key_figures` |
| Dimension table — Description column | `actors[].dimensions.[id].description` |
| Dimension table — Contenu column | `actors[].dimensions.[id].content` |
| Dimension table — Cibles & TOV column | `actors[].dimensions.[id].targets_tov` |
| Dimension table — Pricing column | `actors[].dimensions.[id].pricing` |
| **À retenir :** | `actors[].a_retenir` |
| INSIGHTS ✅ lines | `actors[].insights_positive[]` |
| INSIGHTS ⚠️ lines | `actors[].insights_negative[]` |
| Sources block | `actors[].sources[]` |
| Pricing synthesis table rows | `pricing_matrix.data[]` |
| Executive Summary > Faits marquants | `key_insights[]` |
| Executive Summary > Recommandation | `strategic_recommendation` |

---

## JSON Validation Rules

Before saving `benchmark.json`:
1. Parse with `python3 -c "import json; json.load(open('benchmark.json'))"` — must not error
2. Every `actors[].category` must match a key in `scope.actor_categories`
3. Every `actors[].dimensions` must contain keys matching `dimensions[].id`
4. Every dimension object must carry the sub-fields defined for this `benchmark_nature` in `references/profiles/<nature>.md`
5. `benchmark_nature` must be set and must have a profile file; `sector` must be set (free text is fine)
5b. `comparability.metrics` must be non-empty when `comparables[]` is present, and every `comparables[].metric` must match a declared metric
5c. Every `comparables[]` row carries a `confidence` from the enum, and a `value` or a `value_text` unless `confidence` is `absent`
5d. `comparables[].id` must be unique across the file, and `comparables[].actor` must appear in `scope.actors`
6. Every key of `market_landscape.segments` must be a segment id declared in `scope.segment_axis`
7. `pricing_matrix.data[].transparency_index` must be 1, 2, or 3 (commercial benchmarks)
8. `data_quality.retrieval_date` must be set
9. `actors[].uncertain_fields` must be an array (may be empty)
10. `mission-config.json` may contain an `execution` block with `batch_size` (integer, 1-10)

---

## Transparency Index Reference

| Score | Description | Example |
|-------|-------------|---------|
| **1** | Opaque — pricing only on request or after form submission | Alpaloc B2B |
| **2** | Partial — indicative prices published but no complete simulator | Rentalis Flexi |
| **3** | Transparent — full pricing simulator online, no registration needed | Carvio |
