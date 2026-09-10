from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

from kbo_data.query_guard import validate_readonly_sql


PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "accepted": {"type": "boolean"},
        "question_type": {"type": "string", "enum": ["performance", "comparison", "trend", "ranking", "refusal"]},
        "title": {"type": "string"},
        "sql": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "params": {"type": "array", "items": {"anyOf": [{"type": "string"}, {"type": "number"}]}},
        "chart": {
            "anyOf": [
                {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "category": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "x": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "fields": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["type", "category", "x", "fields"],
                    "additionalProperties": False,
                },
                {"type": "null"},
            ]
        },
        "message": {"type": "string"},
    },
    "required": ["accepted", "question_type", "title", "sql", "params", "chart", "message"],
    "additionalProperties": False,
}


class OpenAIPlanner:
    """Optional planner. It creates a plan only; the server still validates SQL."""

    def __init__(self) -> None:
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.6-terra")

    def plan(self, question: str, schema_context: str) -> dict[str, Any]:
        body = {
            "model": self.model,
            "store": False,
            "instructions": (
                "You plan read-only PostgreSQL queries for a KBO analytics service. "
                "Only performance, comparison, trend, and ranking questions are allowed. "
                "Use only relations in the provided schema. Refuse ambiguity. Never produce writes."
            ),
            "input": f"SCHEMA:\n{schema_context}\n\nQUESTION:\n{question}",
            "text": {"format": {"type": "json_schema", "name": "kbo_query_plan", "strict": True, "schema": PLAN_SCHEMA}},
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(body).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
        output_text = payload.get("output_text")
        if not output_text:
            for item in payload.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        output_text = content.get("text")
        plan = json.loads(output_text)
        if plan.get("accepted"):
            plan["sql"] = validate_readonly_sql(plan["sql"], 100)
        return plan
