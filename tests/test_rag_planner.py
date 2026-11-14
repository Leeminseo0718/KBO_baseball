from pathlib import Path

from kbo_data.eval_runner import evaluate
from kbo_data.rag_planner import RagPlanner, grounded
from kbo_data.retriever import MetricRetriever

STRICT = Path(__file__).resolve().parents[1] / "evals" / "strict_cases.jsonl"


def test_retriever_prefers_longest_alias():
    hits = MetricRetriever().search("원태인 탈삼진 추이")
    assert [hit.doc["id"] for hit in hits] == ["strikeouts"]


def test_retriever_returns_nothing_for_unknown_metric():
    assert MetricRetriever().search("세이브 순위 알려줘") == []


def test_era_ranking_uses_definition_and_sorts_ascending():
    plan = RagPlanner().plan("이번 시즌 평균자책 순위")
    assert plan.accepted and "earned_runs" in plan.sql and "ORDER BY value ASC" in plan.sql


def test_refuses_metric_that_cannot_be_computed():
    plan = RagPlanner().plan("OPS 순위 알려줘")
    assert not plan.accepted and "계산할 수 없습니다" in plan.message


def test_refuses_ranking_without_a_known_metric():
    assert not RagPlanner().plan("세이브 순위 알려줘").accepted


class _FakeLLM:
    def __init__(self, sql):
        self.sql, self.context = sql, None

    def plan(self, question, schema_context):
        self.context = schema_context
        return {"accepted": True, "question_type": "ranking", "title": "t", "sql": self.sql, "params": [2026], "chart": None, "message": ""}


def test_llm_receives_retrieved_definition_and_grounded_sql_is_used():
    llm = _FakeLLM("SELECT player_name, SUM(earned_runs)*27.0/NULLIF(SUM(innings_outs),0) AS value "
                   "FROM kbo.v_player_game_pitching WHERE season=%s GROUP BY player_name ORDER BY value ASC")
    plan = RagPlanner(llm=llm).plan("이번 시즌 평균자책 순위")
    assert "자책점" in llm.context and plan.message.startswith("검색된 지표 정의")


def test_ungrounded_llm_sql_is_replaced_by_definition_based_sql():
    llm = _FakeLLM("SELECT player_name, SUM(strikeouts) AS value FROM kbo.v_player_game_pitching "
                   "WHERE season=%s GROUP BY player_name ORDER BY value DESC")
    plan = RagPlanner(llm=llm).plan("이번 시즌 평균자책 순위")
    assert "earned_runs" in plan.sql and grounded(plan.sql, "ranking", MetricRetriever().docs[7])


def test_strict_eval_gap_between_planners():
    assert evaluate(STRICT, "template", strict=True)["accuracy"] < 0.89
    assert evaluate(STRICT, "rag", strict=True)["target_met"]
