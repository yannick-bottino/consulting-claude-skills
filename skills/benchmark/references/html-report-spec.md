# HTML Report Spec (Phase 5)

Operational reference. Read before generating `outputs/{mission-slug}/benchmark-report.html`.

## Contents
1. Preconditions
2. Report structure
3. Competitive radar
4. Design system
5. Screenshots
6. Anti-placeholder rules
7. Validation

---

## 1. Preconditions

- Single source of data: `benchmark.json`. Inline it into a JS constant `BENCHMARK_DATA`. No figure may exist in the HTML that is absent from `benchmark.json`.
- One documented exception, and it is an arbitration, not a licence: **for screenshots, `actors/screenshots/capture-manifest.json` overrides `benchmark.json`.** The manifest is written by the capture script, `benchmark.json` holds a copy that goes stale on any recapture. When they disagree, the manifest wins, and the disagreement is itself a defect to report: regenerate the copy per `references/capture-spec.md` section 6.
- Resolve visual identity through `references/branding.md` before writing any CSS. Declare the token contract on `:root` and reference tokens only, never literal colours or font names.
- Self-contained file: inline CSS and JS, no external request. A web font is allowed only if the brand source provides an embeddable base64 font; otherwise use the `--font-title` / `--font-body` stacks.
- Every section is driven by a `benchmark.json` key. If the key is absent, hide the section silently. Never render an empty section.

---

## 2. Report structure

| # | Section | Data source | Content |
|---|---------|-------------|---------|
| 1 | Hero | `mission`, `scope`, scorecard | Logo (if resolved), mission title, date, 3 to 4 KPI counters, plus a one-line strategic takeaway (conclusion-first, the key message for the client) |
| 2 | Scope | `scope`, `dimensions` | Segment spectrum of the market, dimension framework, actors analysed, plus a normalised key-figures table (one row per actor, columns from the `key_figures` fields actually populated) |
| 3 | Market landscape | `market_landscape` | CSS grid: segment columns x category rows, actor names as category-coloured badges, focus column outlined |
| 4 | Executive summary | `key_insights`, `actors[]` | Client takeaway, positioning table, key facts. Add a client target column to any inclusion table, drawn with a dashed accent border to mark it as the intended position, not observed data. Each key fact ends with an italic accent-coloured implication line for the client |
| 5 | Competitive radar | `roue_concurrentielle` | SVG radar (section 3 below), market standards as badges, positive and negative differentiator tables |
| 6 | Per-actor benchmark | `actors[]` | One card per actor: link to the official site, one tab per dimension, quote as blockquote, "À retenir" call-out, positive and negative insights in a two-column grid |
| 7 | Comparison synthesis | `pricing_matrix` for `offer`, the profile's equivalent otherwise | Comparison table, degressivity bars, transparency dots, key observations |
| 8 | Targets and population | `targets-analysis.md` | CSS funnel (trapezoid bars via `clip-path`, conversion rate between steps), plus a collapsible sources table (Step, Value, Source, Hypothesis) documenting every step |
| 9 | Recommendation | `recommendation` | Three columns Standard / Singularité / Unicité, risk table (Risk, Probability, Impact, Mitigation), comparison table with a methodological disclaimer where client values are estimates, 3-horizon roadmap |
| 10 | Sources | `actors[].sources`, `data_quality` | Per-actor collapsible source lists, methodological note, data-quality statement |

Sections 7 and 8 are conditional on the mission deliverables. Tab labels, table headers, and axis labels come from `dimensions[].label` and `scope`, never from a hardcoded sector vocabulary.

H2 headings are action titles (conclusion-first), not descriptive labels. Prefix each with its section number in accent-coloured small caps.

---

## 3. Competitive radar

Pure inline SVG, `viewBox 520x460`, no external library.

**Axes.** Derive them from the mission: one axis per dimension in `mission-config.json → dimensions` (3 to 6 axes). Add a cross-cutting axis only if it is backed by a populated field across all actors (typical candidates: price transparency, digital maturity, coverage). Never ship a fixed axis list.

**Scoring, panel-relative.** For each axis, score 1 to 5 against the panel itself, not an absolute scale:
- 5 = best observed in the panel on this axis
- 1 = worst observed in the panel
- intermediate actors are placed on the observed spread

Write the resulting rubric into the report as a collapsible `<details>` grid under the radar: one row per axis with the criterion used and the anchors chosen for 5 and 1. A radar with no visible rubric is not auditable and must not ship.

An actor with no data on an axis gets no point on that axis and is noted in the rubric. Do not impute a middle score.

