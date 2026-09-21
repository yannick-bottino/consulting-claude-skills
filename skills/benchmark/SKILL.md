---
name: benchmark
description: Produces a sourced, structured competitive benchmark of 3 or more actors, from scoping to client deliverable. Two methods: offer comparison (offers, inclusions, pricing, positioning) or maturity assessment against a grid (ESG, data, AI, cyber, accessibility). Per-actor research with traced sources, dated screenshots of key pages as evidence, comparison matrix, market landscape, executive summary, recommendation, self-contained HTML report, and a quality scorecard with an iteration loop. Invoke explicitly with /benchmark.
disable-model-invocation: true
---

# Benchmark Skill

## What this skill does

This skill guides a consultant through a structured competitive benchmark:

- **Phase 0** — Interactive init: configure market, actors, dimensions via AskUserQuestion
- **Phase 1+2** — Parallel actor research: subagent dispatch + validation per actor (with sequential fallback)
- **Phase 3** — Synthesis: pricing comparison, target population, executive summary, market landscape, recommendation
- **Phase 4** — Final output: Markdown files + `benchmark.json`
- **Phase 5** — HTML report: navigable dashboard, branding resolved per mission
- **Phase 6** — Quality Scorecard: auto-evaluation on the applicable total
- **Phase 7** — Iteration loop: diagnostic gaps → corrections ciblées → régénération livrables → re-score (max 3 itérations, convergence ≥90%)

**Reference files (load when the step names them):**
- `references/profiles/` — one file per `benchmark_nature`: sub-fields, deliverable set, comparable metrics, recommendation frame, scorecard sections, capture intents (Phase 0, read before Q4)
- `references/methodology.md` — dimension framework, claim verification protocol
- `references/dimension-library.md` — sector-specific dimension proposals (Phase 0, Q4)
- `references/format-templates.md` — Markdown output templates (Templates 1-7)
- `references/data-sources.md` — sourcing protocol, scraper levels, citation format, missing-data markers
- `references/output-schemas.md` — `benchmark.json` schema v3, projections, Markdown→JSON mapping
- `references/format-templates.md` — Markdown templates and the mission-config template (Template 5)
- `references/recommendation-framework.md` — Standard/Singularité/Unicité methodology (Phase 3e)
- `references/branding.md` — branding contract: token resolution, logo, neutral fallback (Phase 0 + Phase 5)
- `references/capture-spec.md` — screenshot intents, capture plan, manifest, evidence rules (Step 1.4)
- `references/html-report-spec.md` — report structure, radar, design system, validation (Phase 5)
- `references/scorecard.md` — scoring criteria, applicability model, Template 8 (Phase 6)
- `references/iteration-loop.md` — correction protocol and convergence rules (Phase 7)
- `references/agent-prompts/actor-research-prompt.md` — rigid prompt template for parallel actor research
- `references/agent-prompts/outline-agent-prompt.md` — Research Outline Agent (Step 1.05)
- `references/agent-prompts/quality-evaluator-prompt.md` — Quality Evaluator Agent (after each actor batch)
- `references/agent-prompts/search-modules/` — sector-specific search strategies (loaded by prompt template)
- `references/examples/` — saved gold-standard outputs from past missions
- `scripts/scrape.py` — scraper detection and page scraping (Step 0.1)
- `scripts/setup-scraper.sh` — one-off local Crawl4AI install (also installs Chromium for capture)
- `scripts/capture.py` — deterministic screenshot capture (Step 1.4)
- `scripts/consent.json` — consent-banner handlers, data file grown per mission
- `scripts/validate_benchmark.py` — automated field coverage validation (v2 backward compat)
- `scripts/extract_pdf.py` — PDF/PPTX → PNG multimodal extraction (PyMuPDF)

**Path convention:** `{skill_path}` is this skill's own folder. Substitute it in every command below. Never hardcode an install path.

---

## Resume Capability

This skill supports resuming interrupted missions:
- **Phase 1+2:** Checks for existing validated `actors/{slug}.json` files → skips completed actors
- **Phase 3:** Checks for existing synthesis files → skips if present, unless the consultant asks to regenerate a named file
- **Phase 4:** Always rebuilds `benchmark.json` from actor JSONs (idempotent)
- **Phase 5:** Always regenerates HTML from `benchmark.json`

To force a full re-run, delete the `outputs/{mission-slug}/` directory.

---

## Phase 0: Initialization — ALWAYS run first, never skip

The skill adapts itself to the mission context. Do not assume market, actors, or dimensions.

### Step 0.1 — Scan project context, detect scraper and branding

Before asking questions:
1. Check if a `CLAUDE.md` exists in the current folder → read it for mission context
2. List files in `sources/` → note any client documents available
3. If MEMORY.md exists → read it for prior decisions on this mission
4. Resolve the branding source per `references/branding.md` section 5 → record it in `mission-config.json → branding`
5. Detect which web scraper is available:

```bash
python {skill_path}/scripts/scrape.py --check
# Returns: scraper=crawl4ai | scraper=jina | scraper=none
python {skill_path}/scripts/capture.py --check
# Returns: capture=playwright derivatives=pillow | capture=playwright derivatives=none | capture=none
```

