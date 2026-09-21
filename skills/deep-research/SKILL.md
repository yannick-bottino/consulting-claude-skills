---
name: deep-research
description: |
  Use when the user requests a research report, literature review, market or industry analysis,
  competitive landscape, due diligence, policy brief, or technical deep-dive — anything needing
  evidence from many web sources synthesized with citations. Also triggers on: "research this topic", "write a report on",
  "survey the literature on", "competitive analysis of",...
---

# Deep Research

Create high-fidelity research reports with strict format control, evidence mapping, source governance, and multi-pass synthesis.

## What makes this produce provider-grade output

Three things drive deep-research quality, in order of impact. This skill is built around them; do not skip them under time pressure.

1. **Compute spent through a loop** — dozens of queries and full-page reads, not 5-6 snippet searches. Under-spending is the #1 quality leak.
2. **Dynamic re-planning** — decide what to search NEXT from what you just READ. The initial plan is a hypothesis, not a contract. See [references/replanning_loop.md](references/replanning_loop.md). This is the difference between this harness and static RAG.
3. **Verification** — a pass that checks every claim maps to a source that actually supports it. See P6/P7.

Semantic search / embeddings are NOT a quality driver for open-web research — a search engine already ranks the open web. Reranking belongs only on a closed corpus, or as a last-mile token-budget trim on already-scraped pages. See [references/retrieval_tiers.md](references/retrieval_tiers.md).

## Architecture: Lead Agent + Subagents + Replan Gate

```
Lead Agent (coordinator — minimizes raw search context)
  |
  P0: Probe environment (tier) + set effort budget + source policy
  |
  P1: Initial decomposition into sub-questions (HYPOTHESES, not a frozen plan)
  |
  P2: RESEARCH LOOP  ───────────────────────────────────────┐
  |   Dispatch ──→ Subagent A ──→ search broad → READ pages ─┤
  |            ──→ Subagent B ──→ writes task-b.md ──────────┤ (parallel)
  |            ──→ Subagent C ──→ writes task-c.md ──────────┘
  |        |                                                 |
  |   research-notes/  <─────────────────────────────────────┘
  |        |
  |   REPLAN GATE: lead reads notes → writes knowledge-state
  |        (KNOW / THINK / MISSING / CONTRADICTIONS / DECISION)
  |        |
  |   gaps remain + budget left? ──yes──> issue delta-queries, loop again
  |        |
  |        no (coverage sufficient OR budget exhausted)
  |        v
  P3: Build citation registry with source_type + as_of + authority
  P4: Evidence-mapped outline with counter-claim flags
  P5: Draft from notes (never from raw search results)
  P6: Counter-review (claims, confidence, alternatives, contradictions)
  P7: Verify (every [n] in registry, traceability check)
        → then polish to final report with confidence markers (see Output Requirements)
```

**Context efficiency:** Subagents' raw search results stay in their context and are discarded. Lead agent sees only distilled notes (~60-70% context reduction).

**Note on phase numbering:** the research loop is its own phase (P2); citation registry through verify are P3-P7, then a polish step (folded into Output Requirements). This shifts the old V6 numbering by one because the loop is now explicit. The Enterprise pipeline (E1-E7) is unchanged and slots into P2's loop.

## Mode & Effort Selection

Determine three things before starting:

| Dimension          | Options                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------- |
| **Topic Mode**     | Enterprise Research (company/corporation) OR General Research (industry/policy/tech)    |
| **Effort Budget**  | quick / standard / deep — sets query ceiling, replan gates, subagents (see table below) |
| **Retrieval Tier** | T1/T2/T3 — auto-probed at P0, governs HOW retrieval happens                             |

- **Enterprise Research Mode**: Six-dimension data collection with structured analysis frameworks (SWOT, risk matrix, competitive barrier quantification)
- **General Research Mode**: Standard P0-P8 research pipeline with source governance

**Effort budget** (the compute lever — the single biggest quality driver):

| Effort   | When                                | Initial sub-Qs | Replan gates (min) | Query ceiling | Subagents/round | Words     |
| -------- | ----------------------------------- | -------------- | ------------------ | ------------- | --------------- | --------- |
| quick    | single entity/concept, <30-word ask | 2-3            | 1                  | ~10-15        | 1-2             | 2000-4000 |
| standard | multi-entity comparison, default    | 4-6            | 2                  | ~25-40        | 3               | 3000-8000 |
| deep     | "深入"/"comprehensive"/DD/high-stakes | 6-10           | 3+                 | ~60-100       | 3-5             | 8000+     |

