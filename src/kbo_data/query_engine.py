from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from kbo_data.query_guard import validate_readonly_sql


TEAM_NAMES = ("KIA", "삼성", "LG", "두산", "KT", "SSG", "롯데", "한화", "NC", "키움")
SUPPORTED_MESSAGE = "성적 조회, 선수 비교, 시계열 추이, 순위 조회 질문만 지원합니다."


@dataclass(frozen=True)
class QueryPlan:
    accepted: bool
    question_type: str
    title: str
    sql: str | None
    params: tuple[Any, ...]
    chart: dict[str, Any] | None
    message: str

    def public_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["params"] = list(self.params)
        return payload


class TemplatePlanner:
    """Deterministic baseline for the four supported question families."""

    def plan(self, question: str) -> QueryPlan:
        text = " ".join(question.strip().split())
        if not text or len(text) > 200:
            return self.refuse("질문은 1~200자로 입력해 주세요.")
        if any(keyword in text.lower() for keyword in ("예측", "맞혀", "삭제", "drop", "테이블 목록", "개인정보", "잘생긴", "야구 규칙", "날씨")):
            return self.refuse(SUPPORTED_MESSAGE)
        season = self._season(text)
        names = self._names(text)
        is_pitching = any(keyword in text for keyword in ("ERA", "평균자책", "탈삼진", "WHIP", "이닝", "투수"))
        is_rank = "순위" in text or "랭킹" in text or "1위" in text
        is_trend = any(keyword in text for keyword in ("추이", "경기별", "변화", "최근"))
        is_compare = any(keyword in text for keyword in ("비교", "대결", "보다"))

        if is_rank:
            return self._ranking(text, season, is_pitching)
        if is_compare and len(names) >= 2:
            return self._comparison(text, season, names[:2], is_pitching)
        if is_trend and names:
            return self._trend(text, season, names[0], is_pitching)
        if names:
            return self._summary(text, season, names[0], is_pitching)
        return self.refuse(SUPPORTED_MESSAGE)

    def refuse(self, message: str) -> QueryPlan:
        return QueryPlan(False, "refusal", "질문을 처리할 수 없습니다", None, (), None, message)

    def _summary(self, text: str, season: int, name: str, pitching: bool) -> QueryPlan:
        if pitching:
            sql = """SELECT player_name, COUNT(*) AS games, SUM(innings_outs) AS innings_outs,
SUM(strikeouts) AS strikeouts, SUM(earned_runs) AS earned_runs
FROM kbo.v_player_game_pitching WHERE season=%s AND player_name=%s
GROUP BY player_name"""
            chart = {"type": "metric", "fields": ["games", "innings_outs", "strikeouts", "earned_runs"]}
        else:
            sql = """SELECT player_name, SUM(plate_appearances) AS pa, SUM(at_bats) AS ab,
SUM(hits) AS hits, SUM(home_runs) AS home_runs, SUM(rbi) AS rbi
FROM kbo.v_player_game_batting WHERE season=%s AND player_name=%s
GROUP BY player_name"""
            chart = {"type": "metric", "fields": ["pa", "hits", "home_runs", "rbi"]}
        return self._accept("performance", f"{season} {name} 성적", sql, (season, name), chart)

    def _comparison(self, text: str, season: int, names: list[str], pitching: bool) -> QueryPlan:
        if pitching:
            sql = """SELECT player_name, SUM(innings_outs) AS innings_outs, SUM(strikeouts) AS strikeouts,
SUM(earned_runs) AS earned_runs FROM kbo.v_player_game_pitching
WHERE season=%s AND player_name IN (%s,%s) GROUP BY player_name ORDER BY player_name"""
            fields = ["innings_outs", "strikeouts", "earned_runs"]
        else:
            sql = """SELECT player_name, SUM(at_bats) AS at_bats, SUM(hits) AS hits,
SUM(home_runs) AS home_runs, SUM(rbi) AS rbi FROM kbo.v_player_game_batting
WHERE season=%s AND player_name IN (%s,%s) GROUP BY player_name ORDER BY player_name"""
            fields = ["hits", "home_runs", "rbi"]
        return self._accept("comparison", f"{names[0]} · {names[1]} 비교", sql, (season, names[0], names[1]), {"type": "bar", "category": "player_name", "fields": fields})

    def _trend(self, text: str, season: int, name: str, pitching: bool) -> QueryPlan:
        if pitching:
            sql = """SELECT game_date, innings_outs, strikeouts, earned_runs, pitches
FROM kbo.v_player_game_pitching WHERE season=%s AND player_name=%s ORDER BY game_date"""
            fields = ["strikeouts", "earned_runs"]
        else:
            sql = """SELECT game_date, at_bats, hits, home_runs, rbi
FROM kbo.v_player_game_batting WHERE season=%s AND player_name=%s ORDER BY game_date"""
            fields = ["hits", "home_runs"]
        return self._accept("trend", f"{season} {name} 경기별 추이", sql, (season, name), {"type": "line", "x": "game_date", "fields": fields})

    def _ranking(self, text: str, season: int, pitching: bool) -> QueryPlan:
        if pitching:
            sql = """SELECT player_name, SUM(strikeouts) AS value FROM kbo.v_player_game_pitching
WHERE season=%s GROUP BY player_name ORDER BY value DESC"""
            metric = "탈삼진"
        else:
            sql = """SELECT player_name, SUM(home_runs) AS value FROM kbo.v_player_game_batting
WHERE season=%s GROUP BY player_name ORDER BY value DESC"""
            metric = "홈런"
        return self._accept("ranking", f"{season} {metric} 순위", sql, (season,), {"type": "bar", "category": "player_name", "fields": ["value"]})

    @staticmethod
    def _accept(kind: str, title: str, sql: str, params: tuple[Any, ...], chart: dict[str, Any]) -> QueryPlan:
        return QueryPlan(True, kind, title, validate_readonly_sql(sql, 100), params, chart, "조회 계획이 준비되었습니다.")

    @staticmethod
    def _season(text: str) -> int:
        match = re.search(r"\b(20\d{2})\b", text)
        return int(match.group(1)) if match else 2026

    @staticmethod
    def _names(text: str) -> list[str]:
        scrubbed = re.sub(r"20\d{2}년?", " ", text)
        scrubbed = re.sub(r"(성적|조회|비교|대결|추이|변화|순위|랭킹|보여줘|알려줘|알려|보여|누구야|경기별|최근|이번|올해|시즌|홈런|타율|OPS|ERA|평균자책|탈삼진|WHIP|타점|안타|이닝|투수|타자|와|과|의|을|를)", " ", scrubbed, flags=re.IGNORECASE)
        tokens = re.findall(r"[가-힣]{2,4}", scrubbed)
        return [token for token in tokens if token not in TEAM_NAMES][:3]
