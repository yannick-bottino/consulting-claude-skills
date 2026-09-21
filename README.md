# Consulting Claude Skills

Client-agnostic [Claude Code](https://claude.com/claude-code) skills for management consulting work: competitive benchmarks, deep research, project memory, deliverable quality control, and prompt engineering.

These skills were built and used on real consulting engagements, then stripped of every firm and client reference so they run anywhere. No brand charter, no hardcoded client, no house methodology you have to adopt wholesale.

Languages: skills are a mix of English and French, matching the working language of the task they automate.

## Install

As a plugin (recommended, auto-updating and namespaced):

```
/plugin marketplace add yannick-bottino/consulting-claude-skills
/plugin install consulting-skills@consulting-claude-skills
```

Or copy individual skills:

```bash
git clone https://github.com/yannick-bottino/consulting-claude-skills.git
cp -r consulting-claude-skills/skills/benchmark ~/.claude/skills/
```

## Skills

### Research and analysis

| Skill | What it does |
|---|---|
| `benchmark` | Full competitive benchmark pipeline: scoping, actor research, live scraping and screenshot capture, sourced scorecard, PPT-ready output. Two axes drive it, `benchmark_nature` (offer / maturity / generic) and `sector`. |
| `deep-research` | Multi-source research report with citation tracking and evidence persistence. For literature reviews, market analyses, due diligence, policy briefs. |
| `fact-checker` | Systematic fact verification against evidence, with an explicit confidence verdict per claim. |
| `folder-analyzer-optimizer` | Turns a heterogeneous document folder (PDF, DOCX, PPTX, XLSX) into a navigable Markdown knowledge base. |

### Deliverable quality

| Skill | What it does |
|---|---|
| `de-slop` | Quality gate for AI output before it ships. Catches AI writing tells in FR and EN, plus consulting-specific ones. |
| `humanize-output` | Applies anti-AI-pattern rewrites to de-roboticise any LLM-produced text. |
| `deliverable-panel-review` | Multi-perspective critical review of a consulting deliverable. |
| `file-naming-standard` | Enforces a `<Client> x <Firm>_<Mission> - <Deliverable>_YYYYMMDD.<ext>` convention just before delivery. Firm name is configurable. |
| `meeting-summary` | Turns a raw meeting transcript into a structured, professional write-up. |

### Project memory and governance

| Skill | What it does |
|---|---|
| `project-init` | Initialises (or resumes) a shared persistent project memory: session pilot `CLAUDE.md`, task tracker, memory substrate. |
| `project-memory` | The engine behind it: a 3-layer memory substrate (Cold decisions / Warm syntheses / Hot logs) so human decisions are never overwritten by a regeneration. |
| `project-lint` | Audits an existing project folder against those conventions. |
| `session-handoff` | Starts a clean session carrying only the context the next task needs, instead of `/compact`. |
| `instructions-audit` | Audits and refactors a bloated project `CLAUDE.md`. |

### Thinking and tooling

| Skill | What it does |
|---|---|
| `process-interviewer` | Interrogates you until the plan in your head is complete and unambiguous, before any building starts. |
| `decision-toolkit` | Generates decision-making tools: step-by-step guides, bias checkers, scenario explorers, interactive dashboards. |
| `prompt-optimizer` | Analyses and rewrites prompts, teaching the framework rather than just shipping the prompt. |
| `personal-insights` | Cognitive diagnostic of how you actually use Claude: delegation patterns, blind spots, atrophy risks. |
| `skill-creator` | Reverse-engineers a skill from a task you just finished. |

## Configuration

Two skills expect one value of your own:

- **`file-naming-standard`** — set your firm name via the `FIRM_NAME` environment variable, the `--firm` flag, or a `Cabinet : <name>` line in the project `CLAUDE.md`. Defaults to `Firm`.
- **`project-memory`** — `skills/project-memory/references/config.example.md` holds the decision domains, milestones, `context.md` schema and log retention policy. Edit it in place; `project-init` proposes adjustments at init.

`benchmark` ships no brand charter by design: visual identity is resolved per mission through `references/branding.md`, from an external brand skill, a token file, or a neutral fallback.

## Anonymisation

Every firm name, client name and engagement reference has been removed. Example actors in the evals and reference docs (Velora, Carvio, Sharego, Banque Solaris, Mutualis, TransRail…) are fictional. Public methodology references, such as looking up a group-level ESG report for a brand owned by LVMH or Kering, are kept because they are public method, not client data.

## License

MIT. `de-slop` adapts prior work by Hardik Pandya (hvpandya.com), also MIT.