Communicate to the consultant:
- `crawl4ai` → "Scraper : Crawl4AI local (JS rendering activé)"
- `jina` → "Scraper : Jina Reader (pages statiques — pour les SPAs, lancer `bash {skill_path}/scripts/setup-scraper.sh`)"
- `none` → "Scraper : WebSearch natif uniquement (résultats partiels possibles)"
- `capture=playwright` → "Captures d'écran : disponibles (illustration des livrables)"
- `capture=none` → "Captures d'écran : indisponibles — le rapport affichera des liens vers les sites, pas d'images"

### Step 0.2 — Interactive scoping (AskUserQuestion — one question at a time)

Ask these questions sequentially. Wait for each answer before asking the next. Skip a question if the answer is already clear from CLAUDE.md or MEMORY.md.

**Q1 — Market & client:**
> "Quel est le marché analysé et pour quel client ? (ex: Location Moyenne Durée France pour Velora, ou Assurance emprunteur pour Banque Solaris)"

**After Q1 — Classify on two independent axes.**

The **nature** decides the method: dimension sub-fields, deliverable set, recommendation frame, scorecard sections, capture intents. The **sector** decides where to look: sources, queries, vocabulary, known traps. Keeping them separate is what lets a new subject reuse an existing method.

**Axis 1 — `benchmark_nature`** (read the matching profile before Q4):

| Signal in the market description | `benchmark_nature` | Profile |
|---|---|---|
| offre, pricing, tarifs, positionnement commercial, concurrentiel, comparatif d'offres | `offer` | `references/profiles/offer.md` |
| maturité, RSE, ESG, durabilité, impact, data, IA, cyber, accessibilité, évaluation sur grille | `maturity` | `references/profiles/maturity.md` |
| *(anything else, or two natures with equal weight)* | `generic` | `references/profiles/generic.md` |

**Axis 2 — `sector`**: the market's own domain, free text plus an optional search module:

| Signal | `sector` | Sector module loaded |
|---|---|---|
| RSE, sustainability, ESG, développement durable, impact, CSR | `sustainability` | `sustainability-rse.md` |
| *(no dedicated module yet)* | *(free text from Q1)* | *(default modules only)* |

Store both in `mission-config.json`. A legacy config carrying `benchmark_type` is read as an alias: `commercial` → `offer`, `rse` → `maturity` + sector `sustainability`.

If the nature is ambiguous, ask:
> "Est-ce qu'on compare des **offres** (ce que chaque acteur vend, à quel prix, à qui) ou une **maturité** (où en est chaque acteur sur un sujet, évalué sur une grille) ? Cela change les livrables et la méthode, pas seulement les sources."

Read the selected profile now: it governs everything from Q4 onward.

**Q2 — Actors to analyze (with peer discovery if list is empty):**

If the consultant provides a list → use it directly, skip peer discovery.

If the consultant says "propose a list" or leaves it open → run **Step 0.2b — Peer Discovery** before asking:

#### Step 0.2b — Peer Discovery (run only when actor list is not provided)

1. **Macro search** to find market participants:
   ```
   WebSearch: "[market] acteurs principaux France [year] comparatif
   WebSearch: "[market] opérateurs offre concurrents benchmark
   ```
2. **Compile a candidate list** (aim for 8-15 names) with a one-line description of each
3. **Categorize** by business model, using the market's own vocabulary (ex: pure-players digitaux, acteurs historiques, industriels intégrés)
4. **Present to consultant for validation:**
   > "Voici les acteurs identifiés sur le marché [X]. Je les ai regroupés par catégorie :
   >
   > **Catégorie A — [type] :** [actor 1], [actor 2], [actor 3]
   > **Catégorie B — [type] :** [actor 4], [actor 5]
   > ...
   >
   > Quels acteurs souhaitez-vous inclure dans le benchmark ? Vous pouvez valider ma liste, la réduire, ou ajouter des acteurs manquants."

5. **Wait for validation** before proceeding to Q3. The confirmed list becomes the benchmark scope.

> "Quels acteurs souhaitez-vous benchmarker ? Listez-les, par catégorie si possible. Je peux aussi proposer une liste si vous me donnez le marché."

**After Q2 — Set the locale.** Derive `locale` from the market and client: `output_language` (the language every deliverable is written in), `country` (drives the statistical office in `public-statistics.md`), `currency` (drives price formatting and the comparability contract). Default to `fr` / `FR` / `EUR` only when the mission is French: an English-speaking client gets English deliverables, and a Swiss market gets CHF and the OFS, not INSEE. State the resolved locale in the mission brief.

**After Q2 — Check the panel size.** Below 3 actors, the recommendation method degenerates: a "present in at least 80% of the panel" threshold becomes unanimity, and "at least 2 competitors on the same ground" is satisfied by the whole panel. Say so and let the consultant choose:
> "Le panel ne compte que {N} acteurs. La méthode de recommandation (socle, écart, avantage) suppose au moins 3 acteurs pour que les seuils aient un sens. Trois options : ajouter un ou deux acteurs, garder {N} acteurs et livrer sans la recommandation, ou garder {N} acteurs en assumant une recommandation qualitative non chiffrée."

Record the choice in `mission-config.json → execution.panel_note`.

