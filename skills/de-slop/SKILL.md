---
name: de-slop
description: >
  Quality gate for AI output before it ships, adapted for consulting deliverables.
  Flags AI slop, false facts, off-voice writing, structural anti-patterns, and
  off-strategy claims in a single scorecard table. Detects and suggests only;
  never edits or rewrites unless explicitly asked ("fix it" / "applique" / "corrige").
  Use when the user says "de-slop", "de-slop this", "check this before it ships",
  "is this good to send", "run de-slop", "slop check", "relis ce texte",
  "ca fait trop IA", "humanise ca", "stop slop", "clean this up", "remove AI tells",
  "does this sound human", "edit this email", "relecture redactionnelle",
  "rends ca plus naturel", "c'est trop corporate", "ca sonne genere", or has
  produced an email, post, deck, reply, proposal, exec summary, or doc and wants
  it checked first. Also trigger when the user pastes text and says "mieux" or
  "ameliore". Even without an explicit trigger, apply this skill when Claude
  produces prose destined for a client or external publication.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# De-Slop

The quality gate for AI output in a consulting practice. Run it on any finished output before it goes out and it checks against two standards:

1. **Universal Slop Check** (AI writing tells, structural anti-patterns, made-up facts, contradictions, leftover junk, unreadable writing)
2. **Company Slop Check** (voice, visual brand, strategy and facts, whether it did the job it was asked to do)

It renders one scorecard table: every fired check, what is off, the source standard, and a suggestion. It detects and suggests. **It never edits, rewrites, or applies fixes to the output** unless the user explicitly asks (see Step G). The human (or another skill) owns the actual edit.

This is a scope guardrail about *ownership of the fix, not the size of the suggestion.* The skill can and should flag big, fundamental problems and suggest large changes when something is deeply wrong. It just never makes the change itself (unless Step G is triggered).

It never invents problems, and a clean pass is a normal result. Each check has its own standard file. Load a check's file only when that check fires. Do not preload everything.

---

## Quick checklist (fast review shortcut)

For a fast review without the full scorecard procedure, apply this checklist directly:

- Adverbes en -ment or "really/just/truly"? Kill them.
- Passive voice? Find the actor, make them the subject.
- Inanimate thing + human verb ("the data suggests")? Name the person.
- Sentence starting with "Voici" / "Here's" / "Il convient de"? Cut to the point.
- "Not X, but Y" contrast? State Y directly.
- Three consecutive sentences of the same length? Break one.
- Paragraph ending with a punchy one-liner? Vary it.
- Em dash anywhere? Remove it.
- Vague declarative ("Les implications sont significatives")? Name the implication.
- Distant narrator voice ("Les organisations qui...")? Put the reader in the scene.
- Meta-joiner ("Dans cette section, nous allons...")? Delete.
- Bullet = bold noun + colon + sentence? Rewrite as an action sentence.

For a thorough review, run the full procedure below.

---

## Inputs

The output to check (in the chat, or a file or folder path). If it was pasted with no context, ask only what you cannot infer: is it external or internal, and roughly what is it. Otherwise infer and print your read at the top so a wrong assumption is visible.

## Procedure

1. Classify the output (Step A).
2. Decide which checks fire (Step B).
3. Grade the fired checks in bundles of three, at most three subagents running at once, each on Sonnet (Step C). The orchestrator does not grade.
4. Collect the results and set the verdict (Step D).
5. Render the verdict title + scorecard table, in the locked format (Step E). Do not rewrite the output.
6. Append the run to `Intelligence/de-slop-log.md` (Step F).
7. If the user asks, apply mechanical fixes only (Step G).

## Step A. Classify

- Modality: copy, visual, or both. Copy is any words meant to be read. Visual is any designed surface (thumbnail, slide, deck, image, the look of a page).
- Audience: external, internal, or personal.
- Language: FR, EN, or mixed. Determines whether FR-specific checks fire.
- Context profile: pick the one file in `references/contexts/` that matches the output (consulting, marketing, support, sales, and more over time). If none matches, note it and skip the profile.

