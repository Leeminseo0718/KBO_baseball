from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from kbo_data.http import HttpClient
from kbo_data.normalize import normalize_game
from kbo_data.snapshot import SnapshotEnvelope, make_envelope, write_envelope
from kbo_data.sources.kbo import KboOfficialClient
from kbo_data.sources.naver import NaverSnapshot, NaverSportsClient
from kbo_data.storage import PostgresStore


def _current_inning(game_payload: dict) -> int:
    game = game_payload.get("result", {}).get("game", {})
    match = re.search(r"\d+", str(game.get("currentInning") or game.get("inning") or ""))
    return max(1, min(15, int(match.group()))) if match else 1


def collect_game(
    client: NaverSportsClient,
    game_id: str,
    raw_dir: Path,
    *,
    mode: str = "completed",
) -> tuple[dict, list[SnapshotEnvelope]]:
    game_snapshot = client.game(game_id)
    snapshots: list[NaverSnapshot] = [game_snapshot]
    record_payload: dict = {}
    for fetch in (client.record, client.lineup):
        try:
            snapshot = fetch(game_id)
            snapshots.append(snapshot)
            if snapshot.entity_type == "record":
                record_payload = snapshot.payload
        except RuntimeError:
            if mode != "live":
                raise

    if mode == "live":
        current = _current_inning(game_snapshot.payload)
        innings = range(max(1, current - 1), current + 1)
    else:
        innings = range(1, 16)

    empty_streak = 0
    for inning in innings:
        snapshot = client.relay_inning(game_id, inning)
        relay = snapshot.payload.get("result", {}).get("textRelayData") or {}
        if relay.get("textRelays"):
            snapshots.append(snapshot)
            empty_streak = 0
        else:
            empty_streak += 1
            if mode != "live" and inning >= 9 and empty_streak >= 2:
                break
    envelopes = [make_envelope(item) for item in snapshots]
    for envelope in envelopes:
        write_envelope(envelope, raw_dir)
    normalized = normalize_game(
        game_snapshot.payload,
        record_payload,
        [snapshot.payload for snapshot in snapshots if snapshot.entity_type == "relay"],
    )
    return normalized, envelopes


def run(args: argparse.Namespace) -> dict:
    interval = float(os.getenv("REQUEST_INTERVAL_SECONDS", "1.2"))
    http = HttpClient(interval_seconds=interval)
    naver = NaverSportsClient(http, os.getenv("NAVER_API_BASE", "https://api-gw.sports.naver.com"))
    game_date = date.fromisoformat(args.date)
    raw_dir = Path(args.data_dir) / "raw"
    normalized_dir = Path(args.data_dir) / "normalized"
    raw_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)

    schedule = naver.schedule(game_date)
    schedule_envelope = make_envelope(schedule)
    write_envelope(schedule_envelope, raw_dir)
    game_ids = [args.game_id] if args.game_id else naver.game_ids(schedule, mode=args.mode)
    report = {"date": args.date, "mode": args.mode, "game_ids": game_ids, "games": [], "errors": [], "player_verifications": []}

    database_url = os.getenv("DATABASE_URL")
    store = PostgresStore(database_url) if args.load_db and database_url else None
    if args.load_db and not store:
        raise RuntimeError("DATABASE_URL is required with --load-db")
    if store:
        store.initialize(Path("db/schema.sql").read_text(encoding="utf-8"))

    for game_id in game_ids:
        try:
            normalized, envelopes = collect_game(naver, game_id, raw_dir, mode=args.mode)
        except Exception as exc:
            if args.mode != "live":
                raise
            report["errors"].append({"game_id": game_id, "error": str(exc)})
            continue
        output_path = normalized_dir / f"{game_id}.json"
        output_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
        report["games"].append({"game_id": game_id, **normalized["quality"], "output": str(output_path)})
        if store:
            store.load(normalized, [schedule_envelope, *envelopes])

    if args.verify_player:
        kbo = KboOfficialClient(http, os.getenv("KBO_BASE_URL", "https://www.koreabaseball.com"))
        for item in args.verify_player:
            player_id, expected_name = item.split(":", 1)
            report["player_verifications"].append(asdict(kbo.verify_player(player_id, expected_name)))

    report_path = normalized_dir / f"report-{args.date}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect completed KBO games from Naver Sports")
    parser.add_argument("--date", default=(datetime.now(timezone.utc) + timedelta(hours=9) - timedelta(days=1)).date().isoformat())
    parser.add_argument("--game-id")
    parser.add_argument("--mode", choices=("completed", "live", "all"), default="completed")
    parser.add_argument("--verify-player", action="append", metavar="PLAYER_ID:NAME")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--load-db", action="store_true")
    return parser


def main() -> None:
    print(json.dumps(run(build_parser().parse_args()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