**Q3 — Scope (skip if already clear):**
> "Y a-t-il un périmètre spécifique ? (géographie, segment B2B/B2C, produit ou offre de référence, unité de comparaison, autre contrainte)"

From the answer, derive two things.

**The comparability contract** (`mission-config.json -> comparability`): what makes two actors comparable. Reference product or profile, currency, periods, scope (tax basis, volume, geography), and the list of metrics with their units. Without it, two figures land in the same column while measuring different things, which is the most common way a benchmark misleads a client. If the consultant cannot state it, propose one and get it validated: an explicit imperfect contract beats an implicit one.

**The segment axis** of the market: the 2 to 4 segments that structure it, plus which one is the mission focus. Examples: contract duration brackets, coverage tiers, company size bands, distribution models. Store it in `mission-config.json → scope.segment_axis`. It drives the Phase 3d map and the report landscape section. If the market has no such axis, record a single segment and move on.

**Q4 — Dimensions (read `references/dimension-library.md` first):**

Before asking, detect the sector from Q1's answer using the keyword table in `dimension-library.md`.
Load the matching sector entry. If no exact match, use the closest sector + adapt with `references/methodology.md`.
If the market spans two sectors equally (e.g., "assurance auto LMD"), use the primary sector entry and flag cross-sector adaptations in a parenthetical next to the relevant dimension (e.g., "Contenu du service *(adapté : inclut les garanties assurance comme en assurance emprunteur)*").

Present a **structured selection menu** — not just a list:

> "Voici les axes d'analyse que je propose pour le marché **[market]**, adaptés au secteur **[sector]** :
>
> | # | Dimension | Ce qu'elle couvre |
> |---|-----------|-------------------|
> | 1 | **[Dim 1]** | [1-line description] |
> | 2 | **[Dim 2]** | [1-line description] |
> | 3 | **[Dim 3]** | [1-line description] |
> | 4 | **[Dim 4]** | [1-line description] |
> | 5 | **[Dim 5]** *(optionnel)* | [1-line description] |
>
> **Pourquoi ces axes ?** [2-3 sentences: why this selection fits the market — name at least one specific competitive dynamic of the sector, e.g. pricing opacity, digital maturity gap, flexibility as differentiator]
>
> Options :
> - **A)** Valider ces 4 dimensions (standard)
> - **B)** Valider les 5 dimensions (plus détaillé)
> - **C)** Modifier une ou plusieurs dimensions
> - **D)** Proposer vos propres axes"

Wait for answer. If C or D: iterate until locked. If A or B: confirm and proceed.

The "Pourquoi ces axes ?" block is not optional — it demonstrates market understanding and builds consultant trust before data collection starts.

**Q5 — Deliverables (this answer decides the scope):**

The profile's deliverable table is the maximum available for the nature; this answer is what gets produced. Whatever is not in `deliverables` is neither produced, nor validated, nor scored. Write the resolved list into `mission-config.json` using the exact keys: `actor-sheets`, `comparison-synthesis`, `targets-analysis`, `market-landscape`, `exec-summary`, `recommendation`, `screenshots`, `html-report`. If the consultant's wording is ambiguous (a "synthèse" can mean the comparison matrix or the executive summary), read back the resolved list before saving.

> "Quel livrable attendez-vous ? (a) Analyse complète [exec summary + fiches acteurs + pricing + cibles], (b) Fiches acteurs uniquement, (c) Autre ?"

### Step 0.3 — Confirm mission brief and save config

Synthesize all answers into a mission brief and present it:
> "Cadrage de la mission :
> - **Marché :** [market]
> - **Client :** [client]
> - **Acteurs retenus :** [list with categories]
> - **Acteurs exclus (si applicable) :** [actors considered but not retained — one-line reason each]
> - **Dimensions :** [list]
> - **Livrable :** [scope]
> - **Charte :** [branding.resolved — skill name, token file path, or "palette neutre"]
> - **Locale :** [langue des livrables] · [pays] · [devise]
> - **Comparabilité :** [produit de référence, unité, périodes, périmètre]
> On démarre ?"

Wait for explicit confirmation. Then:
1. Create `outputs/[mission-slug]/` directory
2. Save `outputs/[mission-slug]/mission-config.json` (see `references/format-templates.md` → Template 5)

---

## Phase 1+2: Parallel Actor Research (Data Collection + Analysis)

> **Architecture (2026-03-20):** Phases 1 and 2 are merged into a single parallel
> dispatch phase. Each actor is researched by an independent subagent using a rigid prompt
> template from `references/agent-prompts/actor-research-prompt.md`.
> The orchestrator dispatches, validates, and gates — it does NOT research actors itself.

### Step 1.0 — Resume check (run before any dispatch, including the outline agent)

For each actor in the confirmed list:
1. Check if `outputs/{mission-slug}/actors/{actor-slug}.json` exists
2. If it exists, validate it:
   ```bash
   python {skill_path}/scripts/validate_benchmark.py actor "outputs/{mission-slug}/actors/{actor-slug}.json" "outputs/{mission-slug}/mission-config.json"
   ```
3. If validation PASSES → mark this actor as "already done", skip it
4. If validation FAILS → include it in the dispatch queue

If every actor is already done, skip Step 1.05 and Step 1.2 entirely and go to Phase 3.

