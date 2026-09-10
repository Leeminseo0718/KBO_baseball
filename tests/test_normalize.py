from kbo_data.normalize import innings_to_outs


def test_innings_to_outs():
    assert innings_to_outs("6") == 18
    assert innings_to_outs("6.2") == 20
    assert innings_to_outs("0 ⅓") == 1
    assert innings_to_outs("0 ⅔") == 2

