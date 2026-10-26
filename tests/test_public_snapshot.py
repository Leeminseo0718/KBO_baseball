import json
from datetime import date

from kbo_data.public_snapshot import build_snapshot, write_if_changed


def test_build_snapshot_keeps_scores_and_counts_live_games():
    payload = {
        "result": {
            "games": [
                {
                    "gameId": "game-1",
                    "gameDate": "2026-10-26",
                    "statusCode": "STARTED",
                    "statusInfo": "3회말",
                    "currentInning": "3회말",
                    "awayTeamCode": "HT",
                    "awayTeamName": "KIA",
                    "awayTeamScore": "1",
                    "awayTeamScoreByInning": [0, 1, 0],
                    "homeTeamCode": "SS",
                    "homeTeamName": "삼성",
                    "homeTeamScore": 2,
                    "homeTeamScoreByInning": [2, 0, "-"],
                }
            ]
        }
    }

    snapshot = build_snapshot(payload, date(2026, 10, 26))

    assert snapshot["liveGameCount"] == 1
    assert snapshot["games"][0]["statusLabel"] == "경기 중"
    assert snapshot["games"][0]["away"]["score"] == 1
    assert snapshot["games"][0]["home"]["name"] == "삼성"


def test_write_if_changed_ignores_generated_at(tmp_path):
    path = tmp_path / "live.json"
    snapshot = {"schemaVersion": 1, "games": []}

    assert write_if_changed(path, snapshot) is True
    first = json.loads(path.read_text(encoding="utf-8"))
    assert "generatedAt" in first
    assert write_if_changed(path, snapshot) is False