Present resume status to consultant:
> "Reprise détectée : {N} acteurs déjà analysés et validés ({list}). {M} acteurs restants à analyser.
> On continue avec les {M} restants ?"

If no previous outputs exist, skip this step silently.

### Step 1.05 — Build research brief + dispatch Outline Agent

#### Step A — Dispatch Outline Agent (Deep-Research pattern)

Before building the research brief, dispatch a single outline agent to pre-extract all known data from client documents:

```
Agent(
  description: "Research outline for {mission_name}",
  prompt: [outline-agent-prompt.md with all {variables} substituted],
  subagent_type: "general-purpose",
  run_in_background: false   ← wait for completion before dispatching actor subagents
)
```

The prompt template is at `references/agent-prompts/outline-agent-prompt.md`.

Variables to substitute:
- `{market_name}`, `{client_name}`, `{mission_slug}`, `{sources_dir}`, `{output_dir}`, `{skill_path}`, `{current_date}`
- `{actors_list}` — comma-separated list of actor names from mission config

After the outline agent completes, read `outputs/{mission_slug}/research-outline.json`.

**If `sources/` is empty or no source docs exist:** Skip the outline agent dispatch entirely and go directly to Step B.

#### Step B — Build research brief

Generate `outputs/{mission-slug}/research-brief.md` containing:

1. **Contexte client** — Qui est le client, pourquoi ce benchmark, ce qu'il cherche à comprendre
2. **Grille de comparabilité** — Métriques exactes à collecter et leur unité (devise, TTC/HT, durées, produit de référence, unité de volume, périmètre), pour garantir que les données de chaque acteur sont directement comparables
3. **Points d'attention sectoriels** — Pièges connus du marché, tirés du search module sectoriel (opacité tarifaire, frais cachés, rebranding, périmètres d'offre non comparables)
4. **Données déjà connues par acteur** (injected from research-outline.json):

   ```
   ### Données déjà connues par acteur (à ne pas re-rechercher)

   Pour chaque acteur dans research-outline.json :
   - known_prices → inclure dans le brief : "Prix déjà connus : [liste]"
   - known_services → inclure : "Services déjà identifiés : [liste]"
   - client_doc_mentions → inclure : "Sources client disponibles : [liste]"
   - research_hints → inclure : "Points d'attention : [liste]"
   ```

   This prevents actor subagents from re-finding data already extracted by the outline agent.

5. **Tableau des acteurs** — Nom, catégorie, hypothèses B2B/B2C, points d'attention spécifiques par acteur

Ce fichier est injecté dans la variable `{research_brief}` du prompt template de chaque subagent.

**Save to:** `outputs/{mission-slug}/research-brief.md`

---

### Step 1.1 — Prepare subagent context

Before dispatching, the orchestrator MUST:

1. **Read search modules** from `references/agent-prompts/search-modules/`:
   - `official-website.md` — ALWAYS loaded
   - `financial-data.md` — ALWAYS loaded
   - `market-intelligence.md` — loaded if actor has low public visibility
   - `public-statistics.md` — loaded only if `targets-analysis` is in deliverables scope
   - `sustainability-rse.md` — loaded if `sector` is `sustainability`
   - *(future sector modules can be added here following the same pattern)*

2. **Read the prompt template** from `references/agent-prompts/actor-research-prompt.md`
   - **Hard Constraint:** reproduce the template exactly, only replacing `{variables}`

3. **Substitute every variable** listed in the Variables section of `references/agent-prompts/actor-research-prompt.md`. `{comparability_json}` carries the comparability contract verbatim: without it the subagent cannot produce valid comparable rows, and the whole comparison chain falls back to prose. That section is authoritative: it is maintained with the template, so a new variable added to the template cannot be missed here. A `{placeholder}` left unsubstituted in a dispatched prompt is a defect.

### Step 1.2 — Batch dispatch

Read `execution.batch_size` from mission-config.json (default: 3).
Dispatch actors in batches.

**For each batch:**

1. **Dispatch N subagents in parallel** using the Agent tool:
   ```
   For each actor in batch:
     Agent(
       description: "Research {actor_name}",
       prompt: [actor-research-prompt.md with all {variables} substituted],
       subagent_type: "general-purpose",
       run_in_background: true
     )
   ```

2. **Wait for all agents in batch to complete**

3. **Validate each output (structural):**
   ```bash
   python {skill_path}/scripts/validate_benchmark.py actor "outputs/{mission-slug}/actors/{actor-slug}.json" "outputs/{mission-slug}/mission-config.json"
   ```

4. **Dispatch Quality Evaluator per actor** (Deep-Research pattern):

   After structural validation passes, dispatch a quality evaluator for each actor:
   ```
   Agent(
     description: "Evaluate quality of {actor_name} research",
     prompt: [quality-evaluator-prompt.md with variables substituted],
     subagent_type: "general-purpose",
     run_in_background: false
   )
   ```

   Variables: `{actor_name}`, `{actor_json_path}`, `{actor_md_path}`, `{mission_config_path}`, `{benchmark_nature}`

   The prompt template is at `references/agent-prompts/quality-evaluator-prompt.md`. It scores on the applicable criteria and returns `score_pct`.

   **If verdict = FAIL (`score_pct` < 60):**
   - Append the gap list to the original actor research prompt
   - Re-dispatch the actor research agent once (maximum 1 re-dispatch per actor)
   - After re-dispatch completes, re-run structural validation + quality evaluator
   - **Do NOT re-dispatch a second time** — if the verdict is still FAIL, accept the output and flag it in the batch results

