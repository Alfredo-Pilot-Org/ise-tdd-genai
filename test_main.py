import pytest

# GenAI will implement:
#   make_change(amount_cents: int, coins: list[int] | None = None) -> dict[int, int]
#
# Requirements:
# - Return a dict {coin_value: count} using the FEWEST coins possible.
# - Default US coins: [25, 10, 5, 1]
# - Always prefer larger coins when multiple solutions have same #coins.
# - amount_cents must be >= 0 else raise ValueError.
# - If exact change is impossible with provided coins, raise ValueError.
# - Must NOT mutate the `coins` list passed in.
# - Result should not include coins with count 0.

def test_zero_returns_empty_dict():
    from src.change_maker import make_change
    assert make_change(0) == {}

def test_simple_quarter_dime_penny():
    from src.change_maker import make_change
    assert make_change(41) == {25: 1, 10: 1, 5: 1, 1: 1}

def test_fewest_coins_not_greedy_for_noncanonical_system():
    # Greedy fails here:
    # coins = [10, 6, 1], amount=12
    # greedy picks 10+1+1 (3 coins)
    # optimal is 6+6 (2 coins)
    from src.change_maker import make_change
    assert make_change(12, coins=[10, 6, 1]) == {6: 2}

def test_tie_breaker_prefers_larger_coins():
    # For coins [4,3,2,1] and amount 6:
    # 3+3 uses 2 coins
    # 4+2 uses 2 coins (tie on #coins)
    # We prefer larger coins -> 4+2
    from src.change_maker import make_change
    assert make_change(6, coins=[4, 3, 2, 1]) == {4: 1, 2: 1}

def test_impossible_exact_change_raises():
    from src.change_maker import make_change
    with pytest.raises(ValueError):
        make_change(3, coins=[2, 4])  # cannot make 3

def test_negative_amount_raises():
    from src.change_maker import make_change
    with pytest.raises(ValueError):
        make_change(-1)

def test_does_not_mutate_coins_list():
    from src.change_maker import make_change
    coins = [10, 6, 1]
    _ = make_change(12, coins=coins)
    assert coins == [10, 6, 1], "make_change must not mutate the coins list"