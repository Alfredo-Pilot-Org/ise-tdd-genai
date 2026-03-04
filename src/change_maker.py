"""Make change with fewest coins; prefer larger coins on ties."""

DEFAULT_COINS = [25, 10, 5, 1]


def make_change(amount_cents: int, coins: list[int] | None = None) -> dict[int, int]:
    if amount_cents < 0:
        raise ValueError("amount_cents must be >= 0")
    if coins is None:
        coins = DEFAULT_COINS
    # Don't mutate input: work with a sorted copy
    coins_sorted = sorted(set(coins), reverse=True)
    if amount_cents == 0:
        return {}

    # dp[i] = (min_coins, solution_dict) for amount i
    dp: list[tuple[int, dict[int, int]] | None] = [None] * (amount_cents + 1)
    dp[0] = (0, {})

    for i in range(1, amount_cents + 1):
        best: tuple[int, dict[int, int]] | None = None
        for c in coins_sorted:
            if i < c:
                continue
            prev = dp[i - c]
            if prev is None:
                continue
            new_count = prev[0] + 1
            new_sol = dict(prev[1])
            new_sol[c] = new_sol.get(c, 0) + 1
            if best is None or new_count < best[0]:
                best = (new_count, new_sol)
            elif new_count == best[0]:
                # Tie: prefer larger coins (lex order of sorted desc coin list)
                def coin_list(sol: dict[int, int]) -> list[int]:
                    return sorted(
                        [coin for coin, cnt in sol.items() for _ in range(cnt)],
                        reverse=True,
                    )
                if coin_list(new_sol) > coin_list(best[1]):
                    best = (new_count, new_sol)
        dp[i] = best

    if dp[amount_cents] is None:
        raise ValueError("Exact change impossible")
    return {k: v for k, v in dp[amount_cents][1].items() if v > 0}
