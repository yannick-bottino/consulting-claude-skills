# Search Module: Sustainability / RSE (Rapports, Certifications, D&I, HRDD)

> **Loaded by:** actor-research-prompt.md
> **Use for:** Every actor in an RSE/sustainability benchmark — ALWAYS load this module.
> **Critical rule:** Official website scraping alone will NOT surface PDFs, certification scores, D&I KPIs, or HRDD policies. Dedicated searches are REQUIRED for each sub-type below.

---

## Search Strategy Overview

RSE data is scattered across 7 distinct source types. Each requires a dedicated search pass.
Do NOT rely on a single "sustainability page" — the most valuable data is often buried in PDFs,
third-party platforms, or sub-pages not linked from the main navigation.

---

## Pass 1 — Sustainability Report PDFs

**CRITICAL:** Most fashion brands publish annual sustainability/RSE reports as downloadable PDFs.
These contain 80%+ of the quantitative data (GHG breakdown, audit rates, supplier KPIs, targets).

**Search queries (run ALL of them, not just one):**
```
"{actor_name}" sustainability report PDF {current_year}
"{actor_name}" sustainability report PDF {current_year - 1}
"{actor_name}" rapport RSE PDF {current_year}
"{actor_name}" rapport RSE PDF {current_year - 1}
"{actor_name}" rapport développement durable PDF
"{actor_name}" impact report PDF
site:{actor_domain} filetype:pdf sustainability OR RSE OR impact
```

**If the brand belongs to a group (LVMH, Kering, Tapestry, Capri...):**
```
"{group_name}" Document d'Enregistrement Universel {current_year - 1}
"{group_name}" ESG report PDF {current_year - 1}
"{group_name}" social environmental responsibility report PDF
```

**Data Freshness Rule — MANDATORY:**
When a KPI is available for multiple years (e.g., 2024 and 2025), ALWAYS capture and report the most recent year first. If older data provides useful context, include it as: "X% (2025) vs Y% (2024)" with explicit dates. NEVER silently choose an older year when a newer year is available.

**What to extract from PDFs:**

*Core Climate KPIs:*
- Scope 1/2/3 GHG emissions (tCO2e) with year and baseline
- SBTi status and reduction targets
- Reduction % vs baseline year

*Materials & Sourcing (Fashion-Critical):*
- Total % preferred/sustainable/certified materials (and how the brand defines "preferred")
- Material composition breakdown by fiber type: % cotton, % wool, % polyester, % nylon, % leather, % MMCF — with certification split for each fiber (e.g., "81% organic/regenerative/recycled cotton")
- % of each major fiber certified by standard (GOTS %, RWS %, LWG %, GRS %, etc.)
- Regenerative or organic material coverage % by fiber
- Any fiber-specific annexes or tables — extract ALL data from those tables

*Supply Chain & Audits:*
- Audit coverage by tier (% Tier 1, % Tier 2, % Tier 3 audited)
- Geographic breakdown of audit coverage by country or region (e.g., "95% China, 17% Portugal")
- Total number of audits conducted per year
- Grievance mechanism coverage (% of factories with mechanism, case volumes)

*Labor & Wages:*
- Living wage coverage % with methodology noted (Anker, FWN, WageIndicator, etc.)
- Any wage breakdown tables by country or factory size

*Circular Economy:*
- Repair, resale, or recycling volumes (units, % of sales, tCO2e saved)
- Take-back program coverage and results

*Governance & Team:*
- Sustainability team size and structure
- Carbon squad or dedicated climate team headcount
- Board-level ESG oversight

*D&I Demographics:*
- % women in workforce, management, board
- EgaPro score (France)
- D&I targets with timeline

**PDF Extraction Technique for Large PDFs (>50 pages):**
1. Read the table of contents first (usually pages 2-5)
2. Identify sections matching the categories above
3. Use the `pages` parameter to extract relevant sections
4. For sections with tables or breakdowns: extract ALL data in that section — do NOT cherry-pick
5. Always note the page range where data was found
6. If a 2025 report is available and you initially extracted from a 2024 report, STOP and re-extract from 2025

**Scraping instruction:**
Use `extract_pdf.py` from the skill scripts if available, or read the PDF directly with the Read tool.
For large PDFs (>50 pages), use the `pages` parameter to read relevant sections.

