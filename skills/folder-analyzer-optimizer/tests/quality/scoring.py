"""Scoring functions for the quality validation harness."""
from __future__ import annotations

CITATION_EXACT = "exact"
CITATION_ADJACENT = "adjacent"
CITATION_WRONG = "wrong"

FACT_CORRECT = "correct"
FACT_PARTIAL = "partial"
FACT_WRONG = "wrong"


def score_citation(cited: list[int], truth: list[int], tolerance: int = 2) -> str:
    """Return CITATION_EXACT / CITATION_ADJACENT / CITATION_WRONG.

    Rule: best score across all cited pages vs all truth pages.
    """
    if not cited or not truth:
        return CITATION_WRONG
    best = CITATION_WRONG
    for c in cited:
        for t in truth:
            if c == t:
                return CITATION_EXACT
            if abs(c - t) <= tolerance and best == CITATION_WRONG:
                best = CITATION_ADJACENT
    return best


def score_factual_accuracy(answer: str, evidence_phrases: list[str]) -> str:
    """Heuristic: count evidence phrases that appear in answer (case-insensitive).

    All present -> CORRECT
    Some present -> PARTIAL
    None present -> WRONG
    """
    if not evidence_phrases:
        return FACT_WRONG
    a = answer.lower()
    hits = sum(1 for ev in evidence_phrases if ev.lower() in a)
    if hits == len(evidence_phrases):
        return FACT_CORRECT
    if hits > 0:
        return FACT_PARTIAL
    return FACT_WRONG


def aggregate_run(rows: list[dict]) -> dict:
    """Compute summary stats over a list of per-question result dicts."""
    n = len(rows)
    if n == 0:
        return {"n": 0}
    return {
        "n": n,
        "fact_correct":      sum(1 for r in rows if r["factual"] == FACT_CORRECT),
        "fact_partial":      sum(1 for r in rows if r["factual"] == FACT_PARTIAL),
        "fact_wrong":        sum(1 for r in rows if r["factual"] == FACT_WRONG),
        "citation_exact":    sum(1 for r in rows if r["citation"] == CITATION_EXACT),
        "citation_adjacent": sum(1 for r in rows if r["citation"] == CITATION_ADJACENT),
        "citation_wrong":    sum(1 for r in rows if r["citation"] == CITATION_WRONG),
        "mean_tokens":       sum(r["tokens"] for r in rows) / n,
        "mean_latency_ms":   sum(r["latency_ms"] for r in rows) / n,
    }
