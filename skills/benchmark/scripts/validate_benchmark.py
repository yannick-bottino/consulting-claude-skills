#!/usr/bin/env python3
"""
validate_benchmark.py — Validates actor JSON and benchmark.json against schema rules.

Usage:
  python scripts/validate_benchmark.py actor <path-to-actor.json> <path-to-mission-config.json>
  python scripts/validate_benchmark.py benchmark <path-to-benchmark.json>
  python scripts/validate_benchmark.py --help

Returns exit code 0 on PASS, 1 on FAIL.
Prints structured report to stdout.
"""

import json
import sys
import os
import re

# Windows UTF-8 fix (same pattern as scrape.py)
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def load_json(path: str) -> dict:
    """Load and parse a JSON file. Returns dict or raises."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# V2 fields: warn-only if missing (backward compat with v1 actor JSONs)
# Split by benchmark type: a field that cannot exist for a type must not be warned on.
V2_WARN_FIELDS_BASE = [
    "quote",
]

V2_WARN_FIELDS_BY_NATURE = {
    "offer": ["market_position", "vehicle_catalog", "optional_services"],
    "maturity": [],
    "generic": [],
}

# Dimension sub-fields per benchmark nature — mirrors references/profiles/<nature>.md section 1
DIM_SUBFIELDS_BY_NATURE = {
    "offer": ["description", "content", "targets_tov", "pricing"],
    "maturity": ["maturity_level", "key_metrics", "certifications", "commitments"],
    "generic": ["description", "evidence", "implication"],
}

# Legacy benchmark_type values, kept readable so v2 missions still validate
TYPE_TO_NATURE = {
    "commercial": "offer",
    "rse": "maturity",
}

ACCEPTED_SCHEMA_VERSIONS = ("1.0", "2.0", "3.0")

CONFIDENCE_VALUES = ("observed", "estimated", "interpreted", "absent")

# Multi-currency: a euro-only pattern silently passed every non-EUR benchmark.
CURRENCIES = "EUR|USD|GBP|CHF|CAD|AUD|JPY|SEK|DKK|NOK|PLN"
PRICE_RE = re.compile(
    r"\d[\d\s.,]*\s*(?:[€£\$]|(?:" + CURRENCIES + r")\b)"
    r"|[€£\$]\s*\d"
    r"|(?:" + CURRENCIES + r")\s*\d",
    re.IGNORECASE,
)


def resolve_nature(config: dict) -> str:
    """Read benchmark_nature from a mission config or benchmark.json.

    Falls back to the legacy benchmark_type alias, then to 'offer'.
    """
    mission = config.get("mission", {}) if isinstance(config.get("mission"), dict) else {}
    nature = config.get("benchmark_nature") or mission.get("benchmark_nature")
    if not nature:
        legacy = config.get("benchmark_type") or mission.get("benchmark_type")
        if legacy:
            nature = TYPE_TO_NATURE.get(str(legacy).strip().lower(), str(legacy))
    return (nature or "offer").strip().lower()


def validate_comparables(rows: list, comparability: dict, known_actors: set, prefix: str) -> list[dict]:
    """Row-level checks for comparables[], used at actor level and at benchmark level.

    Running them at actor level matters: a subagent that emits malformed rows must
    fail its own gate, not at assembly time when the batch is already accepted.
    """
    issues = []
    metrics = comparability.get("metrics", []) if isinstance(comparability, dict) else []
    declared = {m.get("name") for m in metrics if isinstance(m, dict)}
    names = [m.get("name") for m in metrics if isinstance(m, dict)]
    for n in {x for x in names if names.count(x) > 1}:
        issues.append({"level": "FAIL", "field": "comparability.metrics",
                       "message": f"Metric name '{n}' declared more than once — the name is the "
                                  f"reference key, so a duplicate makes every row citing it "
                                  f"ambiguous. Give each basis its own name (price, price_km...)"})
    if rows and not declared:
        issues.append({"level": "FAIL", "field": prefix.rstrip(".") or "comparability.metrics",
                       "message": "comparables present but comparability.metrics is empty — "
                                  "a comparable with no declared metric and unit is not comparable"})
    seen = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            issues.append({"level": "FAIL", "field": "%s[%d]" % (prefix, i), "message": "Comparable must be an object"})
            continue
        where = "%s[%s]" % (prefix, row.get("id", i))
        rid = row.get("id")
        if not rid:
            issues.append({"level": "WARN", "field": where, "message": "Missing id"})
        elif rid in seen:
            issues.append({"level": "FAIL", "field": where, "message": f"Duplicate comparable id '{rid}'"})
        else:
            seen.add(rid)

        if known_actors and row.get("actor") not in known_actors:
            issues.append({"level": "FAIL", "field": where + ".actor",
                          "message": f"Actor '{row.get('actor')}' not in scope.actors"})

        if declared and row.get("metric") not in declared:
            issues.append({"level": "FAIL", "field": where + ".metric",
                          "message": f"Metric '{row.get('metric')}' not declared in comparability.metrics"})

        conf = row.get("confidence")
        has_value = row.get("value") is not None or bool(row.get("value_text"))
        if conf not in CONFIDENCE_VALUES:
            issues.append({"level": "FAIL", "field": where + ".confidence",
                          "message": f"Invalid confidence '{conf}' — must be one of {', '.join(CONFIDENCE_VALUES)}"})
        elif conf == "absent":
            if not row.get("note"):
                issues.append({"level": "WARN", "field": where + ".note",
                              "message": "confidence 'absent' with no note — state why the value could not be found"})
            if has_value:
                issues.append({"level": "FAIL", "field": where,
                              "message": "confidence 'absent' but a value is present — pick one"})
        else:
            if not has_value:
                issues.append({"level": "FAIL", "field": where,
                              "message": "No value and no value_text, but confidence is not 'absent'"})
            if not row.get("unit") and not any(
                m.get("name") == row.get("metric") and m.get("unit") for m in metrics if isinstance(m, dict)
            ):
                issues.append({"level": "WARN", "field": where + ".unit",
                              "message": "No unit on the row and none on the declared metric"})
            if conf == "observed" and not row.get("source_ref"):
                issues.append({"level": "WARN", "field": where + ".source_ref",
                              "message": "Observed value with no source reference (rule D2)"})
    return issues


def validate_actor(actor: dict, mission_config: dict) -> list[dict]:
    """
    Validate a single actor JSON object against schema rules.
    Returns list of issues: [{"level": "FAIL|WARN|INFO", "field": str, "message": str}]
    """
    issues = []
    nature = resolve_nature(mission_config)
    if nature not in DIM_SUBFIELDS_BY_NATURE:
        issues.append({"level": "WARN", "field": "benchmark_nature",
                       "message": f"Unknown benchmark_nature '{nature}' — falling back to generic "
                                  f"sub-fields. Declare it in DIM_SUBFIELDS_BY_NATURE and write "
                                  f"references/profiles/{nature}.md (rule G2)."})
        nature = "generic"

    # Required top-level fields. `target` (B2B/B2C) describes a market being addressed:
    # it is required for an offer comparison and meaningless in a maturity assessment.
    required_fields = ["id", "name", "category", "dimensions",
                       "a_retenir", "insights_positive", "insights_negative", "sources"]
    if nature == "offer":
        required_fields.append("target")
    for field in required_fields:
        if field not in actor or actor[field] is None:
            issues.append({"level": "FAIL", "field": field, "message": f"Required field '{field}' is missing"})

    # Target must be valid enum
    if actor.get("target") and actor["target"] not in ("B2B", "B2C", "B2B+B2C"):
        issues.append({"level": "FAIL", "field": "target", "message": f"Invalid target '{actor['target']}' — must be B2B|B2C|B2B+B2C"})

    # Dimensions must match mission config
    expected_dims = set()
    if "dimensions" in mission_config:
        dims = mission_config["dimensions"]
        if isinstance(dims, list):
            expected_dims = {d["id"] for d in dims if isinstance(d, dict) and "id" in d}

    if expected_dims:
        actual_dims = set(actor.get("dimensions", {}).keys())
        missing_dims = expected_dims - actual_dims
        extra_dims = actual_dims - expected_dims
        for dim in missing_dims:
            issues.append({"level": "FAIL", "field": f"dimensions.{dim}", "message": f"Missing dimension '{dim}' (expected from mission config)"})
        for dim in extra_dims:
            issues.append({"level": "INFO", "field": f"dimensions.{dim}", "message": f"Extra dimension '{dim}' not in mission config"})

    # Each dimension must have the sub-fields defined for this benchmark type
    dim_subfields = DIM_SUBFIELDS_BY_NATURE[nature]
    for dim_id, dim_data in actor.get("dimensions", {}).items():
        if not isinstance(dim_data, dict):
            issues.append({"level": "FAIL", "field": f"dimensions.{dim_id}", "message": "Dimension data must be an object"})
            continue
        for sf in dim_subfields:
            if sf not in dim_data or not dim_data[sf]:
                issues.append({"level": "WARN", "field": f"dimensions.{dim_id}.{sf}", "message": f"Empty sub-field '{sf}' in dimension '{dim_id}'"})

    # Sources must be non-empty
    sources = actor.get("sources", [])
    if not sources:
        issues.append({"level": "FAIL", "field": "sources", "message": "Actor has no sources — every actor must have at least 1 source"})

    # No price without source check — scan every sub-field, whatever the benchmark type
    pricing_texts = []
    for dim_id, dim_data in actor.get("dimensions", {}).items():
        if isinstance(dim_data, dict):
            for value in dim_data.values():
                if isinstance(value, str) and value:
                    pricing_texts.append(value)

    has_price = any(PRICE_RE.search(t) for t in pricing_texts)
    has_price_source = any(
        s.get("url") or s.get("document")
        for s in sources
        if any(kw in (s.get("description", "").lower()) for kw in ["prix", "tarif", "pricing", "cost"])
    )
    if has_price and not has_price_source and len(sources) < 2:
        issues.append({"level": "WARN", "field": "sources", "message": "Prices found in dimensions but no pricing-specific source identified"})

    # A retenir must be 1 sentence (no bullet points)
    a_retenir = actor.get("a_retenir", "")
    if a_retenir and ("\n" in a_retenir or a_retenir.strip().startswith("-") or a_retenir.strip().startswith("\u2022")):
        issues.append({"level": "FAIL", "field": "a_retenir", "message": "'A retenir' must be exactly 1 sentence, no bullets"})

    # Insights must be opinionated (at least 1 positive, 1 negative)
    if not actor.get("insights_positive"):
        issues.append({"level": "WARN", "field": "insights_positive", "message": "No positive insights — expected at least 1"})
    if not actor.get("insights_negative"):
        issues.append({"level": "WARN", "field": "insights_negative", "message": "No negative insights — expected at least 1"})

    # Data quality block
    dq = actor.get("data_quality", {})
    if not dq:
        issues.append({"level": "WARN", "field": "data_quality", "message": "Missing data_quality block"})

    # Uncertain fields tracking
    uncertain = actor.get("uncertain_fields", [])
    if uncertain:
        issues.append({"level": "INFO", "field": "uncertain_fields", "message": f"{len(uncertain)} uncertain field(s): {', '.join(uncertain)}"})

    # V2 fields: warn-only (backward compat — v1 JSONs won't have these).
    # In v3 the offer-nature blocks are projections generated from comparables[]
    # at assembly time, so an actor carrying comparables must not be warned for
    # not authoring them by hand.
    # After assembly the rows live at benchmark level, so v3 mode is signalled
    # either by the actor's own comparables or by the parent benchmark's.
    v3_mode = bool(actor.get("comparables")) or bool(mission_config.get("has_comparables"))
    v2_fields = list(V2_WARN_FIELDS_BASE)
    if not v3_mode:
        v2_fields += V2_WARN_FIELDS_BY_NATURE[nature]
    for field in v2_fields:
        value = actor.get(field)
        if value is None:
            issues.append({"level": "WARN", "field": field,
                          "message": f"[v2] Field '{field}' missing — expected in schema v2 actors. "
                                     f"Run actor research with updated prompt to populate."})
        elif isinstance(value, list) and len(value) == 0:
            issues.append({"level": "WARN", "field": field,
                          "message": f"[v2] Field '{field}' is empty list — at least 1 entry expected."})
        elif isinstance(value, str) and value.startswith("[N/D"):
            issues.append({"level": "INFO", "field": field,
                          "message": f"[v2] Field '{field}' = {value}"})

    # Comparables carried by this actor (v3). Merged into benchmark.comparables later.
    issues += validate_comparables(
        actor.get("comparables", []) or [],
        mission_config.get("comparability", {}),
        {actor.get("name")} if actor.get("name") else set(),
        "comparables",
    )

    # Offer catalog quality check — commercial benchmarks only
    catalog = actor.get("vehicle_catalog", []) if nature == "offer" else []
    if catalog:
        has_price = any(
            any(entry.get(k) and not str(entry.get(k, "")).startswith("[N/D")
                for k in ["price_1m", "price_3m", "price_6m", "price_12m"])
            for entry in catalog
        )
        if not has_price:
            issues.append({"level": "WARN", "field": "vehicle_catalog",
                          "message": "[v2] vehicle_catalog has entries but all prices are [N/D] — try configurator or contact page"})

    return issues


def check_manifest_consistency(benchmark: dict, benchmark_path: str) -> list[dict]:
    """The capture manifest is authoritative; actors[].screenshots is a copy.

    A copy goes stale the moment a target is recaptured, and a stale `ok` entry is
    how a dead page becomes evidence in a client report. Enforce the arbitration
    instead of only writing it in the spec.
    """
    issues = []
    manifest_path = os.path.join(os.path.dirname(os.path.abspath(benchmark_path)),
                                 "actors", "screenshots", "capture-manifest.json")
    if not os.path.exists(manifest_path):
        return issues
    try:
        truth = {}
        for e in load_json(manifest_path).get("captures", []):
            truth[(e.get("actor_slug"), e.get("intent"))] = e
    except Exception as exc:
        issues.append({"level": "WARN", "field": "capture-manifest.json",
                       "message": f"Manifest present but unreadable: {exc}"})
        return issues

    for actor in benchmark.get("actors", []):
        for shot in actor.get("screenshots", []) or []:
            key = (actor.get("id"), shot.get("intent"))
            ref = truth.get(key)
            if ref is None:
                issues.append({"level": "FAIL", "field": f"actors[{actor.get('id')}].screenshots",
                               "message": f"Screenshot '{shot.get('intent')}' is not in the capture "
                                          f"manifest. Re-fold from the manifest (capture-spec.md section 6)"})
            elif ref.get("status") != shot.get("status"):
                issues.append({"level": "FAIL", "field": f"actors[{actor.get('id')}].screenshots",
                               "message": f"Screenshot '{shot.get('intent')}' says '{shot.get('status')}' "
                                          f"but the manifest says '{ref.get('status')}'. The manifest wins: "
                                          f"re-fold it. A stale 'ok' is how a dead page becomes evidence"})
    return issues


def validate_benchmark(benchmark: dict) -> list[dict]:
    """Validate the full benchmark.json."""
    issues = []

    # Schema version
    if benchmark.get("schema_version") not in ACCEPTED_SCHEMA_VERSIONS:
        issues.append({"level": "WARN", "field": "schema_version",
                      "message": f"Expected one of {', '.join(ACCEPTED_SCHEMA_VERSIONS)}, "
                                 f"got '{benchmark.get('schema_version')}'"})

    # Mission block
    mission = benchmark.get("mission", {})
    for field in ["name", "slug", "client", "market", "date"]:
        if not mission.get(field):
            issues.append({"level": "FAIL", "field": f"mission.{field}", "message": f"Missing required mission field '{field}'"})

    # Actors
    actors = benchmark.get("actors", [])
    if not actors:
        issues.append({"level": "FAIL", "field": "actors", "message": "No actors in benchmark"})

    # Validate each actor against benchmark dimensions
    mission_config_proxy = {
        "dimensions": benchmark.get("dimensions", []),
        "benchmark_nature": resolve_nature(benchmark),
        "comparability": benchmark.get("comparability", {}),
        "has_comparables": bool(benchmark.get("comparables")),
    }
    for actor in actors:
        actor_issues = validate_actor(actor, mission_config_proxy)
        for issue in actor_issues:
            issue["field"] = f"actors[{actor.get('id', '?')}].{issue['field']}"
            issues.append(issue)

    # Category consistency
    categories = benchmark.get("scope", {}).get("actor_categories", {})
    for actor in actors:
        cat = actor.get("category", "")
        if cat and categories and cat not in categories:
            issues.append({"level": "FAIL", "field": f"actors[{actor.get('id')}].category",
                          "message": f"Category '{cat}' not in scope.actor_categories"})

    # Pricing matrix
    pm = benchmark.get("pricing_matrix", {})
    if pm:
        for entry in pm.get("data", []):
            ti = entry.get("transparency_index")
            if ti is not None and ti not in (1, 2, 3):
                issues.append({"level": "FAIL", "field": f"pricing_matrix.data[{entry.get('actor')}].transparency_index",
                              "message": f"Invalid transparency_index {ti} — must be 1, 2, or 3"})

    # Data quality
    if not benchmark.get("data_quality", {}).get("retrieval_date"):
        issues.append({"level": "WARN", "field": "data_quality.retrieval_date", "message": "Missing retrieval_date"})

    # Comparables (v3). Absent means legacy mode: nothing to check.
    comparables = benchmark.get("comparables")
    if comparables:
        issues += validate_comparables(
            comparables,
            benchmark.get("comparability", {}),
            set(benchmark.get("scope", {}).get("actors", [])),
            "comparables",
        )

    # Synthesis sections: only warn about what the mission actually ordered.
    # Warning about a deliverable nobody asked for is the same non-applicability
    # defect as scoring a benchmark out of a fixed total.
    deliverables = benchmark.get("deliverables") or benchmark.get("scope", {}).get("deliverables")
    def ordered(name: str) -> bool:
        return deliverables is None or name in deliverables

    if ordered("market-landscape") and not benchmark.get("market_landscape"):
        issues.append({"level": "WARN", "field": "market_landscape",
                      "message": "market_landscape section missing — expected from Phase 3d"})
    if ordered("exec-summary") and not benchmark.get("roue_concurrentielle"):
        issues.append({"level": "WARN", "field": "roue_concurrentielle",
                      "message": "roue_concurrentielle section missing — expected from Phase 3c"})
    if ordered("recommendation") and not benchmark.get("recommendation"):
        issues.append({"level": "WARN", "field": "recommendation",
                      "message": "recommendation section missing — expected from Phase 3e"})

    return issues


def substance_report(benchmark: dict) -> list[str]:
    """Lines describing what the benchmark actually contains, not whether it parses.

    A structural PASS says every field exists. It says nothing about whether the
    central metric was found, which is what the reader of a benchmark wants to know.
    """
    lines = []
    rows = benchmark.get("comparables") or []
    if rows:
        by_conf = {}
        for r in rows:
            by_conf[r.get("confidence")] = by_conf.get(r.get("confidence"), 0) + 1
        found = sum(v for k, v in by_conf.items() if k in ("observed", "estimated"))
        lines.append("Comparables: %d rows — %s" % (
            len(rows), ", ".join("%s %d" % (k, v) for k, v in sorted(by_conf.items(), key=lambda x: str(x[0])))))
        pct = round(100 * found / len(rows)) if rows else 0
        lines.append("Substance: %d%% of comparable rows carry a value (observed or estimated)" % pct)
        if pct == 0:
            lines.append("WARNING: not a single comparable value was found. The benchmark parses "
                         "but has nothing to compare. A structural PASS is not a deliverable.")
        # per-metric emptiness, so an empty central metric cannot hide in an average
        per_metric = {}
        for r in rows:
            k = r.get("metric")
            per_metric.setdefault(k, []).append(r.get("confidence"))
        for metric, confs in sorted(per_metric.items(), key=lambda x: str(x[0])):
            if all(c == "absent" for c in confs):
                lines.append("WARNING: metric '%s' is absent for every actor (%d rows). If it is the "
                             "comparison's central metric, say so in the delivery summary." % (metric, len(confs)))
    else:
        lines.append("Comparables: none. Nothing measurable was collected (legacy v2 file, or a gap).")

    shots = [s for a in benchmark.get("actors", []) for s in (a.get("screenshots") or [])]
    if shots:
        ok = sum(1 for s in shots if s.get("status") == "ok")
        lines.append("Screenshots: %d of %d usable" % (ok, len(shots)))
        if ok == 0:
            lines.append("WARNING: no usable screenshot. Any section built on visual evidence must be hidden.")
    return lines


def print_report(issues: list[dict], target_name: str, substance: list = None) -> bool:
    """Print validation report. Returns True if PASS (no FAIL issues)."""
    fails = [i for i in issues if i["level"] == "FAIL"]
    warns = [i for i in issues if i["level"] == "WARN"]
    infos = [i for i in issues if i["level"] == "INFO"]

    coverage = max(0, 100 - (len(fails) * 10 + len(warns) * 3))

    status = "PASS" if not fails else "FAIL"
    print(f"\n{'=' * 60}")
    print(f"  VALIDATION: {status} -- {target_name}")
    print(f"  Coverage: {coverage}% | FAIL: {len(fails)} | WARN: {len(warns)} | INFO: {len(infos)}")
    print(f"{'=' * 60}")

    for issue in fails:
        print(f"  FAIL  [{issue['field']}] {issue['message']}")
    for issue in warns:
        print(f"  WARN  [{issue['field']}] {issue['message']}")
    for issue in infos:
        print(f"  INFO  [{issue['field']}] {issue['message']}")

    if substance:
        print("  --- substance ---")
        for line in substance:
            print("  %s" % line)

    print(f"{'=' * 60}\n")
    return not fails


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print("Usage:")
        print("  python scripts/validate_benchmark.py actor <actor.json> <mission-config.json>")
        print("  python scripts/validate_benchmark.py benchmark <benchmark.json>")
        sys.exit(0)

    mode = sys.argv[1]

    if mode == "actor":
        if len(sys.argv) < 4:
            print("ERROR: actor mode requires <actor.json> and <mission-config.json>", file=sys.stderr)
            sys.exit(1)
        actor_path = sys.argv[2]
        config_path = sys.argv[3]
        actor = load_json(actor_path)
        config = load_json(config_path)
        issues = validate_actor(actor, config)
        passed = print_report(issues, os.path.basename(actor_path))

    elif mode == "benchmark":
        if len(sys.argv) < 3:
            print("ERROR: benchmark mode requires <benchmark.json>", file=sys.stderr)
            sys.exit(1)
        benchmark_path = sys.argv[2]
        benchmark = load_json(benchmark_path)
        issues = validate_benchmark(benchmark)
        issues += check_manifest_consistency(benchmark, benchmark_path)
        passed = print_report(issues, os.path.basename(benchmark_path), substance_report(benchmark))

    else:
        print(f"ERROR: Unknown mode '{mode}'. Use 'actor' or 'benchmark'.", file=sys.stderr)
        sys.exit(1)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