**Geometry.**
- Hexagonal or n-gonal grid, levels 1 to 5, 36px per level, centre at 0,0
- `x = S * 36 * cos(angle)`, `y = S * 36 * sin(angle)`, axes evenly spaced over 360 degrees
- One polygon per actor: stroke plus 10% fill, one colour per actor, consistent across the whole report
- Interactive legend: hovering an actor highlights its polygon and drops the others to 8% opacity (`highlightActor` / `resetActors`)

---

## 4. Design system

Target: the visual quality of a top-tier strategy consulting digital deliverable. The following are mandatory.

**Typography**
- `--font-title` for headings, `--font-body` for text
- H1 2.75rem/600, H2 1.75rem/600, H3 1.2rem/600, body 1rem/400
- Section numbers in `--accent`, small caps, before each H2

**Tables (dark header)**
- Header: `background: var(--header-bg); color: var(--header-text)`
- Cell padding `12px 16px`, border `1px solid var(--border)`
- Row hover `var(--accent-soft)`
- No alternating stripes: cleaner with a dark header

**Cards**
- `border-radius: 14px`, `padding: 28px`, `border: 1px solid var(--border)`
- Hover: accent border plus `box-shadow: 0 8px 24px rgba(0,0,0,0.08)`
- `transition: all 0.25s ease`

**Inclusion indicators**
- Harvey balls in CSS (`conic-gradient`), never emoji, in any inclusion or coverage table
- Full = `--positive` filled, half = `--positive` half, option = `--warning` half, none = empty circle with `--border`

**Hero**
- Full-width gradient built from `--accent`
- 3 to 4 KPI counters (figure plus label)

**Micro-animations**
- Cards: fade-up via IntersectionObserver (opacity 0 to 1, translateY 24px to 0, 0.6s ease)
- Bars: `@keyframes barGrow` from width 0 to target, staggered `100ms + i*120ms`
- Scroll-to-top: `transform: scale(1.1)` on hover

**Spacing**
- Section padding `4.5rem 3.5rem`, card margin-bottom `1.5rem`
- Section separator `border-top: 1px solid var(--surface)`

**Responsive and print**
- Sidebar collapses under 1024px, two-column grids stack under 1024px, type scale reduced under 600px
- Print styles: hide sidebar, remove shadows

**Components**
- Fixed sidebar with per-section navigation and scrollspy (IntersectionObserver), section numbers matching the H2s
- One filter tab per dimension inside each actor card
- Animated comparison bars, transparency dots (14px, filled vs empty)
- Scroll-to-top button

---

## 5. Screenshots

Source of truth: `actors/screenshots/capture-manifest.json`. Read `references/capture-spec.md` before wiring this section.

- Inline the **web derivative** (`path_web`) as base64, never the original PNG. Originals stay on disk for deck production.
- Entries with status `ok` are displayed in a browser chrome frame (grey bar, three dots, URL, image). Entries with status `blocked` or `failed` are not displayed at all, and the actor card falls back to a discreet link: `<a href="URL" target="_blank">Voir le site officiel →</a>`.
- Order shots by evidence value inside an actor card: `pricing`, then `offer`, then the rest.
- A screenshot carrying a `claim` is displayed next to that claim, not in a gallery at the end. Evidence sits with the assertion it supports.
- The caption bar is already stamped into the derivative. Do not overlay a second caption, and never crop it out.
- Blocked captures are listed in the sources section with their reason, in one line per actor. Silence about a blocked competitor reads as an omission.

## 6. Anti-placeholder rules

- No screenshot: discreet link only. Never an empty frame.
- No logo resolved: no logo block at all.
- No data for a section: section hidden.

An empty visual block wastes space and weakens the report. Absence of data is stated in the sources section, never staged in the layout.

---

## 7. Validation

Before delivery, check each item:

- [ ] Opens in a browser with no console error
- [ ] Every section listed in section 2 whose data exists in `benchmark.json` is present and navigable from the sidebar
- [ ] Every section whose data is absent is hidden, with no empty residue
- [ ] Actor cards render, dimension tabs switch
- [ ] Comparison table highlights the extreme value
- [ ] Radar shows one polygon per actor with data, and the scoring rubric is visible
- [ ] Responsive behaviour holds (sidebar hidden, layout stacked on mobile)
- [ ] Sources are reachable and links clickable
- [ ] No figure in the report is absent from `benchmark.json`
- [ ] No placeholder, no empty frame, no fabricated value
- [ ] Visual identity resolved through `references/branding.md`, no literal colour or font in the CSS outside the `:root` token block