Ceilings force a STOP; reaching coverage early also forces a stop. Spend the full budget on `deep` — but spend it through the replan gate, never as a blind query dump. See [references/replanning_loop.md](references/replanning_loop.md).

## Source Governance (V6)

### Source Accessibility Classification

**CRITICAL RULE**: Every source must be classified by accessibility:

| Accessibility             | Definition                                                     | Examples                                                                     | Usage Rule                              |
| ------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------- |
| `public`                  | Available to any external researcher without authentication    | Public websites, news articles, WHOIS (without privacy), academic papers     | ✅ Always allowed                        |
| `semi-public`             | Requires registration or limited access                        | LinkedIn profiles, Crunchbase basic, industry reports (free tier)            | ✅ Allowed with disclosure               |
| `exclusive-user-provided` | User's paid subscriptions, private APIs, proprietary databases | Crunchbase Pro, PitchBook, private data feeds, internal databases            | ✅ **ALLOWED** for third-party research  |
| `private-user-owned`      | User's own accounts when researching themselves                | User's registrar for user's own company, user's bank for user's own finances | ❌ **FORBIDDEN** - circular verification |

**⚠️ CIRCULAR VERIFICATION BAN**: You must NOT:

- Use user's private data to "discover" what they already know about themselves
- Research user's own company by accessing user's private accounts
- Present user's private knowledge as "research findings"

**✅ EXCLUSIVE INFORMATION ADVANTAGE**: You SHOULD:

- Use user's Crunchbase Pro to research competitors
- Use user's proprietary databases for market research
- Use user's private APIs for investment analysis
- Leverage any exclusive source user provides for third-party research

### Source Type Labels

Every source MUST also be tagged with:

| Label                | Definition                             | Examples                                               |
| -------------------- | -------------------------------------- | ------------------------------------------------------ |
| `official`           | Primary source, official documentation | Company SEC filings, government reports, official blog |
| `academic`           | Peer-reviewed research                 | Journal articles, conference papers, dissertations     |
| `secondary-industry` | Professional analysis                  | Industry reports, analyst coverage, trade publications |
| `journalism`         | News reporting                         | Reputable media outlets, investigative journalism      |
| `community`          | User-generated content                 | Forums, reviews, social media, Q&A sites               |
| `other`              | Uncategorized or mixed                 | Aggregators, unverified sources                        |

**Quality Gates:**

- standard / deep effort: ≥30% official sources in final approved set
- quick effort: ≥20% official sources
- Maximum single-source share: ≤25% (standard/deep), ≤30% (quick)
- Minimum unique domains: 5 (standard/deep), 3 (quick)

## AS_OF Date Policy

Set `AS_OF` date explicitly at P0. For all time-sensitive claims:

- Include source publication date with every citation
- Downgrade confidence if source is older than relevant horizon
- Flag stale sources in registry (studies >3 years, news >6 months for fast-moving topics)

## P0: Probe Environment & Set Policy

### Step 1 — Probe the retrieval tier (no hooks; works in Cowork and Claude Code)

If `bash` + filesystem are available, run the probe:

```bash
python3 scripts/probe_env.py research-notes
```

It writes `research-notes/_env.md` with the recommended **TIER** (T1/T2/T3). You may override it if you know the sandbox blocks egress regardless. If `bash` is unavailable, you are in **T3**: use native `web_search` + `web_fetch` only, on full pages (never snippet-only). See [references/retrieval_tiers.md](references/retrieval_tiers.md) for what each tier means and the T1 install steps.

### Step 2 — Confirm core capabilities

| Check                            | Requirement                  | Impact if Missing                                    |
| -------------------------------- | ---------------------------- | ---------------------------------------------------- |
| web_search OR retrieve.py search | Required                     | Stop - cannot proceed                                |
| web_fetch OR retrieve.py scrape  | Required for full-page reads | Reads degrade, loop still runs                       |
| Subagent dispatch                | Preferred                    | Degrade to sequential (lead acts as each specialist) |
| Filesystem writable              | Required                     | In-memory notes only (lose context-efficiency)       |

