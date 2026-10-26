from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from kbo_data.query_engine import TemplatePlanner


app = FastAPI(title="KBO Data Room API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:4173,http://127.0.0.1:4173,https://baseball-data-room.leeminseo2249.chatgpt.site",
        ).split(",")
        if origin.strip()
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["content-type"],
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=200)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "planner": "template", "database": "configured" if os.getenv("DATABASE_URL") else "not_configured"}


def _database_rows(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    if not os.getenv("DATABASE_URL"):
        raise HTTPException(status_code=503, detail="DATABASE_URL이 설정되지 않았습니다.")
    try:
        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(
            os.environ["DATABASE_URL"],
            options="-c statement_timeout=5000",
            row_factory=dict_row,
        ) as conn:
            conn.read_only = True
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return [dict(row) for row in cur.fetchall()]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="분석 데이터베이스를 조회하지 못했습니다.") from exc


@app.get("/dashboard")
def dashboard() -> dict[str, Any]:
    games = _database_rows(
        """
        SELECT g.game_id, g.game_date, g.stadium, g.status,
               g.away_score, g.home_score, g.source_updated_at,
               away.name AS away_team, home.name AS home_team
        FROM kbo.game g
        JOIN kbo.team away ON away.team_id = g.away_team_id
        JOIN kbo.team home ON home.team_id = g.home_team_id
        ORDER BY CASE WHEN g.status IN ('STARTED','LIVE','PLAYING','SUSPENDED') THEN 0 ELSE 1 END,
                 g.game_date DESC, g.source_updated_at DESC NULLS LAST
        LIMIT 1
        """
    )
    if not games:
        return {"generatedAt": datetime.now(timezone.utc).isoformat(), "latestGame": None, "leaders": [], "quality": {}}
    game = games[0]
    game_id = str(game["game_id"])
    batters = _database_rows(
        """
        SELECT p.official_name AS name, t.name AS team, '타자' AS kind,
               s.at_bats, s.hits, s.home_runs, s.rbi
        FROM kbo.game_batting_stat s
        JOIN kbo.player p USING (player_id)
        JOIN kbo.team t USING (team_id)
        WHERE s.game_id = %s
        ORDER BY s.hits DESC NULLS LAST, s.home_runs DESC NULLS LAST, s.rbi DESC NULLS LAST
        LIMIT 6
        """,
        (game_id,),
    )
    pitchers = _database_rows(
        """
        SELECT p.official_name AS name, t.name AS team, '투수' AS kind,
               s.innings_outs, s.strikeouts, s.earned_runs, s.pitches, s.decision
        FROM kbo.game_pitching_stat s
        JOIN kbo.player p USING (player_id)
        JOIN kbo.team t USING (team_id)
        WHERE s.game_id = %s
        ORDER BY s.innings_outs DESC NULLS LAST, s.strikeouts DESC NULLS LAST
        LIMIT 6
        """,
        (game_id,),
    )
    quality_rows = _database_rows(
        """
        SELECT
          (SELECT count(*) FROM kbo.pitch_event WHERE game_id = %s) AS events,
          (SELECT count(*) FROM kbo.game_batting_stat WHERE game_id = %s) AS batting_rows,
          (SELECT count(*) FROM kbo.game_pitching_stat WHERE game_id = %s) AS pitching_rows,
          (SELECT count(DISTINCT player_id)
             FROM (SELECT player_id FROM kbo.game_batting_stat WHERE game_id = %s
                   UNION
                   SELECT player_id FROM kbo.game_pitching_stat WHERE game_id = %s) identified) AS identified_players
        """,
        (game_id, game_id, game_id, game_id, game_id),
    )
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "latestGame": game,
        "leaders": [*batters[:3], *pitchers[:3]],
        "quality": quality_rows[0] if quality_rows else {},
    }


@app.get("/games/latest")
def latest_games(limit: int = 10) -> dict[str, Any]:
    safe_limit = max(1, min(limit, 50))
    rows = _database_rows(
        """
        SELECT g.game_id, g.game_date, g.stadium, g.status,
               g.away_score, g.home_score, g.source_updated_at,
               away.name AS away_team, home.name AS home_team
        FROM kbo.game g
        JOIN kbo.team away ON away.team_id = g.away_team_id
        JOIN kbo.team home ON home.team_id = g.home_team_id
        ORDER BY g.game_date DESC, g.source_updated_at DESC NULLS LAST
        LIMIT %s
        """,
        (safe_limit,),
    )
    return {"games": rows}


@app.post("/query")
def query(request: QuestionRequest) -> dict[str, Any]:
    plan = TemplatePlanner().plan(request.question)
    response = {"plan": plan.public_dict(), "columns": [], "rows": []}
    if not plan.accepted or not os.getenv("DATABASE_URL"):
        return response
    try:
        rows = _database_rows(plan.sql, tuple(plan.params))
        response["columns"] = list(rows[0]) if rows else []
        response["rows"] = [list(row.values()) for row in rows]
    except Exception as exc:
        raise HTTPException(status_code=503, detail="분석 데이터베이스를 조회하지 못했습니다.") from exc
    return response


def main() -> None:
    import uvicorn
    uvicorn.run("kbo_data.api:app", host="127.0.0.1", port=8000)