5. **Present batch results to consultant:**
   > "Batch {X}/{Y} terminé :
   >
   > | Acteur | Validation | Qualité | Sources | N/D | Estimations | Incertitudes |
   > |--------|------------|---------|---------|-----|-------------|-------------|
   > | {actor} | PASS | {score_pct}% | {N} | {N} | {N} | {N} |
   >
   > Options :
   > - **A)** Valider et lancer le batch suivant
   > - **B)** Relancer les acteurs en échec
   > - **C)** Voir le détail d'un acteur avant de continuer"

6. **If FAIL actors exist and consultant chooses B:** re-dispatch with error context appended to prompt

### Step 1.3 — Sequential fallback

If the Agent tool is not available or the consultant prefers sequential mode:

> "Mode séquentiel activé. Analyse acteur par acteur."

Then for each actor, execute the research inline using the same search modules as parallel mode:
1. Load `references/agent-prompts/search-modules/official-website.md` and `financial-data.md` for search strategy
2. Scan `sources/` for actor mentions (client documents first)
3. Scrape official website using detected scraper (follow official-website.md protocol)
4. Run WebSearch for financial data (follow financial-data.md protocol)
5. Produce `actors/{actor-slug}.json` + `actors/{actor-slug}.md` (same schema as parallel mode)
6. Validate with `validate_benchmark.py` — fix any FAIL before proceeding
7. Continue to next actor

### Step 1.4 — Capture pass (evidence screenshots)

Skip if `screenshots` is not in the mission deliverables, or if `capture=none` was detected in Phase 0.

Read `references/capture-spec.md`, then:

1. Merge every `capture_targets` array from the validated actor JSONs into `outputs/{mission-slug}/capture-plan.json`
2. Run the capture in one pass:
   ```bash
   python {skill_path}/scripts/capture.py --plan "outputs/{mission-slug}/capture-plan.json" --out "outputs/{mission-slug}/actors/screenshots"
   ```
3. Read `capture-manifest.json` and fold each entry into `actors[].screenshots`, replacing whatever was there
4. Retry the transient failures only, with the full plan:
   ```bash
   python {skill_path}/scripts/capture.py --plan "outputs/{mission-slug}/capture-plan.json" --out "outputs/{mission-slug}/actors/screenshots" --only-status failed
   ```
   Never hand-build a reduced plan: the manifest is the evidence register, and `--only-status` exists so a retry cannot damage it. Re-fold after the retry.
5. Structural blockers (`captcha`, `waf`, `geoblock`, `http-4xx`, `cert-expired`) are documented as gaps and never retried

The orchestrator captures, not the subagents: one browser, one setting, so every screenshot in the report looks like it belongs to the same document. A consent banner that survives is fixed by adding its handler to `scripts/consent.json`, never by patching the script.

### Step 1.5 — All actors complete

After all batches are done and validated:

> "Phase 1+2 terminée : {N} acteurs analysés et validés.
> - Sources totales : {N}
> - Données manquantes (N/D) : {list}
> - Estimations : {list}
> - Champs incertains : {list}
> - Captures : {N} ok, {N} bloquées ({raisons}), {N} en échec
>
> Passage à la Phase 3 (synthèse) ?"

---

## Phase 3: Synthesis Sections

Produce in this order (the comparison synthesis first — it feeds the exec summary).

### Phase 3a — Comparison Synthesis
Use Template 3 from `references/format-templates.md`.
- Build the comparison table by pivoting `comparables[]`: rows are actors, columns are the periods declared in `comparability.periods`. Never retype a figure by hand, pivot it
- Show `confidence` in the table: an estimated value is marked, an absent one carries its reason
- Calculate degressivity (% discount between the shortest and the longest commitment)
- Assign transparency index (1/2/3) per actor
- **Save to:** `outputs/[mission-slug]/pricing-synthesis.md`

The profile decides what this section compares and how the file is named: `pricing-synthesis.md` for `offer`, `maturity-synthesis.md` for `maturity`, `comparison-synthesis.md` for `generic`. Same role in every case: the matrix that feeds the executive summary. Skip the section if the profile marks it not applicable.

### Phase 3b — Target Population Analysis (if in scope)
Use Template 4 from `references/format-templates.md`.
- Size the addressable population with a funnel built on named public statistics for the mission geography
- Map each actor to its primary/secondary segment
- Extract messaging frameworks: tagline, tone, copy example per actor (source: official website/landing pages)
- Identify non-addressable segments with barrier analysis (price, usage, awareness)
- Use `[ESTIMATION]` markers for any calculation based on assumptions
- **Save to:** `outputs/[mission-slug]/targets-analysis.md`