## Step B. Which checks fire

Each check reads its own file. A check that does not fire is marked skipped with the reason, never passed.

Universal Slop Check (no company setup, runs on any copy):

| Check | Fires when | File |
|---|---|---|
| AI writing tells | copy present | `references/checks/ai-writing.md` |
| AI writing tells (FR) | copy present AND language is FR or mixed | `references/checks/ai-writing-fr.md` (loaded alongside `ai-writing.md`) |
| Structural tells | copy present | `references/checks/structural-tells.md` |
| Factual accuracy | any factual claim present | `references/checks/factual-accuracy.md` |
| Consistency | always | `references/checks/consistency.md` |
| Artifacts | always | `references/checks/artifacts.md` |
| Readability | copy or doc | `references/checks/readability.md` |

Company Slop Check:

| Check | Fires when | File |
|---|---|---|
| Voice | copy present | `references/checks/voice.md` plus the matching `contexts/` profile |
| Visual | visual present | `references/checks/visual.md` |
| Company fit | always | `references/checks/company-fit.md` |
| Completeness | only if a clear ask is in the context | no file, grade against the ask itself |

## Step C. Grade the fired checks in bundles of three

Group the fired checks into bundles of up to three, in the order they appear in Step B. Spawn one subagent per bundle with the Task tool, **at most three subagents running at once** (a fourth bundle waits for a slot), **each on the Sonnet model** (this is review, not generation). The orchestrator never grades.

Each subagent grades its three checks independently: it reads each check's own standard file and judges that check on its own, never letting one check's verdict color another. Per-check isolation is the point. It stops any single pass from rationalizing the output as fine.

When both `ai-writing.md` and `ai-writing-fr.md` fire, they count as a single check ("AI writing tells") and go to the same subagent. The subagent loads both files and produces one combined grade.

```
You grade exactly these checks, independently, one at a time: <CHECK 1>, <CHECK 2>, <CHECK 3>.
For each, read ONLY its standard file (and the matching references/contexts/ profile if that check says to), then grade that check alone. Do not blend checks. Do not check anything outside your assigned three.

Standard files:
- <CHECK 1>: <FILE 1>
- <CHECK 2>: <FILE 2>
- <CHECK 3>: <FILE 3>

Output under review:
<the exact output, or the file path / image to read>
The ask (only if Completeness is one of your checks):
<the request the output must satisfy, or "none provided">

For each of your three checks, return:
- check:  <name>
- status: Aligned, Drift, Misaligned, or Skipped (with a reason)
- source: the specific governing doc, not a generic tag (e.g. brand.md / voice.md for Voice; organization.md / strategy.md / icp.md for Company fit; the standard name for universal checks; "the ask" for Completeness)
- findings: for every Drift or Misaligned, a block with:
    Quote:  the exact span from the output, or the located visual element
    Breaks: the rule it breaks, quoted from the standard file
    Suggestion: for the MECHANICAL checks (AI writing tells, Artifacts, Readability, Structural tells) quote the exact offending span so the user sees precisely what to touch. For the JUDGMENT checks (Factual accuracy, Consistency, Voice, Company fit, Completeness, Visual) give generic, awareness-level advice on the kind of problem. Never a full rewrite of the output.
    Severity: blocker, should-fix, or polish
```

## Step D. Severity and the verdict

Severity per finding:

- blocker: off-strategy, a false claim about the company, a hard guardrail break in outward copy, or the output failing the job it was asked to do.
- should-fix: real, fixable, not fundamental.
- polish: cosmetic, optional.

Set one verdict, which becomes the big title in Step E:

- `# Good to go` -- every fired check Aligned, or only polish findings.
- `# Good to go, with a few things you might want to fix` -- real drift or should-fix findings, nothing fundamentally off (no blocker).
- `# Not ready` -- any blocker.

