"""Tests for the quality scoring module."""
import pytest
from scoring import (
    score_citation,
    score_factual_accuracy,
    aggregate_run,
    CITATION_EXACT,
    CITATION_ADJACENT,
    CITATION_WRONG,
    FACT_CORRECT,
    FACT_PARTIAL,
    FACT_WRONG,
)


def test_citation_exact_match():
    assert score_citation(cited=[15], truth=[15]) == CITATION_EXACT


def test_citation_exact_multi_truth():
    assert score_citation(cited=[18], truth=[15, 17, 18]) == CITATION_EXACT


def test_citation_adjacent_within_2():
    assert score_citation(cited=[17], truth=[15]) == CITATION_ADJACENT
    assert score_citation(cited=[13], truth=[15]) == CITATION_ADJACENT


def test_citation_wrong_far():
    assert score_citation(cited=[100], truth=[15]) == CITATION_WRONG


def test_citation_empty_is_wrong():
    assert score_citation(cited=[], truth=[15]) == CITATION_WRONG


def test_citation_best_of_multiple_cited():
    assert score_citation(cited=[100, 17], truth=[15]) == CITATION_ADJACENT
    assert score_citation(cited=[100, 15], truth=[15]) == CITATION_EXACT


def test_factual_correct_when_all_evidence_in_answer():
    answer = "TargetCo generates EUR 500 million in revenue with 8% growth."
    evidence = ["EUR 500 million", "8% growth"]
    assert score_factual_accuracy(answer, evidence) == FACT_CORRECT


def test_factual_partial_when_some_evidence_in_answer():
    answer = "TargetCo generates EUR 500 million in revenue."
    evidence = ["EUR 500 million", "8% growth"]
    assert score_factual_accuracy(answer, evidence) == FACT_PARTIAL


def test_factual_wrong_when_no_evidence_in_answer():
    answer = "The company is in distress."
    evidence = ["EUR 500 million", "8% growth"]
    assert score_factual_accuracy(answer, evidence) == FACT_WRONG


def test_factual_case_insensitive():
    answer = "Revenue is EUR 500 MILLION."
    evidence = ["EUR 500 million"]
    assert score_factual_accuracy(answer, evidence) == FACT_CORRECT


def test_aggregate_run_counts_per_score():
    rows = [
        {"factual": FACT_CORRECT, "citation": CITATION_EXACT, "tokens": 1000, "latency_ms": 2000},
        {"factual": FACT_PARTIAL, "citation": CITATION_ADJACENT, "tokens": 1500, "latency_ms": 2500},
        {"factual": FACT_WRONG,   "citation": CITATION_WRONG,    "tokens": 800,  "latency_ms": 1800},
    ]
    agg = aggregate_run(rows)
    assert agg["n"] == 3
    assert agg["fact_correct"] == 1
    assert agg["fact_partial"] == 1
    assert agg["fact_wrong"] == 1
    assert agg["citation_exact"] == 1
    assert agg["citation_adjacent"] == 1
    assert agg["citation_wrong"] == 1
    assert agg["mean_tokens"] == pytest.approx(1100.0)
    assert agg["mean_latency_ms"] == pytest.approx(2100.0)