### Step 3 — Set policy variables

- `AS_OF`: Today's date (YYYY-MM-DD) — mandatory for timed topics
- `EFFORT`: quick / standard / deep (sets the loop budget — see Mode & Effort table)
- `TIER`: T1 / T2 / T3 (from the probe)
- `SOURCE_TYPE_POLICY`: Enforce official/academic/secondary/journalism/community/other labels
- `COUNTER_REVIEW_PLAN`: What opposing interpretation to test

Report: `[P0 complete] Tier: {T1/T2/T3}. Subagent: {yes/no}. Effort: {quick/standard/deep}. AS_OF: {YYYY-MM-DD}.`

When researching a specific company/enterprise, follow this specialized workflow that ensures six-dimension coverage, quantified analysis frameworks, and three-level quality control.

### Enterprise Workflow Overview

```
Enterprise Research Progress:
- [ ] E1: Intake — confirm company entity, research depth, format contract
- [ ] E2: Six-dimension data collection (parallel where possible)
  - [ ] D1: Company fundamentals (entity, founding, funding, ownership)
  - [ ] D2: Business & products (segments, products, revenue structure)
  - [ ] D3: Competitive position (industry rank, competitors, barriers)
  - [ ] D4: Financial & operations (3-year financials, efficiency metrics)
  - [ ] D5: Recent developments (6-month events, strategic signals)
  - [ ] D6: Internal/proprietary sources (or note limitation)
- [ ] E3: Structured analysis frameworks
  - [ ] SWOT analysis (evidence-backed, 4 quadrants × 3-5 entries)
  - [ ] Competitive barrier quantification (7 dimensions, weighted score)
  - [ ] Risk matrix (8 categories, probability × impact)
  - [ ] Comprehensive scorecard (6 dimensions, weighted total)
- [ ] E4: L1/L2/L3 quality checks at each stage transition
- [ ] E5: Draft report using 7-chapter enterprise template
- [ ] E6: Multi-pass drafting + UNION merge (same as general Step 6-7)
- [ ] E7: Present draft for human review and iterate
```

## P1: Initial Decomposition (Hypotheses)

Decompose the research question into initial sub-questions, sized by EFFORT (quick 2-3, standard 4-6, deep 6-10). **These are hypotheses about where the answer lives, not a frozen plan.** P2's replan gate will revise, drop, and add sub-questions based on what gets read. Do not over-invest in a perfect plan here — getting into the field and reading is what reveals the real structure.

Each initial sub-question includes:

- **Expert Role**: Specialist persona (e.g., "Policy Historian", "Ecosystem Mapper")
- **Objective**: One-sentence investigation goal
- **Seed Queries**: 2-3 starting search queries (the loop will generate more)
- **Output**: Path to research notes file
- **Parallel Group**: Group A (independent) or Group B (depends on Group A)

Note: every sub-question is DEEP by default — subagents READ full pages, they do not stop at snippets. "SCAN-only" is not a depth choice; it is a degraded fallback when no fetch/scrape is available at all.

### Decomposition Rules

1. Each sub-question covers one coherent area a specialist would own
2. Group A sub-questions must be independent and source-diverse
3. Max 3 dispatched in parallel per round (concurrency limit)
4. Flag time-sensitive claims and citation-aging risk up front
5. **Start wide, then narrow** — first round explores the landscape; later rounds drill into the specific gaps the gate surfaces

### Enterprise Research Integration

When in Enterprise Research Mode, the initial sub-questions map to six dimensions:

- Company fundamentals / Business & products / Competitive position / Financial & operations / Recent developments / Internal-proprietary (or documented limitation)

Report: `[P1 complete] {N} initial sub-questions in {M} groups. Entering research loop.`

---

## Enterprise Research Mode (Specialized Pipeline)

When researching a specific company/enterprise, follow this specialized workflow that ensures six-dimension coverage, quantified analysis frameworks, and three-level quality control.

### E1: Intake

Same as P0/P1 above, plus:

- Confirm the exact legal entity being researched (parent vs subsidiary)
- Select research depth: Quick scan (3-5 pages) / Standard (10-20 pages) / Deep (20-40 pages)
- Identify any specific comparison targets (benchmark companies)

