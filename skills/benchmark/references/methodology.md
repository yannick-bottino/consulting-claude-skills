# Benchmark — Methodology Reference

## Purpose
This file is loaded by the skill when the consultant needs to configure the benchmark dimensions.
It explains the framework, default dimensions, and how to adapt them per mission.

---

## Default 4-Dimension Framework (reference: Velora LMD 2026)

| Dimension | What to cover |
|-----------|---------------|
| **1. Offre, Conditions & Promesse** | Durée(s) disponibles, type de contrat, flexibilité/résiliation, engagement, promesse client headline |
| **2. Contenu du service** | Ce qui est inclus : assurance, entretien, assistance, garanties, km inclus, frais additionnels |
| **3. Cibles & Tone of Voice** | Segments cibles (B2B/B2C/mixte), messaging principal, canaux, ton de la marque |
| **4. Pricing & Choix** | Grille tarifaire (par durée/gamme), dégressivité, comparaison km, frais cachés, transparence |

These are defaults. Each mission may add, remove, or relabel dimensions during initialization.

---

## Dimension Sub-Fields

Sub-fields are defined by the `benchmark_nature` profile, not here: `references/profiles/<nature>.md` section 1. The orchestrator injects the profile's block into `{dimension_sub_fields}` in the actor research prompt.

Single home, so a profile cannot drift from what the validator enforces (`DIM_SUBFIELDS_BY_NATURE` in `scripts/validate_benchmark.py`).

### Adding a new benchmark nature

See rule G2 in SKILL.md. In short: write `references/profiles/<nature>.md`, register its sub-fields in the validator, add the Phase 0 detection row, add an eval. A new **sector** needs none of that: it needs a search module and a sector row.

---

## Configuring Dimensions for a Mission

During Phase 0 (Init), the skill asks the consultant to validate or customize the dimensions.

> See `references/dimension-library.md` for sector-specific dimension proposals covering 12 markets
> (LMD, Assurance, Télécom B2B, Coworking, Banque & Fintech, Mobilité Electrique, Logistique,
> RH/SIRH, Santé au Travail, Financement PME, SaaS, Retail).

**Rules:**
- Keep between 3 and 6 dimensions for readability
- Each dimension maps to one column in the per-actor analysis table
- Dimensions should be mutually exclusive but collectively exhaustive for the market

*For full sector-specific frameworks (12 sectors), see `references/dimension-library.md`.*

---

## Actor Categories

Group actors by category for the executive summary competitive wheel. Categories vary by market.

- Example (LMD France / Velora): Leasers / LCD (Location Courte Durée) / Abonnements & Plateformes
- Example (Banque): Banques universelles / Banques digitales / Néobanques
- The consultant defines categories during Phase 0 initialization

---

## Data Integrity and Sourcing

Cross-phase rules: Quality Rules block D in SKILL.md.
Missing-data markers and their exact syntax: Step 5 of `references/data-sources.md`.
Source priority order and trust levels: the priority table in `references/data-sources.md`.

Not restated here: a marker or a priority order defined twice drifts.

---

## Claim Verification Protocol

> Added 2026-04-10 following discovery of systematic over-interpretation in RSE benchmark deliverables.

### The three-layer check

Before writing any factual claim in an actor file, apply this sequence:

**Layer 1 — Source verbatim exists?**
- Yes: quote it. Write the claim. Mark `OK`.
- No: the claim is an interpretation. Mark `[INTERPRETATION]`. Do NOT present it as fact.

**Layer 2 — Escalation check**
Compare the verb/qualifier in the claim against the verb in the source:

| Source says | You may write | You may NOT write |
|-------------|---------------|-------------------|
| "revue méthodologique", "methodology review" | "revue par X", "méthodologie validée par X" | "audité par X", "certifié par X" |
| "objectif visé", "target", "commitment" | "objectif : X", "ambition : X" | "certifié", "obtenu", "conforme" |
| "membre de" | "membre de" | "certifié par" |
| "en cours d'obtention" | "en cours" | "obtenu" |

**Layer 3 — Audit vs methodology distinction**
A third party validating a **tool's methodology** ≠ a third party auditing a **company's data**.

- "PwC performs annual reviews for methodological compliance [of Carbonfact]" → write: "méthodologie Carbonfact revue annuellement par PwC"
- Do NOT write: "bilan carbone audité par PwC" or "BC vérifié par PwC"

### Cross-file consistency check

Before finalizing any synthesis, verify that the same KPI has the same value in:
1. The actor file (actors/X.md)
2. The benchmark synthesis (synthese-benchmark.md)
3. The generation scripts and HTML outputs

When values differ: trace to primary source → use that value everywhere → document the correction.

---

## Benchmark Phases Overview

Phase list and their outputs: SKILL.md. Not duplicated here.
