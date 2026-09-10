from __future__ import annotations

from typing import Any, Iterable


def innings_to_outs(value: str | int | float | None) -> int | None:
    if value is None or value == "":
        return None
    text = str(value).strip().replace("⅓", "1/3").replace("⅔", "2/3")
    if " " in text:
        whole, fraction = text.split(" ", 1)
    elif "." in text:
        whole, remainder = text.split(".", 1)
        fraction = f"{remainder}/3"
    else:
        whole, fraction = text, "0/3"
    numerator = int(fraction.split("/", 1)[0]) if "/" in fraction else 0
    return int(whole) * 3 + numerator


def normalize_game(
    game_payload: dict[str, Any],
    record_payload: dict[str, Any],
    relay_payloads: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    game = game_payload["result"]["game"]
    record = record_payload.get("result", {}).get("recordData") or {}
    teams = [
        {"team_id": game["awayTeamCode"], "name": game["awayTeamName"], "full_name": game.get("awayTeamFullName")},
        {"team_id": game["homeTeamCode"], "name": game["homeTeamName"], "full_name": game.get("homeTeamFullName")},
    ]
    normalized = {
        "game": {
            "game_id": game["gameId"],
            "season": int(game["seasonYear"]),
            "game_date": game["gameDate"],
            "stadium": game.get("stadium"),
            "away_team_id": game["awayTeamCode"],
            "home_team_id": game["homeTeamCode"],
            "away_score": int(game.get("awayTeamScore") or 0),
            "home_score": int(game.get("homeTeamScore") or 0),
            "status": game["statusCode"],
        },
        "teams": teams,
        "players": [],
        "aliases": [],
        "batting": [],
        "pitching": [],
        "pitch_events": [],
        "quality": {},
    }
    seen_players: dict[str, dict[str, Any]] = {}

    def remember(player_id: Any, name: Any, **extra: Any) -> None:
        if not player_id or not name:
            return
        key = str(player_id)
        seen_players[key] = {"player_id": key, "official_name": str(name), **extra}

    boxscore = record.get("battersBoxscore") or {}
    for side, team_id in (("away", game["awayTeamCode"]), ("home", game["homeTeamCode"])):
        for batter in boxscore.get(side) or []:
            player_id = str(batter.get("playerCode") or batter.get("pcode") or "")
            remember(player_id, batter.get("name"))
            if not player_id:
                continue
            normalized["batting"].append(
                {
                    "game_id": game["gameId"], "team_id": team_id, "player_id": player_id,
                    "batting_order": batter.get("batOrder"), "plate_appearances": batter.get("pa"),
                    "at_bats": batter.get("ab"), "hits": batter.get("hit"), "home_runs": batter.get("hr"),
                    "walks": batter.get("bb"), "strikeouts": batter.get("kk"), "runs": batter.get("run"),
                    "rbi": batter.get("rbi"), "stolen_bases": batter.get("sb"),
                }
            )

    pitchers = record.get("pitchersBoxscore") or {}
    for side, team_id in (("away", game["awayTeamCode"]), ("home", game["homeTeamCode"])):
        for pitcher in pitchers.get(side) or []:
            player_id = str(pitcher.get("pcode") or "")
            remember(player_id, pitcher.get("name"))
            if not player_id:
                continue
            normalized["pitching"].append(
                {
                    "game_id": game["gameId"], "team_id": team_id, "player_id": player_id,
                    "innings_outs": innings_to_outs(pitcher.get("inn")), "batters_faced": pitcher.get("pa"),
                    "hits": pitcher.get("hit"), "home_runs": pitcher.get("hr"), "walks": pitcher.get("bb"),
                    "strikeouts": pitcher.get("kk"), "runs": pitcher.get("r"), "earned_runs": pitcher.get("er"),
                    "pitches": pitcher.get("bf"), "decision": pitcher.get("wls") or None,
                }
            )

    event_by_seq: dict[int, dict[str, Any]] = {}
    for relay_payload in relay_payloads:
        relay = relay_payload.get("result", {}).get("textRelayData") or {}
        for group in relay.get("textRelays") or []:
            inning = int(group.get("inn") or 0)
            half = "top" if str(group.get("homeOrAway")) == "0" else "bottom"
            for option in group.get("textOptions") or []:
                seq = option.get("seqno")
                text = str(option.get("text") or "").strip()
                state = option.get("currentGameState") or {}
                if seq is None or not text:
                    continue
                event_by_seq[int(seq)] = {
                    "game_id": game["gameId"], "sequence_no": int(seq), "inning": inning, "half": half,
                    "batter_id": str(state.get("batter") or "") or None,
                    "pitcher_id": str(state.get("pitcher") or "") or None,
                    "balls": _int_or_none(state.get("ball")), "strikes": _int_or_none(state.get("strike")),
                    "outs": _int_or_none(state.get("out")), "event_text": text,
                    "raw_event_type": _int_or_none(option.get("type")),
                }
                batter = option.get("batterRecord") or {}
                remember(batter.get("pcode"), batter.get("name"), bats=batter.get("hitType"))

    normalized["pitch_events"] = [event_by_seq[key] for key in sorted(event_by_seq)]
    normalized["players"] = list(seen_players.values())
    normalized["aliases"] = [
        {"source": "naver", "source_player_id": p["player_id"], "alias_name": p["official_name"], "player_id": p["player_id"]}
        for p in normalized["players"]
    ]
    normalized["quality"] = {
        "event_count": len(normalized["pitch_events"]),
        "batting_row_count": len(normalized["batting"]),
        "pitching_row_count": len(normalized["pitching"]),
        "player_count": len(normalized["players"]),
        "score_matches_record": _score_matches(game, record),
    }
    return normalized


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _score_matches(game: dict[str, Any], record: dict[str, Any]) -> bool:
    batting = record.get("battersBoxscore") or {}
    away = batting.get("awayTotal") or {}
    home = batting.get("homeTotal") or {}
    return int(away.get("run") or 0) == int(game.get("awayTeamScore") or 0) and int(home.get("run") or 0) == int(game.get("homeTeamScore") or 0)

