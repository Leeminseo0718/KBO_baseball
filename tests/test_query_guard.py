import pytest

from kbo_data.query_guard import UnsafeQuery, validate_readonly_sql


def test_adds_limit_to_allowed_view():
    sql = validate_readonly_sql("SELECT player_name FROM kbo.v_player_game_batting")
    assert sql.endswith("LIMIT 500")


@pytest.mark.parametrize("sql", [
    "DELETE FROM kbo.game",
    "SELECT * FROM pg_catalog.pg_user",
    "SELECT * FROM kbo.game; DROP TABLE kbo.game",
    "SELECT pg_sleep(10) FROM kbo.game",
])
def test_rejects_unsafe_sql(sql):
    with pytest.raises(UnsafeQuery):
        validate_readonly_sql(sql)

