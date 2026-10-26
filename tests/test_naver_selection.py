from kbo_data.sources.naver import NaverSnapshot, NaverSportsClient


def schedule(*statuses: str) -> NaverSnapshot:
    games = [{"gameId": f"game-{index}", "statusCode": status} for index, status in enumerate(statuses)]
    return NaverSnapshot("schedule", "2026-10-26", "https://example.test", {"result": {"games": games}})


def test_game_ids_are_filtered_by_collection_mode():
    client = NaverSportsClient(http=None)  # type: ignore[arg-type]
    snapshot = schedule("BEFORE", "STARTED", "RESULT", "CANCEL")

    assert client.game_ids(snapshot, mode="completed") == ["game-2"]
    assert client.game_ids(snapshot, mode="live") == ["game-1"]
    assert client.game_ids(snapshot, mode="all") == ["game-0", "game-1", "game-2"]


def test_unknown_collection_mode_is_rejected():
    client = NaverSportsClient(http=None)  # type: ignore[arg-type]
    try:
        client.game_ids(schedule("RESULT"), mode="future")
    except ValueError as exc:
        assert "Unsupported collection mode" in str(exc)
    else:
        raise AssertionError("unknown mode must raise ValueError")
