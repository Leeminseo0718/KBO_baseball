from __future__ import annotations

import argparse
import json
from pathlib import Path

from kbo_data.query_engine import TemplatePlanner


def evaluate(path: Path) -> dict:
    planner = TemplatePlanner()
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    failures = []
    for case in cases:
        plan = planner.plan(case["question"])
        passed = plan.accepted == case["accepted"] and plan.question_type == case["expected_type"]
        if not passed:
            failures.append({"id": case["id"], "expected": case["expected_type"], "actual": plan.question_type, "accepted": plan.accepted})
    passed_count = len(cases) - len(failures)
    return {
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
    args = parser.parse_args()
    result = evaluate(Path(args.cases))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["target_met"] else 1)


if __name__ == "__main__":
    main()