## P2: Research Loop (Dispatch → Read → Replan)

Subagents execute using [references/subagent_prompt.md](references/subagent_prompt.md) and output to [references/research_notes_format.md](references/research_notes_format.md).

This is the engine. It runs in ROUNDS. Each round dispatches subagents that search broad and READ full pages, then a REPLAN GATE decides whether to loop again. Full protocol: [references/replanning_loop.md](references/replanning_loop.md).

**Retrieval calls by tier** (from P0 probe, in `research-notes/_env.md`):

- **T1**: subagents call `python3 scripts/retrieve.py search "<q>"` then `scrape "<url>"` for full pages. If a call returns `NEEDS_NATIVE`, fall back to native tools for that call.
- **T2**: native `web_search` to discover, then `retrieve.py scrape` (trafilatura cleanup) or native `web_fetch` for full pages.
- **T3**: native `web_search` + `web_fetch` only. Full pages, never snippet-only.

### Each round

1. Dispatch up to 3 subagents in parallel (per EFFORT's subagents/round)
2. Each subagent: searches broad → READS full pages → tags source types → writes `task-{id}.md`
3. Wait for the round to complete
4. **REPLAN GATE** — lead reads the round's notes and appends a knowledge-state block to `research-notes/_knowledge_state.md`:
   - **KNOW** (established, ≥2 sources or 1 official) / **THINK** (weak, single-source) / **MISSING** (gaps + the specific next query for each) / **CONTRADICTIONS** (sources disagree + how to adjudicate) / **DECISION** (continue with listed delta-queries | stop: coverage sufficient | stop: budget exhausted)
5. If DECISION = continue → dispatch a new round targeting ONLY the MISSING items (delta-queries). Else exit the loop.

**At least one gate is mandatory** (quick), two (standard), three+ (deep). Running initial sub-questions to completion and skipping straight to P3 is the V6.1 failure mode — forbidden.

### Subagent Output Requirements

Each `task-{id}.md` must contain:

- **Sources section**: URLs from actual results with Source-Type, As Of, Authority (1-10), Accessibility
- **Findings section**: ≤10 one-sentence facts with source numbers
- **Full-Read Notes**: 2-3+ sources READ IN FULL with key data/insights (not snippet paraphrase)
- **Gaps section**: what was searched but NOT found, alternative interpretations

### Without Subagents (Degraded Mode)

Lead agent runs each sub-question sequentially, acting as each specialist, discarding raw results after writing notes. The replan gate still runs — sequential does not mean single-pass. Loop until coverage or budget.

### Stop conditions (exit the loop when EITHER holds)

- **Coverage sufficient**: every original sub-question has a KNOW-level answer, no MISSING item blocks the conclusion, contradictions resolved or flagged.
- **Budget exhausted**: hit the EFFORT query/round ceiling. On budget-exit, carry residual MISSING items into the report as stated limitations. Never hide a gap by stopping silently.

### Enterprise Research: Six-Dimension Collection

Follow [references/enterprise_research_methodology.md](references/enterprise_research_methodology.md) for per-dimension collection, source-priority matrix, and cross-validation. The six dimensions are the initial sub-questions; the replan gate still applies (e.g. a gap in D4 financials triggers a targeted delta-round).

**Key principles**: evidence-driven (every conclusion traces to a citable source); multi-source validation (key data needs ≥2 independent sources); restrained judgment (mark speculation); structured presentation (tables, lists).

Run L1 quality check after each dimension (see enterprise_quality_checklist.md).

Status per round: `[P2 round-{N}] {N} sources, {M} findings, decision: {continue/stop}.`
Status exit: `[P2 complete] {R} rounds, {N} total sources. Exit: {coverage/budget}. Building registry.`

### E3: Structured Analysis Frameworks

Apply frameworks from [references/enterprise_analysis_frameworks.md](references/enterprise_analysis_frameworks.md) in order:

1. **SWOT analysis** — each entry with evidence + source + impact assessment
2. **Competitive barrier quantification** — 7 dimensions with weighted scoring → A+/A/B+/B/C+/C rating
3. **Risk matrix** — 8 mandatory categories, probability × impact → Red/Yellow/Green
4. **Comprehensive scorecard** — 6-dimension weighted total → X/10

Run L2 quality check after analysis is complete.

### E4: Quality Control

Three-level checks from [references/enterprise_quality_checklist.md](references/enterprise_quality_checklist.md):

- **L1 (Data)**: Source count, attribution, cross-validation, timeliness
- **L2 (Analysis)**: SWOT completeness, risk coverage, barrier scoring, conclusion support
- **L3 (Document)**: Structure compliance, format consistency, readability, appendices

### E5: Draft Using Enterprise Template

Use the 7-chapter enterprise report template from enterprise_quality_checklist.md:

1. Company Overview
2. Business & Product Structure
3. Market & Competitive Position
4. Financial & Operations Analysis
5. Risks & Concerns
6. Recent Developments
7. Comprehensive Assessment & Conclusion

Plus appendices: Data Source Index, Glossary, Disclaimer.

### E3-E7: Enterprise Analysis, Drafting, and Review

- **E3: Structured Analysis** — Apply frameworks from [references/enterprise_analysis_frameworks.md](references/enterprise_analysis_frameworks.md)
- **E4: Quality Control** — Run L1/L2/L3 checks per [references/enterprise_quality_checklist.md](references/enterprise_quality_checklist.md)
- **E5: Draft** — Use 7-chapter enterprise template
- **E6-E7: Multi-Pass Drafting and Review** — Same as P4-P7 below

---

## P3: Citation Registry + Source Governance

Lead agent reads all task notes and builds unified registry.

### Registry Process

1. Read every task file's `## Sources` section
2. Merge all sources, deduplicate by URL
3. Assign sequential [n] numbers by first appearance
4. Tag: source_type, as_of date, authority score (1-10), task id
5. **Apply quality gates:**
   - standard / deep: ≥12 approved sources, ≥5 unique domains, ≥30% official
   - quick: ≥6 approved sources, ≥3 unique domains, ≥20% official
   - Max single-source share: ≤25% (standard/deep), ≤30% (quick)
6. **Drop sources** below threshold and list them explicitly

### Registry Output Format

```
CITATION REGISTRY

Approved:
[1] Author/Org — Title | URL | Source-Type: official | Accessibility: public | Date: 2026-03-01 | Auth: 8 | task-a
[2] ...

Dropped:
x Source | URL | Source-Type: community | Accessibility: privileged | Auth: 3 | Reason: PRIVILEGED SOURCE - NOT ALLOWED

Stats: {approved}/{total}, {N} domains, official_share {xx}%
Privileged sources rejected: {N}
```

**Critical rule:** These [n] are FINAL. P5 may only cite from Approved list. Dropped sources never reappear.

**Circular verification handling**: When researching the user's own company/assets, if you discover data in user's private accounts (e.g., user's domain registrar showing they own domains), you MUST:

1. Reject it from the registry (user already knows this)
2. Note it as "CIRCULAR - USER ALREADY KNOWS" in Dropped
3. Search for equivalent PUBLIC sources (e.g., public WHOIS, news articles)
4. Report from external investigator perspective only

**Exclusive source handling**: When user EXPLICITLY PROVIDES their paid subscriptions or private APIs for third-party research (e.g., "Use my Crunchbase Pro to research competitors"), you SHOULD:

1. Accept it as "exclusive-user-provided" accessibility
2. Use it as competitive advantage
3. Cite it properly in registry
4. If no public equivalent exists, mark as [unverified] or omit the claim

Report: `[P3 complete] {approved}/{total} sources. {N} domains. Official share: {xx}%. Privileged rejected: {N}.`

### Handling Information Black Box

When researching entities with no public footprint (like the "字节跳动子公司" example):

**What an external researcher would find:**

- WHOIS: Privacy protected → No owner info
- Web search: No news, no press releases
- Social media: No company pages
- Business registries: No public API or requires local access
- Result: **Complete information black box**

**Correct response:**

```
Findings: NO PUBLIC INFORMATION AVAILABLE

Sources checked:
- WHOIS (public): Privacy protected [failed]
- Company registry (public): Access denied/No API [failed]
- News media: No coverage [failed]
- Corporate website: Placeholder only [minimal]

Verdict: UNABLE TO VERIFY COMPANY EXISTENCE from external perspective
Sources found: 0 (or minimal, e.g., only WHOIS showing domain exists)
Confidence: N/A - Insufficient evidence
```

**DO NOT:**

- ❌ Use user's own credentials to "fill in the gaps"
- ❌ Assume the company exists based on domain registration alone
- ❌ Fill missing data with speculation
- ❌ Claim to have "verified" information you accessed through privileged means

**DO:**

- ✅ Clearly state what an external researcher can/cannot verify
- ✅ Document all failed search attempts
- ✅ Mark claims as [unverified] or omit entirely
- ✅ Downgrade effort to quick or stop if insufficient public sources
- ✅ Recommend direct contact for due diligence

---

## P4: Evidence-Mapped Outline

Lead agent reads notes + registry to build outline.

1. Identify cross-task patterns
2. Design sections topic-first, not task-order-first
3. Map each section to specific findings with source numbers
4. Flag sections needing counter-review
5. Mark recency-sensitive claims with AS_OF checks

Outline format:

```
## N. {Section Title}
Sources: [1][3][7] from tasks a, b
Claims: {claim from task-a finding 3}, {claim from task-b finding 1}
Counter-claim candidates: {alternative explanations}
Recency checks: {source dates + AS_OF}
Gaps: {limited official evidence}
```

---

## P5: Draft from Notes

Write section by section using [references/report_template_v6.md](references/report_template_v6.md).

**Rules:**

- Every factual claim needs citation [n]
- Numbers/percentages must have source
- Add **confidence marker** per section: High/Medium/Low with rationale
- Add **counter-claim sentence** when evidence conflicts
- No new sources may be introduced
- Use [unverified] for unsupported statements

**Anti-hallucination:**

- Lead agent never invents URLs — only from subagent notes
- Lead agent never fabricates data — mark [unverified] if number not in notes

Status: `[P5 in progress] {N}/{M} sections, ~{words} words.`

---

## P6: Counter-Review (Mandatory)

For each major conclusion, perform opposite-view checks:

1. **Could the conclusion be wrong?**
2. **Which high-impact claims depend on a single source?**
3. **Which claims lack official/academic support?**
4. **Are stale sources used for time-sensitive claims?**
5. **Find ≥3 issues** (re-examine if 0 found)

### Using Counter-Review Team (Recommended)

For comprehensive parallel review, use the Counter-Review Team:

```bash
# 1. Prepare inputs
counter-review-inputs/
  ├── draft_report.md
  ├── citation_registry.md
  ├── task-notes/
  └── p0_config.md

# 2. Dispatch to 4 specialist agents in parallel
SendMessage to: claim-validator
SendMessage to: source-diversity-checker
SendMessage to: recency-validator
SendMessage to: contradiction-finder

# 3. Wait for all specialists to complete

# 4. Send to coordinator for synthesis
SendMessage to: counter-review-coordinator
  inputs: [4 specialist reports]

# 5. Receive final P6 Counter-Review Report
```

See [references/counter_review_team_guide.md](references/counter_review_team_guide.md) for detailed usage.

### Manual Counter-Review (Fallback)

If Counter-Review Team is unavailable, perform manual checks:

- Verify every high-confidence claim has ≥2 sources
- Check official/academic backing for key claims
- Verify AS_OF dates on time-sensitive claims
- Document opposing interpretations

### Output

Include in final report:

```
## 核心争议 / Key Controversies
- **争议 1:** [主张 A 与反向证据 B 对比] [n][m]
- **争议 2:** ...
```

Report: `[P6 complete] {N} issues found: {critical} critical, {high} high, {medium} medium.`

---

## P7: Verify

Cross-check before finalization:

1. **Registry cross-check:** List every [n] in report vs approved registry
2. **Spot-check 5+ claims:** Trace to task notes
3. **Remove/fix non-traceable claims**
4. **Validate no dropped source resurrected**
5. **Check source concentration** for key claims

Report: `[P7 complete] {N} spot-checks, {M} violations fixed.`

---

## Output Requirements

- Match the requested language and tone
- Preserve technical terms in English
- Respect the report spec and formatting rules
- Include a references section or bibliography

## Reference Files

### Core Pipeline References (V7)

| File                                                                        | When to Load                                                                 |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [retrieval_tiers.md](references/retrieval_tiers.md)                         | **P0**: which retrieval stack the env supports (T1/T2/T3) + T1 install       |
| [replanning_loop.md](references/replanning_loop.md)                         | **P2 (CRITICAL)**: the research loop + replan gate — the core quality driver |
| [source_accessibility_policy.md](references/source_accessibility_policy.md) | **P0**: source classification rules — read with retrieval_tiers              |
| [subagent_prompt.md](references/subagent_prompt.md)                         | P2: subagent dispatch                                                        |
| [research_notes_format.md](references/research_notes_format.md)             | P2: subagent output format                                                   |
| [report_template_v6.md](references/report_template_v6.md)                   | P5: draft with confidence markers and counter-review                         |
| [quality_gates.md](references/quality_gates.md)                             | All phases: quality thresholds and anti-hallucination checks                 |
| [evaluation_rubric.md](references/evaluation_rubric.md)                     | After delivery: score output quality / iterate with skill-creator            |

### General Research References

| File                                                                            | When to Load                                   |
| ------------------------------------------------------------------------------- | ---------------------------------------------- |
| [research_report_template.md](references/research_report_template.md)           | Build outline and draft structure              |
| [formatting_rules.md](references/formatting_rules.md)                           | Enforce section formatting and citation rules  |
| [source_quality_rubric.md](references/source_quality_rubric.md)                 | Score and triage sources                       |
| [research_plan_checklist.md](references/research_plan_checklist.md)             | Build research plan and query set              |
| [completeness_review_checklist.md](references/completeness_review_checklist.md) | Review for coverage, citations, and compliance |

### Enterprise Research References (load when in Enterprise Research Mode)

| File                                                                                | When to Load                                                                          |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [enterprise_research_methodology.md](references/enterprise_research_methodology.md) | Six-dimension data collection workflow, source priority, cross-validation rules       |
| [enterprise_analysis_frameworks.md](references/enterprise_analysis_frameworks.md)   | SWOT template, competitive barrier quantification, risk matrix, comprehensive scoring |
| [enterprise_quality_checklist.md](references/enterprise_quality_checklist.md)       | L1/L2/L3 quality checks, per-dimension checklists, 7-chapter report template          |

## Anti-Patterns

- **Frozen plan** — running P1's initial sub-questions to completion and going straight to P3 with no replan gate. The #1 thing that makes output static-RAG-grade. At least one gate is mandatory.
- **Under-spending compute** — 5-6 snippet searches and done. Compute through the loop is the top quality driver; spend the EFFORT budget.
- **Snippet satisficing** — claiming a fact as established from a search snippet without a full-page read.
- **Replanning without reading** — writing the knowledge-state from result titles instead of subagent notes.
- **Contrarian padding** — inventing MISSING items to justify another round. Question answered → stop.
- **Bolting on semantic search for discovery** — embeddings do not fix open-web research; the search engine already ranks. Reranking only on closed corpus or as a token-budget trim on scraped pages.
- Single-pass drafting; splitting passes by section instead of full report drafts
- Ignoring the format contract; claims without citations
- Mixing conflicting dates without calling out discrepancies
- Copying external AI output without verification; deleting intermediate drafts
- **Lead agent reading raw search results** — only read subagent notes
- **Inventing URLs** — only use URLs from actual search results
- **Resurrecting dropped sources** — dropped in P3 never reappear
- **Missing AS_OF for time-sensitive claims** — always include source date
- **Skipping counter-review** — mandatory P6 must find ≥3 issues
- **CIRCULAR VERIFICATION** — never use user's private data to "discover" what they already know about themselves
- **IGNORING EXCLUSIVE SOURCES** — when user provides Crunchbase Pro etc. for competitor research, USE IT
- **Self-graded quality labels** — do not claim "outperforms X" in the output. Prove quality with the evaluation rubric, not a slogan.

## Next Step: Verify and Deliver

After completing research, suggest verification and output:

```
Research report complete: [N] sources cited, [M] claims made.

Options:
A) Verify facts — run /fact-checker on the report (Recommended)
B) Create slides — run /daymade-docs:ppt-creator from the findings
C) Export as PDF — run /daymade-docs:pdf-creator for formal delivery
D) No thanks — the report is ready as-is
```
