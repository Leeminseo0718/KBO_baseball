from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from kbo_data.query_engine import TemplatePlanner


app = FastAPI(title="KBO Data Room API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:4173").split(",") if origin],
    allow_methods=["GET", "POST"],
    allow_headers=["content-type"],
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=200)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "planner": "template", "database": "configured" if os.getenv("DATABASE_URL") else "not_configured"}


@app.post("/query")
def query(request: QuestionRequest) -> dict[str, Any]:
    plan = TemplatePlanner().plan(request.question)
    response = {"plan": plan.public_dict(), "columns": [], "rows": []}
    if not plan.accepted or not os.getenv("DATABASE_URL"):
        return response
    try:
        import psycopg
        with psycopg.connect(os.environ["DATABASE_URL"], options="-c statement_timeout=5000") as conn:
            conn.read_only = True
            with conn.cursor() as cur:
                cur.execute(plan.sql, plan.params)
                response["columns"] = [column.name for column in cur.description or []]
                response["rows"] = [list(row) for row in cur.fetchall()]
    except Exception as exc:
        raise HTTPException(status_code=503, detail="분석 데이터베이스를 조회하지 못했습니다.") from exc
    return response


def main() -> None:
    import uvicorn
    uvicorn.run("kbo_data.api:app", host="127.0.0.1", port=8000)