### Phase 3c — Executive Summary
Write this last (after all actors are analyzed and pricing is done).
Use Template 2 from `references/format-templates.md`.
- Context: 2-3 sentences
- Positioning table: all actors, 1 differentiating point each
- Key insights: 3-5 facts with data (no fabrication)
- Strategic recommendation: 3-5 sentences structured as follows:
  1. **Market gap** — which segment or need is underserved by current players?
  2. **Client positioning opportunity** — where can the client win, and why them specifically?
  3. **Priority lever** — one concrete action (pricing, segment, feature, channel)
  4. **Risk / watch-out** — what must be avoided or monitored
  Ground each point in benchmark evidence — cite specific actors, prices, or positioning facts. No generic strategy advice.

**Before saving exec-summary.md — build roue_concurrentielle data:**

1. Read `insights_positive` and `insights_negative` from all actor JSONs
2. For each insight, classify it on one of the configured dimension ids (`dimensions[].id` from mission-config). The axes are the mission's dimensions, never a fixed list
3. Write the following block to `benchmark.json → roue_concurrentielle`:
   ```json
   {
     "center_common": ["List of features/practices common to all actors"],
     "differentiators_positive": [
       {"actor": "ActorName", "axis": "contenu_service", "label": "Short differentiator (≤10 words)"}
     ],
     "differentiators_negative": [
       {"actor": "ActorName", "axis": "offre_conditions", "label": "Short weakness (≤10 words)"}
     ]
   }
   ```
4. Axis classification guide:
   - `contenu_service` — what's included: assurance, entretien, km, assistance, équipements
   - `offre_conditions` — contract terms: engagement, flexibilité, annulation, frais
   - `cibles` — targeting and messaging: B2B/B2C, segments, ton
   - `pricing` — price level, transparency, degressivity

- **Save to:** `outputs/[mission-slug]/exec-summary.md`

### Phase 3d — Market Landscape Map

Use Template 6 from `references/format-templates.md`.

1. Read the segment field and `category` from all actor JSONs
2. Build the segment × category positioning grid. Segments come from `mission-config.json → scope.segment_axis`, set in Phase 0 (Q3) from the market's own structure. Mark which segment is the mission focus
3. List all actors included in the benchmark with rationale (1 line each)
4. List actors excluded from the benchmark (if any were considered but dropped) with reason

**Save to:** `outputs/[mission-slug]/market-landscape.md`

Also write `benchmark.json → market_landscape`, one key per segment on the axis:
```json
{
  "segment_axis": { "id": "axis id", "label": "axis label", "focus": "segment id" },
  "segments": {
    "[segment id]": ["Actor names operating in this segment"]
  },
  "categories": {
    "CategoryName": ["Actor names in this category"]
  }
}
```

If the market has no meaningful segment axis, use a single segment named after the market and say so in the file. Never force an axis borrowed from another sector.

### Phase 3e — Strategic Recommendation

**The profile owns the frame.** Read section 4 of `references/profiles/<nature>.md` first: it names the three blocks to produce. For `offer` that frame is Standard / Singularité / Unicité, detailed in `references/recommendation-framework.md` with Template 7. For any other nature the profile's frame wins, and `recommendation-framework.md` and Template 7 do not apply: they are the `offer` frame, not the skill's frame.

1. **Read inputs:** all actor JSONs + `pricing-synthesis.md` + `targets-analysis.md` + `market-landscape.md`
2. **Build STANDARD:** list features present in ≥80% of actors (≥3/4 for 4-actor benchmark)
3. **Build SINGULARITÉ:** for each client advantage, verify ≥2 competitors compete on same terrain
4. **Build UNICITÉ:** identify segments where structural barriers exclude most competitors
5. **Build pricing_chart:** client vs each competitor for all 4 durations (from `pricing-synthesis.md`)

Write `benchmark.json → recommendation` following the schema in `references/output-schemas.md`.

**Save to:** `outputs/[mission-slug]/recommendation.md`

---

## Phase 4: Final Output

### Step 4.1 — Assemble and validate benchmark.json

Build the complete `benchmark.json` following the full schema in `references/output-schemas.md`.

Order matters: merge every `actors[].comparables` into the benchmark-level `comparables[]` first, then generate the projections (`pricing_matrix`, `vehicle_catalog`, `recommendation.pricing_chart`) from it for the `offer` nature. A value in a projection that is absent from `comparables[]` is a defect, not a bonus.

Validate:
```bash
python -c "import json; data = json.load(open('outputs/[mission-slug]/benchmark.json')); print(f'Valid — {len(data[\"actors\"])} actors')"
```

### Step 4.2 — Automated quality check

Run the full benchmark validation:
```bash
python {skill_path}/scripts/validate_benchmark.py benchmark "outputs/{mission-slug}/benchmark.json"
```

Review the validation report. If FAIL:
- Fix the identified issues in benchmark.json
- Re-run validation until PASS

**A PASS is structural, not editorial.** It says every field exists, not that the benchmark has anything to compare. Read the `substance` block the validator prints: it gives the share of comparable rows carrying a value, and names any metric absent for every actor. If the comparison's central metric is empty, say it in the delivery summary in those words, before the file list. A 100% structural coverage on an empty benchmark is the most misleading signal the skill can produce.

Re-fold `actors[].screenshots` from `capture-manifest.json` before writing, even if Step 1.4 already did it: a retry between the two leaves the copy stale, and a stale `ok` entry is how a dead page becomes evidence.

