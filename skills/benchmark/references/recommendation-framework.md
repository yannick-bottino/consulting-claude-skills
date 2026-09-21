> **Scope: nature `offer` only.** This frame assumes a buyer to win. For another nature, section 4 of `references/profiles/<nature>.md` defines the frame to produce and this file does not apply.

# Standard / Singularité / Unicité — Recommendation Framework

This is the single source of truth for the Strategic Recommendation methodology used in Phase 3e.

---

## The Three Layers

### STANDARD DE MARCHÉ

**Definition:** Features or practices present in ≥80% of benchmark actors.

For a 4-actor benchmark: present in ≥3 actors.
For a 6-actor benchmark: present in ≥5 actors.

**Purpose:** Table stakes. The client MUST have these to be credible. They do not differentiate — they are the price of entry. If the client lacks any standard feature, that is a critical gap to fix before competing.

**Examples (LMD France):**
- Durée variable (1 à 12 mois minimum)
- Assurance incluse dans le forfait
- Grille tarifaire publiée en ligne
- Choix de plusieurs segments de véhicule
- Sans apport / sans LOA

**How to identify:**
1. Read all actor JSONs
2. For each feature in `dimensions.contenu_service.content` and `dimensions.offre_conditions.content`, count how many actors offer it
3. If count ≥ (n_actors × 0.8), round up → it's a Standard

---

### SINGULARITÉ DU CLIENT

**Definition:** Features where the client outperforms most competitors on a shared competitive terrain.

**Requirements:**
- At least 2 other actors offer something similar (shared terrain) — but the client's version is measurably better, cheaper, simpler, or faster
- OR the client is clearly differentiated on a dimension where all actors compete

This is NOT a niche advantage. It's a competitive win on a terrain that matters to most buyers.

**Examples (Velora LMD 2026):**
- 100% digital, sans agence physique → plus rapide que les acteurs traditionnels
- P2P pricing → ~20-30% moins cher que les concurrents pour engagements 1-6 mois
- Zéro frais de mise en route → avantage pricing perçu vs Rentalis/Rouli

**How to identify:**
1. Read `pricing-synthesis.md` → identify where the client price undercuts the field
2. Read each actor's `insights_positive` and `a_retenir` → identify shared competitive traits
3. For each client advantage, verify: are at least 2 competitors in the same arena but weaker?
4. If yes → document as Singularité with evidence and source

---

### UNICITÉ DU CLIENT

**Definition:** Segments for which the client is the ONLY viable option — not just better, but structurally irreplaceable.

**Requirements:**
- Structural barrier prevents other actors from serving this segment (not just price preference)
- Examples of structural barriers: credit check required, bancaire history required, B2B-only offer, French RIB required, long-term engagement mandatory, geographic exclusion

**Examples (Velora LMD 2026):**
- Étudiants étrangers (sans domiciliation bancaire française) → les leasers et LCD exigent un compte FR ou garant FR
- Travailleurs en visa court séjour → engagement 12+ mois impossible pour un séjour de 3 mois
- Personnes en situation de précarité financière → score bancaire exigé par la plupart des acteurs

**How to identify:**
1. Read `targets-analysis.md` → segments barriers section
2. For each excluded segment, identify WHICH actors exclude them and WHY (structural reason)
3. Check if the client has no such barrier for this segment
4. If client can serve the segment and all/most competitors cannot → document as Unicité

---

## How to Build the Recommendation (Phase 3e)

### Step 1 — Read inputs
- All actor JSONs (dimensions, insights, sources)
- `pricing-synthesis.md` (comparison table, degressivity, transparency index)
- `targets-analysis.md` (segments, barriers, population funnel)
- `market-landscape.md` (positioning by category/duration)

### Step 2 — Build STANDARD list
For each benchmark dimension and sub-feature: count actors, mark those at ≥80% threshold.

### Step 3 — Build SINGULARITÉ
1. List all client advantages identified in research
2. For each: verify ≥2 competitors compete on the same terrain
3. Select the 2-3 strongest advantages with evidence
4. Write 1 differentiator phrase ("Cœur de proposition")

### Step 4 — Build UNICITÉ
1. List all segments where structural barriers exclude most actors
2. Verify the client has no equivalent barrier
3. For each viable segment: name the barrier + why client wins

### Step 5 — Build pricing_chart
Extract from `pricing-synthesis.md`:
- Client prices for 1m/3m/6m/12m
- Each competitor's prices for same durations
- Set `is_client: true` for the client row

### Step 6 — Write recommendation.md
Use Template 7 from `references/format-templates.md`.
Write to `outputs/[mission-slug]/recommendation.md`.

---

## Quality Rules for This Framework

1. **Standard must be evidence-based.** Count actors from JSONs, don't infer.
2. **Singularité requires a named competitor.** "Le client est moins cher" is not enough — "Le client est 23% moins cher que Rentalis sur 1 mois (source: pricing-synthesis.md)" is.
3. **Unicité requires a named structural barrier.** "Difficile d'accès" is not a structural barrier. "Scoring bancaire Experian requis par l'acteur X" is.
4. **Pricing chart must use real prices from pricing-synthesis.md.** Never estimate or fabricate pricing chart data.
5. **Each section must have at least 1 entry.** If Unicité has no genuine segment, leave it empty with a note — do not invent segments.
