from __future__ import annotations

import argparse
import json
from pathlib import Path

from kbo_data.query_engine import TemplatePlanner
from kbo_data.rag_planner import RagPlanner, grounded
from kbo_data.retriever import MetricRetriever


def _planner(name: str):
    if name == "template":
        return TemplatePlanner()
    if name == "rag":
        return RagPlanner()
    if name == "rag-llm":
        return RagPlanner.from_env()
    raise ValueError(name)


def evaluate(path: Path, planner_name: str = "template", strict: bool = False) -> dict:
    """Scores a planner.

    Default mode checks only accept/refuse and question type (the original criterion).
    Strict mode also requires the SQL to compute every metric the question asked for.
    """
    planner = _planner(planner_name)
    metrics = {doc["id"]: doc for doc in MetricRetriever().docs}
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    failures = []
    for case in cases:
        plan = planner.plan(case["question"])
        passed = plan.accepted == case["accepted"] and plan.question_type == case["expected_type"]
        reason = None if passed else "type"
        if passed and strict and case.get("expected_metrics"):
            if not all(grounded(plan.sql, plan.question_type, metrics[m]) for m in case["expected_metrics"]):
                passed, reason = False, "metric"
        if not passed:
            failures.append({"id": case["id"], "question": case["question"], "reason": reason,
                             "expected": case["expected_type"], "actual": plan.question_type, "accepted": plan.accepted})
    passed_count = len(cases) - len(failures)
    return {
        "planner": planner_name,
        "strict": strict,
        "total": len(cases),
        "passed": passed_count,
        "accuracy": round(passed_count / len(cases), 4) if cases else 0,
        "target": 0.89,
        "target_met": bool(cases) and passed_count / len(cases) >= 0.89,
        "failures": failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="evals/text_to_sql_cases.jsonl")
    parser.add_argument("--planner", choices=["template", "rag", "rag-llm"], default="template")
    parser.add_argument("--strict", action="store_true", help="also require the SQL to compute the asked metric")
    args = parser.parse_args()
    result = evaluate(Path(args.cases), args.planner, args.strict)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["target_met"] else 1)


if __name__ == "__main__":
    main()