---

## Pass 2 — Certifications & Labels

**Search queries:**
```
"{actor_name}" B Corp score certified
site:bcorporation.net "{actor_name}"
"{actor_name}" Fair Wear Foundation member
site:fairwear.org "{actor_name}" brand performance check
"{actor_name}" GOTS certified percentage
"{actor_name}" RWS certified wool
"{actor_name}" OEKO-TEX Standard 100
"{actor_name}" Bluesign certification
"{actor_name}" SA8000 certification
"{actor_name}" SBTi targets committed approved
site:sciencebasedtargets.org "{actor_name}"
"{actor_name}" Good On You rating
"{actor_name}" Fashion Transparency Index score
```

**What to extract:**
- B Corp score (numeric) + certification year
- Fair Wear membership level (Leader/Good/Needs improvement) + year
- GOTS/RWS/OEKO-TEX coverage % of products
- SBTi status (Committed/Targets Set/Approved) + scope + targets
- Good On You rating (1-5) + date
- Fashion Transparency Index score (%) + year
- Any other sustainability label with quantitative score

---

## Pass 3 — D&I (Diversité & Inclusion)

**Search queries:**
```
"{actor_name}" diversity inclusion report
"{actor_name}" diversité inclusion
"{actor_name}" D&I report
"{actor_name}" gender equality
"{actor_name}" EgaPro index score
"{actor_name}" women leadership percentage
site:{actor_domain} diversity OR inclusion OR D&I OR égalité
```

**What to extract:**
- % women in workforce
- % women in senior management / leadership
- % women on board
- EgaPro score (France-specific, /100)
- Gender pay gap %
- D&I training programs
- ERG (Employee Resource Groups) existence
- Diversity targets with timeline

---

## Pass 4 — Living Wage & Fair Wages

**Search queries:**
```
"{actor_name}" living wage suppliers
"{actor_name}" salaire vital fournisseurs
"{actor_name}" fair wage commitment
"{actor_name}" living wage percentage
"{actor_name}" Fair Wage Network member
site:{actor_domain} living wage OR salaire vital
```

**What to extract:**
- % suppliers paying living wage
- Living wage methodology used (Anker methodology, FWN, SA8000)
- Timeline/targets for living wage coverage
- Purchasing practices commitments (prompt payment, no unauthorized subcontracting)

---

## Pass 5 — HRDD & Due Diligence

**Search queries:**
```
"{actor_name}" human rights due diligence policy
"{actor_name}" devoir de vigilance plan
"{actor_name}" HRDD policy PDF
"{actor_name}" modern slavery statement
"{actor_name}" code of conduct suppliers
"{actor_name}" plan de vigilance
site:{actor_domain} vigilance OR "due diligence" OR "human rights"
```

**What to extract:**
- HRDD/Vigilance plan existence (published Y/N)
- Coverage: which tiers and geographies
- Grievance mechanism existence
- Corrective action process documented
- Modern Slavery Act statement (UK law)
- Responsible purchasing practices policy

---

## Pass 5.5 — Materials & Fiber Sourcing (Fashion-Critical)

> **Why a dedicated pass:** Materials data is fashion-specific and almost never surfaces from generic sustainability searches. Brands maintain dedicated materials/fabric pages, fiber trackers, and sourcing annexes that require targeted scraping.

**Search queries (run ALL):**
```
"{actor_name}" materials sourcing sustainable fibers percentage
"{actor_name}" matières premières durables pourcentage
"{actor_name}" preferred materials breakdown fiber
"{actor_name}" cotton organic percentage certified
"{actor_name}" wool RWS certified percentage
"{actor_name}" polyester recycled GRS percentage
"{actor_name}" leather LWG certified percentage
"{actor_name}" regenerative agriculture fibers
"{actor_name}" GOTS certified percentage products
"{actor_name}" fiber traceability breakdown
site:{actor_domain} materials OR matières OR fibers OR fibres OR fabric
{actor_domain}/materials
{actor_domain}/our-materials
{actor_domain}/fabrics
{actor_domain}/sourcing
{actor_domain}/matières
```

