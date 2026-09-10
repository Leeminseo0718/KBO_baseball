from __future__ import annotations

import re


class UnsafeQuery(ValueError):
    pass


ALLOWED_RELATIONS = {
    "kbo.v_player_game_batting",
    "kbo.v_player_game_pitching",
    "kbo.game",
    "kbo.team",
}
FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy|call|execute|do|vacuum|analyze|pg_sleep)\b",
    re.IGNORECASE,
)
RELATION = re.compile(r"\b(?:from|join)\s+([a-zA-Z_][\w.]*)", re.IGNORECASE)


def validate_readonly_sql(sql: str, max_limit: int = 500) -> str:
    normalized = " ".join(sql.strip().split())
    if not re.match(r"^(select|with)\b", normalized, re.IGNORECASE):
        raise UnsafeQuery("SELECT 또는 WITH 쿼리만 허용됩니다.")
    if ";" in normalized.rstrip(";"):
        raise UnsafeQuery("다중 SQL 문장은 허용되지 않습니다.")
    if FORBIDDEN.search(normalized):
        raise UnsafeQuery("데이터를 변경하거나 서버를 제어하는 SQL은 허용되지 않습니다.")
    relations = {match.lower() for match in RELATION.findall(normalized)}
    if not relations or not relations.issubset(ALLOWED_RELATIONS):
        raise UnsafeQuery(f"허용되지 않은 테이블 또는 뷰입니다: {sorted(relations - ALLOWED_RELATIONS)}")
    limit_match = re.search(r"\blimit\s+(\d+)\b", normalized, re.IGNORECASE)
    if limit_match and int(limit_match.group(1)) > max_limit:
        raise UnsafeQuery(f"최대 {max_limit}행까지만 조회할 수 있습니다.")
    if not limit_match:
        normalized = f"{normalized.rstrip(';')} LIMIT {max_limit}"
    return normalized

