from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from kbo_data.http import HttpClient
from kbo_data.sources.naver import NaverSportsClient


KST = timezone(timedelta(hours=9))
STATUS_LABELS = {
    "BEFORE": "경기 예정",
    "STARTED": "경기 중",
    "LIVE": "경기 중",
    "PLAYING": "경기 중",
    "SUSPENDED": "일시 중단",
    "RESULT": "경기 종료",
    "CANCEL": "경기 취소",
    "CANCELED": "경기 취소",
}


def _integer(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _team(game: dict[str, Any], side: str) -> dict[str, Any]:
    prefix = "away" if side == "away" else "home"
    innings = game.get(f"{prefix}TeamScoreByInning")
    return {
        "code": game.get(f"{prefix}TeamCode"),
        "name": game.get(f"{prefix}TeamName"),
        "score": _integer(game.get(f"{prefix}TeamScore")),
        "scoreByInning": innings if isinstance(innings, (list, dict)) else [],
        "rheb": game.get(f"{prefix}TeamRheb") or {},
    }


def build_snapshot(schedule_payload: dict[str, Any], game_date: date) -> dict[str, Any]:
    games = schedule_payload.get("result", {}).get("games", [])
    compact_games = []
    for game in games:
        status = str(game.get("statusCode") or "UNKNOWN")
        compact_games.append(
            {
                "gameId": str(game.get("gameId") or ""),
                "date": str(game.get("gameDate") or game_date.isoformat()),
                "dateTime": game.get("gameDateTime"),
                "status": status,
                "statusLabel": STATUS_LABELS.get(status, str(game.get("statusInfo") or status)),
                "stadium": game.get("stadium"),
                "currentInning": str(game.get("currentInning") or ""),
                "away": _team(game, "away"),
                "home": _team(game, "home"),
            }
        )
    compact_games.sort(key=lambda item: (str(item.get("dateTime") or ""), item["gameId"]))
    live_statuses = {"STARTED", "LIVE", "PLAYING", "SUSPENDED"}
    return {
        "schemaVersion": 1,
        "source": "naver_sports",
        "date": game_date.isoformat(),
        "liveGameCount": sum(1 for game in compact_games if game["status"] in live_statuses),
        "games": compact_games,
    }


def write_if_changed(path: Path, snapshot: dict[str, Any]) -> bool:
    existing: dict[str, Any] | None = None
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = None
    comparable_existing = {key: value for key, value in (existing or {}).items() if key != "generatedAt"}
    if comparable_existing == snapshot:
        return False
    payload = {**snapshot, "generatedAt": datetime.now(KST).isoformat(timespec="seconds")}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a compact public KBO schedule and live-score snapshot")
    parser.add_argument("--date", default=datetime.now(KST).date().isoformat())
    parser.add_argument("--output", default="dist/data/live.json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    game_date = date.fromisoformat(args.date)
    client = NaverSportsClient(HttpClient(interval_seconds=0))
    schedule = client.schedule(game_date)
    snapshot = build_snapshot(schedule.payload, game_date)
    changed = write_if_changed(Path(args.output), snapshot)
    print(json.dumps({"date": args.date, "games": len(snapshot["games"]), "live": snapshot["liveGameCount"], "changed": changed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