Carry `deliverables` into `benchmark.json`: the validator and the scorecard both read it to decide what applies. Without it, both fall back to warning about sections the mission never ordered.

Then run the secondary manual checklist:
- [ ] Every actor has at least 1 source URL
- [ ] No quantitative claim without source (rule D2)
- [ ] Every missing-data marker carries a reason, per Step 5 of `references/data-sources.md`, and is reflected in `data_quality`
- [ ] All configured dimensions have data in every actor sheet
- [ ] `uncertain_fields` arrays are populated for actors with estimated data

### Step 4.3 — Delivery summary

Present to the consultant:
> "Benchmark terminé. Voici ce qui a été produit dans `outputs/[mission-slug]/` :
>
> - [N] fiches acteurs : `actors/[actor1].md`, `actors/[actor2].md`...
> - Synthèse pricing : `pricing-synthesis.md`
> - Analyse cibles : `targets-analysis.md` *(si applicable)*
> - Cartographie du marché : `market-landscape.md`
> - Executive Summary : `exec-summary.md`
> - Recommandation stratégique : `recommendation.md`
> - Données structurées : `benchmark.json` ([N] acteurs)
>
> **Points de vigilance :**
> - Données manquantes (N/D) : [list actors/fields]
> - Estimations : [list what was estimated]
> - Champs incertains : [list uncertain_fields]
>
> Ces fichiers alimentent directement la Phase 5 (rapport HTML) et le skill PPT pour la production du livrable final."

---

## Phase 5: Rapport HTML navigable

Skip this phase if `html-report` is not in the mission deliverables.

### Step 5.1 — Générer le rapport

Read `references/branding.md`, then `references/html-report-spec.md`. Generate `outputs/[mission-slug]/benchmark-report.html` from `benchmark.json` following that spec.

Non-negotiables (the spec holds the detail):
- `benchmark.json` is the only data source. No figure in the HTML that is absent from it
- Visual identity resolved through the branding contract. No literal colour or font name outside the `:root` token block
- Self-contained file: inline CSS and JS, no external request
- A section whose source data is missing is hidden, never rendered empty. No placeholder, no empty frame

### Step 5.2 — Valider

Run the validation checklist in `references/html-report-spec.md` section 7. Fix every failed item before delivery.

### Step 5.3 — Delivery summary

> "Rapport HTML généré dans `outputs/[mission-slug]/benchmark-report.html`.
>
> - Dashboard navigable, {N} sections, données issues de `benchmark.json`
> - Charte : {branding.resolved}
> - Fichier autonome, à ouvrir directement dans un navigateur
>
> Ce fichier peut être partagé tel quel au client ou servir de base à la production PPT."

---

## Phase 6: Quality Scorecard

Read `references/scorecard.md` and score this run against it. Save the result to `outputs/[mission-slug]/benchmark-scorecard.md` using Template 8 of that file.

Two rules override any habit:
- The total is the **applicable** total, never a fixed 80. Which sections apply depends on `benchmark_nature` and on the deliverable scope
- A section that cannot apply is marked `N/A` and excluded from the denominator, never scored 0

Consumed by Phase 7: `score_pct` and the classified gap table.

---

## Phase 7: Iteration Loop

Read `references/iteration-loop.md` and follow it.

Entry rule: `score_pct` ≥ 90% delivers. Below that, correct the top 3 corrigeable gaps, regenerate the affected deliverables, re-score. A section scored 0 by hard fail (unsourced figure, escalated claim) forces an iteration whatever the total. Maximum 3 iterations, then deliver as is with the structural limits documented.

---

## Quality Rules — Always Apply

Rules carry stable IDs. Adding one means appending to its theme block with the next free ID. Never renumber, and never open a second rule list anywhere else in this skill: one list, one home.

### D — Data integrity

- **D1. Never fabricate data.** No exceptions. A fabricated figure survives into a slide and gets presented to a C-level audience as fact. When a value is missing, mark it and flag it to the consultant.
- **D2. Every price point and every market sizing figure carries a source**: a URL, a named and dated publication, or a client document reference with page.
- **D3. Verbatim sourcing is mandatory for factual claims.** Every certification status, third-party attribution, and quantitative figure carries the exact quote from its source. With no verbatim, mark the claim `[INTERPRETATION]` and never promote it to stated fact. Never conflate a methodology review with a data audit: apply the three-layer check in `references/methodology.md`. [2026-04-10]
- **D4. Cross-file consistency is mandatory.** The same fact holds the same value in every file it appears in. On conflict, trace back to the primary source verbatim and propagate that value everywhere. [2026-04-10]

Missing-data markers (`[N/D]`, `[ESTIMATION]`, `[INTERPRETATION]`, stale-data note) have a single definition: Step 5 of `references/data-sources.md`. Do not invent a marker.

### S — Sourcing and research

