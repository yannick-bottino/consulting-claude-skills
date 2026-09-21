# Run battery protocol

## Inputs

- `evals/evals.json` (9 questions)
- `_fixtures/TARGETCO.md`
- `_fixtures/TARGETCO.tree.json`
- `_fixtures/_index_plain.md`
- `_fixtures/_index_with_tree.md`
- `baseline_prompt.md`
- `treatment_prompt.md`

## Output (per run)

One file per subagent run: `results/{QID}-{CONDITION}.json`

```json
{
  "qid": "Q1",
  "condition": "baseline" | "treatment",
  "persona": "sector_analyst",
  "question": "...",
  "subagent_response": {
    "answer": "...",
    "citations": [15],
    "confidence": "high",
    "reasoning": "..."
  },
  "tokens": 4500,
  "latency_ms": 3200
}
```

## Dispatch loop

For each `q` in question_pool.questions × each `condition` in ("baseline", "treatment"):
1. Pick template
2. Substitute {{PERSONA_LABEL}}, {{QUESTION_TEXT}}, {{MD_PATH}}, {{INDEX_PATH}}, {{TREE_PATH}}
3. Dispatch via Agent tool (general-purpose, sonnet, foreground)
4. Persist results/{qid}-{condition}.json

## Parallelization

Dispatch all 18 in one message with parallel Agent calls.

## After all 18 complete

Run aggregate.py → QUALITY-REPORT.md.
