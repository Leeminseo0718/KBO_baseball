from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any
from urllib.parse import urlencode

from kbo_data.http import HttpClient


@dataclass(frozen=True)
class NaverSnapshot:
    entity_type: str
    source_key: str
    url: str
    payload: dict[str, Any]


class NaverSportsClient:
    """Rate-limited adapter for the JSON used by Naver Sports' public game pages.

    These are undocumented web endpoints, so callers must preserve raw responses,
    tolerate schema changes, and avoid high-frequency/live polling by default.
    """

    def __init__(self, http: HttpClient, base_url: str = "https://api-gw.sports.naver.com") -> None:
        self.http = http
        self.base_url = base_url.rstrip("/")

    def schedule(self, game_date: date) -> NaverSnapshot:
        query = urlencode(
            {
                "fields": "all",
                "categoryId": "kbo",
                "fromDate": game_date.isoformat(),
                "toDate": game_date.isoformat(),
                "size": 50,
            }
        )
        url = f"{self.base_url}/schedule/games?{query}"
        return NaverSnapshot("schedule", game_date.isoformat(), url, self.http.get_json(url))

    def game(self, game_id: str) -> NaverSnapshot:
        return self._game_snapshot(game_id, "game", "")

    def record(self, game_id: str) -> NaverSnapshot:
        return self._game_snapshot(game_id, "record", "/record")

    def lineup(self, game_id: str) -> NaverSnapshot:
        return self._game_snapshot(game_id, "lineup", "/lineup")

    def relay_inning(self, game_id: str, inning: int) -> NaverSnapshot:
        suffix = f"/relay?inning={inning}"
        return self._game_snapshot(game_id, "relay", suffix, source_key=f"{game_id}:{inning}")

    def completed_game_ids(self, schedule: NaverSnapshot) -> list[str]:
        return self.game_ids(schedule, mode="completed")

    @staticmethod
    def games(schedule: NaverSnapshot) -> list[dict[str, Any]]:
        return list(schedule.payload.get("result", {}).get("games", []))

    def game_ids(self, schedule: NaverSnapshot, *, mode: str) -> list[str]:
        games = self.games(schedule)
        if mode == "completed":
            selected = [game for game in games if game.get("statusCode") == "RESULT"]
        elif mode == "live":
            terminal = {"BEFORE", "RESULT", "CANCEL", "CANCELED"}
            selected = [game for game in games if str(game.get("statusCode") or "") not in terminal]
        elif mode == "all":
            selected = [game for game in games if game.get("statusCode") not in {"CANCEL", "CANCELED"}]
        else:
            raise ValueError(f"Unsupported collection mode: {mode}")
        return [str(game["gameId"]) for game in selected if game.get("gameId")]

    def _game_snapshot(
        self,
        game_id: str,
        entity_type: str,
        suffix: str,
        *,
        source_key: str | None = None,
    ) -> NaverSnapshot:
        url = f"{self.base_url}/schedule/games/{game_id}{suffix}"
        return NaverSnapshot(entity_type, source_key or game_id, url, self.http.get_json(url))

