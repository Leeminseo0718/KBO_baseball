from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Iterable

from kbo_data.snapshot import SnapshotEnvelope


class PostgresStore:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def initialize(self, schema_sql: str) -> None:
        import psycopg
        with psycopg.connect(self.database_url) as conn:
            conn.execute(schema_sql)

    def load(self, normalized: dict[str, Any], snapshots: Iterable[SnapshotEnvelope]) -> None:
        import psycopg
        with psycopg.connect(self.database_url) as conn, conn.cursor() as cur:
            for team in normalized["teams"]:
                cur.execute(
                    "INSERT INTO kbo.team(team_id,name,full_name) VALUES (%s,%s,%s) "
                    "ON CONFLICT(team_id) DO UPDATE SET name=excluded.name,full_name=excluded.full_name",
                    (team["team_id"], team["name"], team.get("full_name")),
                )
            for player in normalized["players"]:
                cur.execute(
                    "INSERT INTO kbo.player(player_id,official_name,bats,throws) VALUES (%s,%s,%s,%s) "
                    "ON CONFLICT(player_id) DO UPDATE SET official_name=excluded.official_name",
                    (player["player_id"], player["official_name"], player.get("bats"), player.get("throws")),
                )
            for alias in normalized["aliases"]:
                cur.execute(
                    "INSERT INTO kbo.player_alias(source,source_player_id,alias_name,player_id) VALUES (%s,%s,%s,%s) "
                    "ON CONFLICT(source,source_player_id) DO UPDATE SET alias_name=excluded.alias_name,player_id=excluded.player_id",
                    (alias["source"], alias["source_player_id"], alias["alias_name"], alias["player_id"]),
                )
            game = normalized["game"]
            cur.execute(
                "INSERT INTO kbo.game(game_id,season,game_date,stadium,away_team_id,home_team_id,away_score,home_score,status,source_updated_at) "
                "VALUES (%(game_id)s,%(season)s,%(game_date)s,%(stadium)s,%(away_team_id)s,%(home_team_id)s,%(away_score)s,%(home_score)s,%(status)s,now()) "
                "ON CONFLICT(game_id) DO UPDATE SET away_score=excluded.away_score,home_score=excluded.home_score,status=excluded.status,source_updated_at=now()",
                game,
            )
            self._upsert_rows(cur, "game_batting_stat", normalized["batting"])
            self._upsert_rows(cur, "game_pitching_stat", normalized["pitching"])
            self._upsert_rows(cur, "pitch_event", normalized["pitch_events"])
            for snapshot in snapshots:
                item = asdict(snapshot)
                cur.execute(
                    "INSERT INTO kbo.source_snapshot(source,entity_type,source_key,fetched_at,source_url,sha256,payload) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s::jsonb) ON CONFLICT DO NOTHING",
                    (item["source"], item["entity_type"], item["source_key"], item["fetched_at"], item["source_url"], item["sha256"], json.dumps(item["payload"])),
                )

    @staticmethod
    def _upsert_rows(cur: Any, table: str, rows: list[dict[str, Any]]) -> None:
        allowed = {"game_batting_stat", "game_pitching_stat", "pitch_event"}
        if table not in allowed:
            raise ValueError("Unsupported table")
        for row in rows:
            columns = list(row)
            placeholders = ",".join(["%s"] * len(columns))
            updates = ",".join(f"{column}=excluded.{column}" for column in columns if column not in {"game_id", "team_id", "player_id", "sequence_no"})
            sql = f"INSERT INTO kbo.{table}({','.join(columns)}) VALUES ({placeholders}) ON CONFLICT DO UPDATE SET {updates}"
            cur.execute(sql, tuple(row[column] for column in columns))