A per-row status maps the same way: Good to go (Aligned / polish), Might wanna fix (drift / should-fix), Not ready (blocker).

## Step E. Render the verdict and scorecard

Render in the locked format defined in `references/output-format.md`. Read that file and match it exactly. The shape:

1. The big verdict title (`#` heading), one of the three states from Step D.
2. One short line summarizing the situation (optional on a fully clean run).
3. One table, every fired check shown (greens included), columns in this order: **Check, Status, What's off, Source, Suggestion**.

```
# <verdict title>

<one short summary line>

| Check | Status | What's off | Source | Suggestion |
|-------|--------|-----------|--------|-----------|
| <name> | <status + words> | <short, or -- if green> | <specific governing doc> | <suggestion, or -- if green> |
| ... |
```

Rules for the render:

- **Source** names the specific governing doc, not a generic tag (see the mapping in `references/output-format.md`).
- **Suggestion** is tiered: the mechanical checks (AI writing tells, Artifacts, Readability, Structural tells) quote the exact offending span; the judgment checks give generic awareness-level advice. Never a rewrite.
- Show every fired check as its own row, greens included, with `--` in What's off / Suggestion.
- No header box, no "improved version," no numbered "suggested changes" list, no apply prompt. The skill never edits or rewrites the output (unless Step G is triggered).
- A suggestion can be large when the problem is fundamental. The limit is that the skill never makes the change, not that the change must be small.

## Step F. Log the run

Append one entry to `Intelligence/de-slop-log.md`: date, person (from the active profile), what the output was, the verdict, and each finding (check, source, severity). One line of context plus the findings. Do not paste the whole output.

## Step G. Apply fixes (optional)

Triggered only when the user explicitly asks: "fix it", "applique", "corrige", "corrige le texte", or any clear request to apply corrections.

When triggered:

1. Apply corrections for **mechanical checks only**: AI writing tells, AI writing tells (FR), Structural tells, Artifacts, Readability. These have objectively right fixes.
2. **Do not touch** judgment checks: Voice, Company fit, Factual accuracy, Consistency, Completeness, Visual. These require human judgment.
3. Deliver the corrected text directly.
4. After the corrected text, add one summary line: "Corrections: X adverbes supprimes, Y passifs reformules, Z artefacts retires." (adapt to what was actually fixed, in the language of the output).
5. Preserve meaning. This step removes style markers, not ideas.
6. Respect the source language. FR text gets FR corrections. EN text gets EN corrections.

## Hard rules

- Every finding rests on an exact quote and the rule it breaks. No vibes. "Feels off" is not a finding.
- **The skill detects and suggests. It never edits, rewrites, or applies fixes to the output** unless Step G is explicitly triggered by the user. It produces a scorecard and suggestions; the human (or another skill) owns the edit. This is the core scope guardrail.
- The scope limit is on *ownership of the fix, not the size of the suggestion.* Flag big, fundamental problems and suggest large changes when warranted. Just never make the change (unless Step G).
- Render in the locked format in `references/output-format.md`: a big verdict title, then one scorecard table. No improved version, no suggested-changes list, no apply prompt.
- Source always names the specific governing doc, not a generic tag.
- Never invent findings to look thorough. Good to go is a real, common, correct result.
- If a check's file will not load, mark that check Skipped with the reason. A silent pass is a lie.
- No em dashes anywhere you write.
- Respect the source language of the output under review.

## Where the standard comes from

The Company Slop Check files (`voice.md`, `visual.md`, `company-fit.md`, and the `contexts/` profiles) are generated from the company's Context docs by the companion adapter skill. They are static. Re-run the adapter to refresh them. Each carries a `last-refreshed` date. The Universal Slop Check files are universal and do not depend on the company.

Adapted from de-slop by Hardik Pandya (hvpandya.com) and stop-ai-slop, both MIT License.
