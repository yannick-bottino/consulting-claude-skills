# Replanning Loop (P2 Gate)

The single feature that separates a real deep-research harness from static RAG: the lead agent decides what to search NEXT based on what it just READ, instead of executing a frozen plan. This file defines that loop.

**Core principle:** Research is OODA (Observe-Orient-Decide-Act), not a checklist. The initial decomposition in P1 is a set of HYPOTHESES, not a contract. You revise it every round.

## The loop

```
P1 produces initial sub-questions (hypotheses)
        |
        v
  ┌─> DISPATCH round N: subagents search broad → READ full pages → write notes to disk
  │         |
  │         v
  │   REPLAN GATE: lead reads the round's notes and writes a knowledge-state block (below)
  │         |
  │         v
  │   Decide: coverage sufficient OR budget exhausted?
  │     │                              │
  │     │ no (gaps remain + budget left)│ yes
  │     │                              │
  └─ issue DELTA-QUERIES ──────────────┘
            (targeted follow-ups for the gaps only)        → exit loop, go to P3
```

## The knowledge-state block (write this at every gate, to disk)

After each dispatch round, the lead agent appends to `research-notes/_knowledge_state.md`:

```
## Round {N} — knowledge state ({timestamp})
KNOW (established, ≥2 sources or 1 official):
- {claim} [task-x]
- ...

THINK (single-source / weak / contested — needs corroboration):
- {claim} [task-y] — why weak: {reason}

MISSING (gaps that block the question):
- {gap} → next: {specific delta-query or "spawn subagent on Z"}

CONTRADICTIONS (sources disagree):
- {A says X [n]} vs {B says Y [m]} → next: {how to adjudicate}

DECISION: {continue → delta-queries listed in MISSING} | {stop → coverage sufficient} | {stop → budget exhausted, declare residual gaps}
```

This block is not bureaucracy. It forces the Orient step that static pipelines skip. If you cannot fill MISSING with anything specific and KNOW covers the question, you are done — stop, do not pad rounds to hit a number.

## Exit conditions (stop the loop when EITHER is true)

1. **Coverage sufficient** — every sub-question of the original query has ≥1 KNOW-level answer, no MISSING item blocks the conclusion, contradictions are either resolved or explicitly flagged for the report.
2. **Budget exhausted** — you hit the round/query ceiling for the effort tier (see `retrieval_tiers.md`). On budget-exit you MUST carry residual MISSING items into the report as stated limitations. Never hide a gap by stopping silently.

## Anti-patterns specific to the loop

- **Frozen plan** — running P1's tasks to completion and going straight to P3 without a single replan gate. This is the V6.1 failure mode. At least one gate is mandatory; complex topics need several.
- **Infinite curiosity** — spawning rounds because "more is better". The gate's DECISION must point to a SPECIFIC gap. No gap → stop.
- **Snippet satisficing** — declaring KNOW from a search snippet without a full-page read. A claim is only KNOW-eligible if a subagent actually read the source page.
- **Replanning without reading** — the lead writing the knowledge-state from search result titles instead of subagent notes. The gate runs on distilled notes, never on raw SERP.
- **Contrarian padding** — inventing MISSING items to justify another round. If the question is answered, answer it.

## Effort-tier defaults for the loop

| Effort | Initial sub-questions | Replan gates (min) | Query ceiling | Subagents/round |
|--------|----------------------|--------------------|---------------|-----------------|
| quick | 2-3 | 1 | ~10-15 | 1-2 |
| standard | 4-6 | 2 | ~25-40 | 3 |
| deep | 6-10 | 3+ | ~60-100 | 3-5 |

Ceilings are targets, not quotas. Hitting the ceiling forces a stop; reaching coverage early also forces a stop. Compute is the #1 driver of quality (it explains the bulk of performance variance in published harness evals), so do not under-spend on `deep` — but spend it through the gate, not as a blind query dump.
