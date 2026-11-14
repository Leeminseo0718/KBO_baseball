from __future__ import annotations

import os
import re
from typing import Any, Protocol

from kbo_data.query_engine import SUPPORTED_MESSAGE, QueryPlan, TemplatePlanner
from kbo_data.query_guard import UnsafeQuery, validate_readonly_sql
from kbo_data.retriever import Hit, MetricRetriever

VIEWS = {"batting": "kbo.v_player_game_batting", "pitching": "kbo.v_player_game_pitching"}
SCHEMA_CONTEXT = """kbo.v_player_game_batting(game_date, season, team_name, player_name, plate_appearances, at_bats, hits, home_runs, walks, strikeouts, runs, rbi, stolen_bases)
kbo.v_player_game_pitching(game_date, season, team_name, player_name, innings_outs, batters_faced, hits, home_runs, walks, strikeouts, runs, earned_runs, pitches, decision)"""


class LLMPlanner(Protocol):
    def plan(self, question: str, schema_context: str) -> dict[str, Any]: ...


def grounded(sql: str | None, question_type: str, metric: dict[str, Any]) -> bool:
    """True when the SQL actually computes the retrieved metric, not a neighbouring one."""
    if not sql:
        return False
    text = " ".join(sql.lower().split())
    if VIEWS[metric["side"]] not in text:
        return False
    if question_type == "ranking":
        value = re.search(r"select\s+player_name\s*,\s*(.+?)\s+as\s+value\b", text)
        order = re.search(r"order\s+by\s+value\s+(asc|desc)", text)
        if not value or not order or order.group(1) != metric["order"].lower():
            return False
        text = value.group(1)
    return all(re.search(rf"\b{column}\b", text) for column in metric["columns"])


class RagPlanner(TemplatePlanner):
    """Retrieval-grounded planner.

    1. Retrieve metric definitions for the question from knowledge/metrics.jsonl.
    2. Refuse when a retrieved definition says the metric cannot be computed from the mart.
    3. Generate SQL from the retrieved definition: with an LLM when one is supplied,
       otherwise (or when the LLM's SQL is not grounded in the definition) with a
       deterministic builder that uses the definition's own expression.
    Questions that name no metric fall back to the baseline templates.
    """

    def __init__(self, retriever: MetricRetriever | None = None, llm: LLMPlanner | None = None) -> None:
        self.retriever = retriever or MetricRetriever()
        self.llm = llm

    @classmethod
    def from_env(cls) -> "RagPlanner":
        llm = None
        if os.getenv("OPENAI_API_KEY"):
            from kbo_data.openai_planner import OpenAIPlanner

            llm = OpenAIPlanner()
        return cls(llm=llm)

    def plan(self, question: str) -> QueryPlan:
        base = super().plan(question)
        hits = self.retriever.search(question)
        if not hits:
            if base.question_type == "ranking":
                return self.refuse("어떤 지표의 순위인지 지표 사전에서 찾지 못했습니다. 예: 홈런 순위, 평균자책 순위")
            return base
        unavailable = [hit.doc for hit in hits if not hit.doc["available"]]
        if unavailable:
            doc = unavailable[0]
            return self.refuse(f"{doc['name']}은(는) 현재 데이터로 계산할 수 없습니다. {doc['definition']}")
        if not base.accepted:
            return self._metric_without_player(question, hits) or base
        metrics = [hit.doc for hit in hits]
        side = metrics[0]["side"]
        metrics = [metric for metric in metrics if metric["side"] == side]
        names = self._player_names(question, hits)
        season = self._season(question)
        fallback = self._build(base.question_type, season, names, metrics)
        if fallback is None:
            return base
        if self.llm is not None:
            generated = self._generate(question, base.question_type, metrics)
            if generated is not None:
                return generated
        return fallback

    def _metric_without_player(self, question: str, hits: list[Hit]) -> QueryPlan | None:
        text = " ".join(question.split())
        if any(word in text for word in ("순위", "랭킹", "1위")):
            return self._build("ranking", self._season(text), [], [hits[0].doc])
        return None

    def _player_names(self, question: str, hits: list[Hit]) -> list[str]:
        text = question
        for doc in self.retriever.docs:
            for alias in sorted(doc["aliases"], key=len, reverse=True):
                text = re.sub(re.escape(alias), " ", text, flags=re.IGNORECASE)
        return self._names(text)

    def _build(self, kind: str, season: int, names: list[str], metrics: list[dict[str, Any]]) -> QueryPlan | None:
        view = VIEWS[metrics[0]["side"]]
        select = ", ".join(f"{metric['expr']} AS {metric['id']}" for metric in metrics)
        fields = [metric["id"] for metric in metrics]
        label = "·".join(metric["name"] for metric in metrics)
        if kind == "ranking":
            metric = metrics[0]
            sql = (f"SELECT player_name, {metric['expr']} AS value FROM {view} WHERE season=%s "
                   f"GROUP BY player_name ORDER BY value {metric['order']} NULLS LAST")
            return self._accept("ranking", f"{season} {metric['name']} 순위", sql, (season,),
                                {"type": "bar", "category": "player_name", "fields": ["value"]})
        if kind == "comparison" and len(names) >= 2:
            sql = (f"SELECT player_name, {select} FROM {view} WHERE season=%s AND player_name IN (%s,%s) "
                   "GROUP BY player_name ORDER BY player_name")
            return self._accept("comparison", f"{names[0]} · {names[1]} {label} 비교", sql, (season, names[0], names[1]),
                                {"type": "bar", "category": "player_name", "fields": fields})
        if kind == "trend" and names:
            sql = (f"SELECT game_date, {select} FROM {view} WHERE season=%s AND player_name=%s "
                   "GROUP BY game_date ORDER BY game_date")
            return self._accept("trend", f"{season} {names[0]} 경기별 {label} 추이", sql, (season, names[0]),
                                {"type": "line", "x": "game_date", "fields": fields})
        if kind == "performance" and names:
            sql = (f"SELECT player_name, COUNT(*) AS games, {select} FROM {view} WHERE season=%s AND player_name=%s "
                   "GROUP BY player_name")
            return self._accept("performance", f"{season} {names[0]} {label}", sql, (season, names[0]),
                                {"type": "metric", "fields": ["games", *fields]})
        return None

    def _generate(self, question: str, kind: str, metrics: list[dict[str, Any]]) -> QueryPlan | None:
        definitions = "\n".join(
            f"- {metric['name']} ({metric['side']}): {metric['definition']} SQL: {metric['expr']} / 정렬 {metric['order']}"
            for metric in metrics
        )
        context = (f"{SCHEMA_CONTEXT}\n\nRETRIEVED METRIC DEFINITIONS (use only these formulas):\n{definitions}\n"
                   "Rankings must select player_name and the metric AS value, ordered by value. Use %s placeholders for params.")
        try:
            raw = self.llm.plan(question, context)
            if not raw.get("accepted") or raw.get("question_type") != kind:
                return None
            sql = validate_readonly_sql(raw["sql"], 100)
        except (UnsafeQuery, KeyError, TypeError, ValueError, OSError):
            return None
        if not all(grounded(sql, kind, metric) for metric in metrics[:1]):
            return None
        return QueryPlan(True, kind, raw.get("title") or "", sql, tuple(raw.get("params") or ()), raw.get("chart"),
                         "검색된 지표 정의를 근거로 조회 계획을 만들었습니다.")
