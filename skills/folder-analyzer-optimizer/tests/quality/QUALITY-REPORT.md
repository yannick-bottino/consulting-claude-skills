# Tree Builder Quality Validation Report

**Target**: anonymized (Target Co.)  
**Source doc**: 437-page Strategic Vendor Due Diligence report  
**Questions**: 9 (3 sector analyst, 3 IC member, 3 buyer-DD; 3 easy / 3 medium / 3 hard)  
**Conditions**: baseline (.md + plain index) vs treatment (.md + .tree.json + enriched index)  
**Subagent model**: Claude Sonnet 4.6

---

## Aggregate scores

| Metric | Baseline | Treatment | Δ |
|---|---:|---:|---:|
| Factual CORRECT (/9) | 0 | 0 | +0 |
| Factual PARTIAL (/9) | 0 | 0 | +0 |
| Factual WRONG (/9) | 0 | 0 | +0 |
| Citation EXACT (/9) | 0 | 0 | +0 |
| Citation ADJACENT (/9) | 0 | 0 | +0 |
| Citation WRONG (/9) | 0 | 0 | +0 |
| Mean tokens | 0 | 0 | +0 |
| Mean latency (ms) | 0 | 0 | +0 |

## Per-persona breakdown

| Persona | Cond | Fact ✓ | Cite ✓ | Mean tokens | Mean latency (ms) |
|---|---|---:|---:|---:|---:|

## Per-question detail

Format: `Fact / Cite / Tokens` — F=factual (C=correct, P=partial, W=wrong), C=citation (E=exact, A=adjacent ±2, W=wrong).

| QID | Persona | Difficulty | Truth pages | Baseline | Treatment |
|---|---|---|---|---|---|
| Q1 | sector_analyst | easy | [276] | — | — |
| Q2 | sector_analyst | medium | [426] | — | — |
| Q3 | sector_analyst | hard | [321] | — | — |
| Q4 | ic_member | easy | [23, 26, 53] | — | — |
| Q5 | ic_member | medium | [29] | — | — |
| Q6 | ic_member | hard | [27, 70] | — | — |
| Q7 | buyer_dd | easy | [219] | — | — |
| Q8 | buyer_dd | medium | [53] | — | — |
| Q9 | buyer_dd | hard | [219, 227] | — | — |

## Failure modes

**Baseline imperfect results**: 0/9
**Treatment imperfect results**: 0/9

## Interpretation

- Tree is NEUTRAL on factual accuracy.
- Tree is NEUTRAL on citation accuracy.
- Tree INCREASES token cost: +0 tokens/query (larger context).
- Tree INCREASES latency: +0 ms/query.

**Verdict**: Tree is neutral or marginal — both conditions perform similarly on this benchmark.