# De-Slop output format (canonical)

Every run renders in this exact shape. Do not deviate. The skill detects and suggests. It never rewrites or edits the output (unless Step G is explicitly triggered).

## Shape

1. **A big verdict title** (`#` heading) so the user knows the result at a glance. One of three states:
   - `# Good to go` -- all fired checks green.
   - `# Good to go, with a few things you might want to fix` -- only drift, no blockers.
   - `# Not ready` -- any blocker / hard cross.
2. **One short line** under the title summarizing the situation. On a fully clean run, this line is optional.
3. **One table, every fired check shown** (greens included), columns in this order:

| Column | What goes in it |
|--------|-----------------|
| Check | The check name. |
| Status | Words: Good to go / Might wanna fix / Not ready. |
| What's off | Short and plain. `--` if the row is green. |
| Source | The specific governing doc, not a generic tag (see mapping below). |
| Suggestion | Generic, awareness-level advice for the judgment checks. For the mechanical checks, quote the exact offending span. `--` if green. |

Nothing else. No header box, no "improved version," no "suggested changes" list, no apply prompt.

## Source column mapping

Name the real standard, not a generic label.

| Check | Source shown |
|-------|--------------|
| AI writing tells | Signs of AI writing (humanizer standard) |
| AI writing tells (FR) | Marqueurs IA francophones |
| Structural tells | Structural anti-patterns standard |
| Factual accuracy | World-truth / fact-checker |
| Consistency | Internal coherence |
| Artifacts | Universal slop standard |
| Readability | Universal readability standard |
| Voice | `brand.md` / `voice.md` |
| Company fit | `organization.md` / `strategy.md` / `icp.md` |
| Completeness | The ask |
| Visual | `visual.md` (design system) |

## Suggestion column: two tiers

- **Mechanical checks** (AI writing tells, AI writing tells (FR), Structural tells, Artifacts, Readability) -- quote the exact offending span so the user sees precisely what to touch. e.g. for Readability, put the actual run-on sentence in the cell.
- **Judgment checks** (Factual accuracy, Consistency, Voice, Company fit, Completeness, Visual) -- generic, awareness-level advice. Point at the kind of problem, not a line-edit.

## Canonical example (copy, external, consulting)

This is the reference render. Match its tone and density.

```
# Good to go, with a few things you might want to fix

No blockers. Voice is on and nothing's false about the company. The drift is structural patterns and a few FR tells.

| Check | Status | What's off | Source | Suggestion |
|-------|--------|-----------|--------|-----------|
| AI writing tells | Good to go | Clean. No tells, no em dashes. | Signs of AI writing | -- |
| AI writing tells (FR) | Might wanna fix | Two consulting jargon terms, one opener. | Marqueurs IA francophones | "Naviguer les defis" -> "gerer les defis". "Voici ce que nous proposons" -> cut, start with the proposal. |
| Structural tells | Might wanna fix | One binary contrast, two formulaic bullets. | Structural anti-patterns standard | "Ce n'est pas un probleme de budget. C'est un probleme de priorites." -> state the priority issue directly. Bullets: remove bold labels. |
| Factual accuracy | Good to go | All claims check out. | World-truth / fact-checker | -- |
| Consistency | Good to go | No contradictions. | Internal coherence | -- |
| Artifacts | Good to go | Nothing stray. | Universal slop standard | -- |
| Readability | Might wanna fix | One run-on sentence. | Universal readability standard | Split: "La transformation digitale necessite une refonte des processus operationnels qui s'appuie sur une gouvernance renouvelee et des indicateurs de performance adaptes aux nouveaux enjeux." |
| Voice | Good to go | On register for consulting. | brand.md / voice.md | -- |
| Company fit | Good to go | On-strategy, no retired offers. | organization.md / strategy.md / icp.md | -- |
```

## Mode fix output format (Step G)

When the user triggers Step G ("fix it", "applique", "corrige"), the output is different:

1. **The corrected text** -- delivered directly, with mechanical fixes applied. No scorecard table, no side-by-side. Just the clean text.
2. **One summary line after the text** -- listing what was changed. Format: "Corrections: [count and type of fixes applied]." In the language of the output.

Example:
```
[The full corrected text here]

Corrections: 3 adverbes supprimes, 2 passifs reformules, 1 contraste binaire brise, 1 opener coupe.
```

Rules for mode fix:
- Only mechanical checks get applied: AI writing tells, AI writing tells (FR), Structural tells, Artifacts, Readability.
- Judgment checks (Voice, Company fit, Factual accuracy, Consistency, Completeness, Visual) are never applied. If they had findings in the scorecard, mention them in a second line: "Non corrige (jugement humain requis): [list the judgment findings]."
- Preserve meaning. Remove style markers, not ideas.
- Respect the source language.

## Rules baked into the format

- The skill flags and suggests. It never edits, rewrites, or applies (unless Step G is explicitly triggered by the user).
- A suggestion can be large when something is fundamentally wrong. The scope limit is on ownership of the fix, not the size of the suggestion.
- A clean `# Good to go` run is normal: the title and the all-green table, no caveat line needed.
- No em dashes anywhere.
