"""One-shot: aggregate results/*.json into QUALITY-REPORT.md (anonymized)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
EVALS_PATH = HERE.resolve().parents[1] / "evals" / "evals.json"
QPOOL = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
from scoring import (
    score_citation, score_factual_accuracy, aggregate_run,
    CITATION_EXACT, CITATION_ADJACENT, CITATION_WRONG,
    FACT_CORRECT, FACT_PARTIAL, FACT_WRONG,
)

truth_by_qid = {q["id"]: q for q in QPOOL["questions"]}


def anonymize(text: str) -> str:
    """Replace target company name and aliases with 'Target Co.'."""
    # Fill with the real names from your own run before aggregating; the map
    # is applied to every answer so the published report carries no client data.
    replacements = {
        "TargetCo": "Target Co.",
        "TARGETCO": "TARGET CO.",
        "BrandN": "Brand-N",
        "BrandU": "Brand-U",
        "BrandJ": "Brand-J",
        "PartnerA": "OffshorePartner-A",
        "PartnerB": "OffshorePartner-B",
        "PartnerC": "OffshorePartner-C",
    }
    out = text
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


def score_one(result: dict) -> dict:
    qid = result["qid"]
    truth = truth_by_qid[qid]
    if result.get("parse_error"):
        return {
            "qid": qid, "persona": truth["persona"], "condition": result["condition"],
            "factual": FACT_WRONG, "citation": CITATION_WRONG,
            "tokens": result.get("tokens", 0), "latency_ms": result.get("latency_ms", 0),
            "note": "parse_error",
        }
    resp = result["subagent_response"]
    return {
        "qid": qid, "persona": truth["persona"], "condition": result["condition"],
        "factual": score_factual_accuracy(resp["answer"], truth["evidence_phrases"]),
        "citation": score_citation(resp.get("citations", []), truth["ground_truth_pages"]),
        "tokens": result["tokens"], "latency_ms": result["latency_ms"],
    }


def main() -> None:
    results_dir = HERE / "results"
    rows = []
    for f in sorted(results_dir.glob("Q*-*.json")):
        result = json.loads(f.read_text(encoding="utf-8"))
        rows.append(score_one(result))

    baseline = [r for r in rows if r["condition"] == "baseline"]
    treatment = [r for r in rows if r["condition"] == "treatment"]

    md = ["# Tree Builder Quality Validation Report", ""]
    md.append("**Target**: anonymized (Target Co.)  ")
    md.append("**Source doc**: 437-page Strategic Vendor Due Diligence report  ")
    md.append(f"**Questions**: {len(QPOOL['questions'])} (3 sector analyst, 3 IC member, 3 buyer-DD; 3 easy / 3 medium / 3 hard)  ")
    md.append("**Conditions**: baseline (.md + plain index) vs treatment (.md + .tree.json + enriched index)  ")
    md.append("**Subagent model**: Claude Sonnet 4.6")
    md.append("")
    md.append("---")
    md.append("")

    md.append("## Aggregate scores")
    md.append("")
    md.append("| Metric | Baseline | Treatment | Δ |")
    md.append("|---|---:|---:|---:|")
    b = aggregate_run(baseline)
    t = aggregate_run(treatment)

    def line(label, key, fmt="{:.0f}"):
        bv = b.get(key, 0)
        tv = t.get(key, 0)
        d = tv - bv
        sign = "+" if d >= 0 else ""
        md.append(f"| {label} | {fmt.format(bv)} | {fmt.format(tv)} | {sign}{fmt.format(d)} |")

    line("Factual CORRECT (/9)",  "fact_correct")
    line("Factual PARTIAL (/9)",  "fact_partial")
    line("Factual WRONG (/9)",    "fact_wrong")
    line("Citation EXACT (/9)",   "citation_exact")
    line("Citation ADJACENT (/9)","citation_adjacent")
    line("Citation WRONG (/9)",   "citation_wrong")
    line("Mean tokens",           "mean_tokens")
    line("Mean latency (ms)",     "mean_latency_ms")
    md.append("")

    md.append("## Per-persona breakdown")
    md.append("")
    md.append("| Persona | Cond | Fact ✓ | Cite ✓ | Mean tokens | Mean latency (ms) |")
    md.append("|---|---|---:|---:|---:|---:|")
    for persona in ("sector_analyst", "ic_member", "buyer_dd"):
        for cond, subset in (("baseline", baseline), ("treatment", treatment)):
            sub = [r for r in subset if r["persona"] == persona]
            if not sub: continue
            agg = aggregate_run(sub)
            md.append(f"| {persona} | {cond} | {agg['fact_correct']}/{agg['n']} | {agg['citation_exact']}/{agg['n']} | {agg['mean_tokens']:.0f} | {agg['mean_latency_ms']:.0f} |")
    md.append("")

    md.append("## Per-question detail")
    md.append("")
    md.append("Format: `Fact / Cite / Tokens` — F=factual (C=correct, P=partial, W=wrong), C=citation (E=exact, A=adjacent ±2, W=wrong).")
    md.append("")
    md.append("| QID | Persona | Difficulty | Truth pages | Baseline | Treatment |")
    md.append("|---|---|---|---|---|---|")
    for q in QPOOL["questions"]:
        b_row = next((r for r in baseline if r["qid"] == q["id"]), None)
        t_row = next((r for r in treatment if r["qid"] == q["id"]), None)
        def fmt(r):
            if not r: return "—"
            f_short = {FACT_CORRECT:"C",FACT_PARTIAL:"P",FACT_WRONG:"W"}[r["factual"]]
            c_short = {CITATION_EXACT:"E",CITATION_ADJACENT:"A",CITATION_WRONG:"W"}[r["citation"]]
            return f"{f_short}/{c_short}/{r['tokens']}"
        md.append(f"| {q['id']} | {q['persona']} | {q['difficulty']} | {q['ground_truth_pages']} | {fmt(b_row)} | {fmt(t_row)} |")
    md.append("")

    md.append("## Failure modes")
    md.append("")
    failures_t = [r for r in treatment if r["factual"] != FACT_CORRECT or r["citation"] != CITATION_EXACT]
    failures_b = [r for r in baseline  if r["factual"] != FACT_CORRECT or r["citation"] != CITATION_EXACT]

    md.append(f"**Baseline imperfect results**: {len(failures_b)}/9")
    md.append(f"**Treatment imperfect results**: {len(failures_t)}/9")
    md.append("")

    if failures_t or failures_b:
        md.append("### Imperfect / failing answers (anonymized)")
        md.append("")
        for r in baseline + treatment:
            if r["factual"] == FACT_CORRECT and r["citation"] == CITATION_EXACT:
                continue
            q = truth_by_qid[r["qid"]]
            md.append(f"- **{r['qid']}** ({r['persona']}, {q['difficulty']}, **{r['condition']}**): factual={r['factual']}, citation={r['citation']} (cited vs truth {q['ground_truth_pages']})")
        md.append("")

    md.append("## Interpretation")
    md.append("")
    fact_delta = t.get("fact_correct", 0) - b.get("fact_correct", 0)
    cite_delta = t.get("citation_exact", 0) - b.get("citation_exact", 0)
    token_delta = t.get("mean_tokens", 0) - b.get("mean_tokens", 0)
    latency_delta = t.get("mean_latency_ms", 0) - b.get("mean_latency_ms", 0)

    if fact_delta > 0:
        md.append(f"- Tree IMPROVES factual accuracy: +{fact_delta} correct answers out of 9.")
    elif fact_delta == 0:
        md.append("- Tree is NEUTRAL on factual accuracy.")
    else:
        md.append(f"- Tree HURTS factual accuracy: {fact_delta} correct answers vs baseline. Investigate.")

    if cite_delta > 0:
        md.append(f"- Tree IMPROVES citation accuracy: +{cite_delta} exact citations out of 9.")
    elif cite_delta == 0:
        md.append("- Tree is NEUTRAL on citation accuracy.")
    else:
        md.append(f"- Tree HURTS citation accuracy: {cite_delta} exact citations. Investigate.")

    if token_delta < 0:
        md.append(f"- Tree REDUCES token cost: {token_delta:+.0f} tokens/query on average.")
    else:
        md.append(f"- Tree INCREASES token cost: {token_delta:+.0f} tokens/query (larger context).")

    if latency_delta < 0:
        md.append(f"- Tree REDUCES latency: {latency_delta:+.0f} ms/query on average.")
    else:
        md.append(f"- Tree INCREASES latency: {latency_delta:+.0f} ms/query.")

    md.append("")
    md.append("**Verdict**: " + (
        "Tree adds clear value on at least one quality axis." if (fact_delta > 0 or cite_delta > 0) else
        "Tree is neutral or marginal — both conditions perform similarly on this benchmark."
    ))

    out = anonymize("\n".join(md))
    (HERE / "QUALITY-REPORT.md").write_text(out, encoding="utf-8")
    print(f"Wrote {HERE / 'QUALITY-REPORT.md'}")


if __name__ == "__main__":
    main()