**What to extract (MANDATORY — do not skip any item):**
- Total % preferred/sustainable/certified materials (brand's own definition of "preferred")
- **Fiber-by-fiber breakdown** (the most commonly missed data):
  - % cotton + certification split (organic %, GOTS %, recycled %)
  - % wool + certification split (RWS %, Responsible Wool %)
  - % polyester + certification split (recycled GRS %, rPET %)
  - % nylon/polyamide + certification split (Econyl %, recycled %)
  - % leather + certification split (LWG %, vegetable-tanned %)
  - % MMCF (viscose, lyocell, modal) + certification split (ECOVERO %, Tencel %)
  - % cashmere + certification split (GCS %, responsible sourcing %)
  - Any regenerative material % (regenerative cotton, regenerative wool, etc.)
- Material certification targets with timeline
- Fiber-specific annexes or tables — extract ALL data rows
- EIM score (if denim brand — Jeanologia Environmental Impact Measurement)
- Traceability depth by material (T1 only, T2, T3, raw material origin)

---

## Pass 5.6 — Supply Chain & Audit Depth

> **Why a dedicated pass:** Audit coverage data is highly granular and spread across supplier codes of conduct, audit reports, and interactive maps. It requires scraping dedicated supply chain/sourcing pages.

**Search queries (run ALL):**
```
"{actor_name}" supplier audit coverage percentage
"{actor_name}" factory audit results tier 1 tier 2
"{actor_name}" audit fournisseurs couverture
"{actor_name}" supply chain transparency map factories
"{actor_name}" supplier list factories count
"{actor_name}" grievance mechanism suppliers workers
"{actor_name}" mécanisme alerte fournisseurs
"{actor_name}" corrective action plan suppliers
"{actor_name}" audits sociaux nombre {current_year}
site:{actor_domain} suppliers OR supply chain OR fournisseurs OR factories OR audit
{actor_domain}/supply-chain
{actor_domain}/sourcing
{actor_domain}/fournisseurs
{actor_domain}/our-suppliers
{actor_domain}/transparency
{actor_domain}/traceability
```

**What to extract:**
- Audit coverage % by tier (Tier 1, Tier 2, Tier 3)
- **Geographic audit breakdown by country or region** (e.g., "95% China vs 17% Portugal") — frequently missed
- Total number of audits conducted per year with year noted
- Audit methodology (SMETA, BSCI, SA8000, ICS, internal)
- **Grievance mechanism coverage**: % factories with worker grievance mechanism, case volumes reported
- Supplier list published (Y/N) + URL if yes
- Number of Tier 1 vs Tier 2 suppliers
- HRDD geographic asymmetry (flag when high-risk countries have lower coverage than low-risk)
- Corrective action closure rate if available

---

## Pass 5.7 — Sustainability Frameworks & Initiatives

> **Why a dedicated pass:** Framework participation (SBTi, SBTN, ZDHC, Fashion Pact, etc.) is highly impactful for maturity scoring but requires dedicated searches against each platform's own database.

**Search queries (run ALL):**
```
"{actor_name}" Science Based Targets SBTi committed approved
site:sciencebasedtargets.org "{actor_name}"
"{actor_name}" SBTN AR3T biodiversity nature targets
"{actor_name}" Fashion Pact signatory
"{actor_name}" ZDHC member chemicals
"{actor_name}" UN Global Compact signatory
"{actor_name}" Sustainable Apparel Coalition Higg Index
"{actor_name}" Ellen MacArthur Foundation circular economy
"{actor_name}" 1.5°C target pathway
"{actor_name}" Net Zero commitment timeline
"{actor_name}" RE100 renewable energy commitment
"{actor_name}" CDP climate score disclosure
site:cdp.net "{actor_name}"
```

**What to extract:**
- SBTi status: Committed / Targets Set / Approved — with scope (1+2 only vs 1+2+3) and % reduction target
- SBTN/AR3T: nature commitments (Assess, Reduce, Restore, Transform) — participation level
- Fashion Pact signatory status + commitments signed
- ZDHC membership level if applicable
- CDP score (A, A-, B, etc.) + year
- UN Global Compact signatory
- Any other framework with quantitative commitment or score
- Renewable energy % (current) + RE100 target year

---

## Pass 6 — Sustainability Sub-Pages (Topic-Specific Scraping)

Many brands bury key RSE data in sub-pages NOT linked from the main sustainability hub. **Generic hub scraping is not enough** — each topic area requires its own dedicated URL sweep.

**Step 1 — Discover the sustainability hub:**
```
site:{actor_domain} sustainability OR responsabilité OR impact OR engagements
{actor_domain}/sustainability
{actor_domain}/responsabilite
{actor_domain}/impact
{actor_domain}/about/sustainability
{actor_domain}/engagements
{actor_domain}/our-impact
{actor_domain}/responsibility
{actor_domain}/esg
{actor_domain}/csr
```

**Step 2 — Scrape topic-specific sub-pages (MANDATORY — 4 topic categories):**

*Materials topic pages:*
```
{actor_domain}/materials
{actor_domain}/our-materials
{actor_domain}/fabrics
{actor_domain}/sourcing
{actor_domain}/matières
{actor_domain}/sustainability/materials
```

*Supply chain topic pages:*
```
{actor_domain}/supply-chain
{actor_domain}/our-suppliers
{actor_domain}/transparency
{actor_domain}/traceability
{actor_domain}/fournisseurs
{actor_domain}/sustainability/supply-chain
```

*Climate & circularity topic pages:*
```
{actor_domain}/climate
{actor_domain}/circular
{actor_domain}/circularity
{actor_domain}/repair
{actor_domain}/resale
{actor_domain}/sustainability/climate
```

*People & governance topic pages:*
```
{actor_domain}/people
{actor_domain}/diversity
{actor_domain}/inclusion
{actor_domain}/workers
{actor_domain}/community
{actor_domain}/governance
```

**For each sub-page found:** scrape with `scrape.py` or WebFetch and extract structured data. Note: data found on official sub-pages should be considered **current year** unless explicitly dated otherwise — do NOT default to PDF report data when the website shows more recent figures.

---

## Pass 7 — Recent News & Updates + Final Freshness Verification

**Step 1 — News search:**

```
"{actor_name}" sustainability news {current_year}
"{actor_name}" RSE actualités {current_year}
"{actor_name}" new certification {current_year}
"{actor_name}" B Corp recertification {current_year}
"{actor_name}" SBTi approved {current_year}
"{actor_name}" sustainability award {current_year}
"{actor_name}" materials progress {current_year}
"{actor_name}" living wage update {current_year}
```

**Step 2 — Data Freshness Audit (MANDATORY before closing actor):**

For every KPI collected across all passes, check whether the website or a more recent source has a newer value:

1. List all KPIs where the most recent data is from {current_year - 1} or older
2. Re-scrape the official website page most likely to host that KPI (use Pass 5.5/5.6 URLs)
3. If a newer figure exists: **replace** the older figure AND note both values with dates (e.g., "63% (2025) vs 43% (2024)")
4. If the website shows a figure without a year: treat as {current_year} but flag as "date non précisée sur le site"
5. If no newer figure found after re-scrape: keep existing data and note `[Vérifié {current_date} — pas de mise à jour publique trouvée]`

**Critical conflict rule:** When website data contradicts PDF report data, ALWAYS prefer the more recent source. If dates are the same, prefer the more specific/granular source. Document the conflict explicitly in `data_quality.notes`.

---

## Completeness Checklist (MANDATORY before marking actor as DONE)

After all passes, verify ALL items below. Each unchecked item is a blocker.

```
REPORTS & PDFS
□ Sustainability report PDF searched (brand-level, current AND prior year)
□ Group-level ESG report searched (if brand belongs to LVMH, Kering, Tapestry, etc.)

CERTIFICATIONS & FRAMEWORKS
□ Certification scores collected (B Corp, Fair Wear, GOTS, RWS, OEKO-TEX, SBTi, Good On You)
□ Framework participation checked (SBTi, SBTN/AR3T, Fashion Pact, ZDHC, CDP)

MATERIALS — 4 fiber types minimum
□ Total % preferred/certified materials found
□ Fiber-by-fiber breakdown extracted (cotton, wool, polyester, leather at minimum)
□ Certification split per fiber extracted (not just total %)
□ Materials sub-pages scraped: {actor_domain}/materials (or equivalent)

SUPPLY CHAIN — geographic depth required
□ Audit coverage % by tier (T1 mandatory, T2 if available)
□ Geographic audit breakdown extracted (% by country or region)
□ Grievance mechanism coverage checked
□ Supply chain sub-pages scraped: {actor_domain}/supply-chain or /transparency

SOCIAL & GOVERNANCE
□ D&I data searched (workforce %, management %, board %, EgaPro)
□ Living wage data searched (% suppliers, methodology, targets)
□ HRDD / vigilance plan existence checked

FRESHNESS
□ No KPI value is older than 12 months without a documented freshness check attempt
□ Multi-year KPIs formatted with explicit dates (e.g., "63% (2025) vs 43% (2024)")
□ All KPIs from Pass 7 freshness audit — older figures replaced where website shows newer data
□ Any conflict between website data and PDF report documented in data_quality.notes
□ Recent news (<12 months) searched for certifications, score updates, major announcements

SOURCE DIVERSITY
□ At least 1 official website sub-page scraped per topic category
□ At least 1 third-party certification platform checked

CLAIM INTEGRITY (Gate 1 — Verbatim Rule)
□ For each certification, label, or third-party attribution: verbatim quote from primary source verified — company audit ≠ tool methodology validation (e.g., "PwC reviews Carbonfact methodology" ≠ "AMI's BC audited by PwC")
□ Escalation verbs checked: "audité", "certifié", "validé" only used when source verbatim uses the same or stronger term — otherwise: "revue par", "méthodologie validée par", "en cours d'obtention"

CROSS-FILE CONSISTENCY (Gate 3)
□ All % figures and KPIs appear with the same value in dimensions content, a_retenir, insights, and any synthesis referencing this actor — flag any discrepancy before marking DONE
```

If any checklist item returns no data after 2+ search attempts:
- Mark as `[NON DOCUMENTÉ — recherché le {current_date}, non trouvé publiquement]`
- Note in `data_quality.notes` which passes returned empty results

---

## Source Citation Format

```markdown
**Sources RSE :**
- Rapport RSE 2024 (PDF, 87p) : https://example.com/sustainability-report-2024.pdf (téléchargé le {date})
- B Corp Profile : https://www.bcorporation.net/en-us/find-a-b-corp/company/example/ (consulté le {date})
- Fair Wear Brand Performance : https://www.fairwear.org/brands/example (consulté le {date})
- SBTi Dashboard : https://sciencebasedtargets.org/companies-taking-action#table (consulté le {date})
- Page D&I officielle : https://example.com/diversity-inclusion (scrapé le {date})
- LVMH DEU 2023 (PDF) : https://r.lvmh-static.com/uploads/2024/04/deu-2023.pdf (consulté le {date})
```

---

## Minimum Source Targets (RSE benchmark)

| Actor profile | Min. sources expected |
|---------------|----------------------|
| Brand with sustainability report | ≥ 25 sources |
| Brand without sustainability report | ≥ 15 sources |
| Brand in luxury group (LVMH, Kering) | ≥ 20 sources (brand + group combined) |

If source count is below minimum after all 7 passes: flag in `data_quality.notes` and attempt a second round of Passes 1-3 with alternative search terms.

---

## Reasoning triggers (injected as `{sector_reasoning_triggers}`)

Sector-level triggers for a sustainability or ESG assessment. They complement the method-level triggers already in the actor prompt; they do not replace them.

| What you discover | What it implies | What to do next |
|---|---|---|
| Actor belongs to a fashion or luxury group (LVMH, Kering, Inditex, PVH...) | Group ESG reports hold the deepest quantitative data | Run the group-level report searches immediately (PDF, ESG report, DEU) |
| Actor holds B Corp, Fair Wear or SBTi | The certification platform has scored data the website does not show | Scrape the platform profile directly (bcorporation.net, fairwear.org, sciencebasedtargets.org) |
| A sustainability report PDF exists | It holds most of the quantitative data, structured by section | Extract the table of contents first, then the relevant sections in full |
| A percentage is published without breakdown (e.g. "84% sustainable materials") | A fiber-by-fiber or category breakdown exists on a dedicated page | Scrape `/materials`, `/our-materials`, `/sourcing` |
| Audit coverage found for Tier 1 only | Geographic and Tier 2 detail may sit on a supplier page | Search `/supply-chain`, `/transparency`, `/traceability`, supplier lists |
| A framework claim appears (SBTi, Fashion Pact, SBTN, ZDHC, CDP) | The framework platform holds the real commitment level | Cross-check on the framework's own platform |