- **S1. Scrape when the URL is known, search when the data lives elsewhere.** Scraping official pages beats search snippets for offers, pricing, and service content. WebSearch stays mandatory for data official sites never publish: financial KPIs of non-listed actors, registries, press. The two are complementary, not interchangeable. [2026-03-19]
- **S2. Client documents: searched late, trusted high.** Public sources come first because they are verifiable, but a value found only in `sources/` still belongs in the actor table, cited with file and page. Never mark a cell missing when the value sits in a client brief.
- **S4. A URL is citable only if a fetch of it returned usable content.** Never cite a plausible-looking URL, and never nominate one for capture: a run of 2026-07-29 cited a 404 page as a pricing source, and nothing caught it until the capture pass returned `http-404`. A search-engine snippet is a **lead, not a source**: it does not make its URL citable. A value known only from a snippet is still recorded, with `confidence: interpreted`, the engine and query in `note`, and no `source_ref`. Never promote it to `observed`, and never discard it either: dropping a found value because its page would not load loses the benchmark's substance. [2026-07-29]
- **S3. Never read a file marked "golden source" during a run.** Those are reference extractions of the final deliverable: reading them biases the run. [2026-03-21]

### F — Format and deliverable

- **F1. Deliverables must be mechanically parseable.** Markdown tables: every row carries the same number of `|`-separated cells as the header, because the downstream PPT skill parses them programmatically. JSON: `benchmark.json` and every actor file validate before saving. [F2 fusionnée ici le 2026-07-29 pour tenir le plafond de 15 règles]
- **F3. "À retenir" is one sentence, 30 words maximum, no bullets.** It maps to a single call-out cell. Needing bullets means the differentiating insight has not been found yet.
- **F4. Insights are opinionated judgments, not data summaries.**

### G — Skill genericity

- **G1. Never hardcode a sector or a method into the skill.** Method material is injected through the `{benchmark_nature}` profile (sub-fields, deliverables, recommendation frame, scorecard sections, capture intents). Sector material is injected through the `{sector}` search module. SKILL.md and the prompt templates stay free of both. [2026-04-10, révisé 2026-07-29]
- **G2. Extend on the right axis.** A new **method** ships a profile in `references/profiles/<nature>.md` (sub-fields, deliverables, comparables, recommendation frame, scorecard sections, capture intents), a sub-fields entry in `scripts/validate_benchmark.py`, a Phase 0 detection row, and an eval. A new **domain** ships only a search module in `references/agent-prompts/search-modules/` and a sector row. Never write a profile to describe a sector, never write a search module to describe a method. [2026-04-10, révisé 2026-07-29]
- **G3. The skill embeds no brand charter.** Visual identity is resolved per mission through `references/branding.md`, so the skill runs on any organisation's charter. [2026-07-28]

### P — Process

- **P1. Work incrementally**: ask, collect, analyse, synthesise. Never batch everything silently then dump the output.

---

## Self-Improvement — Toujours actif

Ce skill se met à jour de lui-même à chaque retour du consultant.

### Quand mettre à jour ce fichier

**Retour positif** — le consultant dit : "parfait", "exactement ça", "garde ça", "très bon", valide un output sans réserve, ou exprime une satisfaction explicite sur un choix non évident.
→ Identifier ce qui a produit ce résultat et l'inscrire en règle permanente dans la section Quality Rules ci-dessus.

**Red flag** — le consultant dit : "non pas comme ça", "ne fais plus ça", "c'est un problème", pointe une erreur, demande une correction, ou rejette un output.
→ Identifier la cause racine et ajouter une règle explicite pour ne pas reproduire ce comportement.

### Protocole de mise à jour

Dès qu'un retour qualifié est détecté :

1. **Formuler la règle** : une phrase impérative, courte, sans ambiguïté.
2. **Choisir le bloc thématique** dans Quality Rules (D, S, F, G, P) et ajouter la règle avec le prochain ID libre de ce bloc, suffixée par `[AAAA-MM-JJ]` pour la traçabilité. Ne jamais renuméroter les règles existantes, ne jamais ouvrir une seconde liste.
3. **Si la règle porte sur un fichier de référence plutôt que sur le comportement global** (format de sortie, critère de scoring, protocole de recherche), l'écrire dans ce fichier de référence et non dans Quality Rules. Quality Rules ne contient que les règles transverses à toutes les phases.
4. **Confirmer au consultant** :
   > "Compris — j'ai ajouté cette règle dans le skill : *[règle en une phrase]*. Elle s'appliquera à toutes les missions futures."

5. **Consolider avant d'ajouter** : parcourir le bloc concerné.
   - Si la nouvelle règle est déjà couverte → ne pas dupliquer, préciser la règle existante.
   - Si deux règles se chevauchent → fusionner en une seule plus précise, en conservant les deux dates.
   - Objectif : 15 règles maximum au total. Au-delà, fusionner dans le bloc le plus chargé.

### Ce qui NE justifie pas une mise à jour

- Corrections ponctuelles liées au contexte d'une mission spécifique (ne pas généraliser)
- Préférences esthétiques sans impact sur la qualité du livrable
- Instructions déjà couvertes par une règle existante

### Sauvegarder les bons outputs

Quand le consultant valide un livrable sans réserve, copier la version validée dans `references/examples/` sous `[type]-[marché]-[année].md` et ajouter une ligne dans `references/examples/README.md` (mission, type de benchmark, ce que cet exemple démontre).

Ces exemples servent de référence de qualité pour les runs suivantes. Ils ne sont jamais lus pendant une run de recherche (règle S3) : ils se consultent en amont, au moment du cadrage, ou en aval pour comparer un livrable fini.
