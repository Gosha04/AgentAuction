import numpy as np

# ------------------------------------------------------------
# Auction Strategy Simulator - 75 Minute In-Class Activity
# CPSC 370: Agentic AI Systems
# ------------------------------------------------------------
# Complete the TODO sections in order.
#
# The goal is NOT to build an auction framework. The goal is to
# use simulation to study strategic behavior under first-price
# and second-price sealed-bid auctions.
# ------------------------------------------------------------

SEED = 42
N_AGENTS = 6
N_TRIALS = 2000


def first_price(valuations, bids):
    """Run one first-price sealed-bid auction.

    Highest bid wins. Winner pays their own bid.

    Returns
    -------
    winner : int
        Index of winning bidder.
    price : float
        Price paid by winner.
    utilities : np.ndarray
        Utility for every bidder. Losers receive 0.
    """

    winner = int(np.argmax(bids))

    price = bids[winner]

    utilities = np.zeros(len(bids), dtype=float)

    utilities[winner] = valuations[winner] - price

    return winner, price, utilities


def second_price(valuations, bids):
    """Run one second-price (Vickrey) sealed-bid auction.

    Highest bid wins. Winner pays the second-highest bid.
    """
   
    order = np.argsort(bids)

    winner = int(order[-1])

    price = bids[order[-2]]

    utilities = np.zeros(len(bids), dtype=float)

    utilities[winner] = valuations[winner] - price

    return winner, price, utilities


def run_trials(mechanism, bid_rule, n_agents=N_AGENTS,
               trials=N_TRIALS, seed=SEED):
    """Run many auctions and report aggregate performance."""

    rng = np.random.default_rng(seed)

    revenue = []
    winner_utility = []
    efficient = []

    for _ in range(trials):
        values = rng.integers(10, 101, size=n_agents)
        bids = np.asarray(bid_rule(values), dtype=float)

        winner, price, utilities = mechanism(values, bids)

        revenue.append(price)
        winner_utility.append(utilities[winner])

        # Allocation is efficient when the highest-value agent wins.
        efficient.append(winner == np.argmax(values))

    return {
        "average_revenue": float(np.mean(revenue)),
        "average_winner_utility": float(np.mean(winner_utility)),
        "efficiency_rate": float(np.mean(efficient)),
    }


def focal_bidder_experiment(focal_shade, opponent_shade=0.80,
                             n_agents=N_AGENTS,
                             trials=N_TRIALS, seed=SEED):
    """Measure Agent 0's first-price performance.

    Agent 0 bids focal_shade * its valuation.
    Every opponent bids opponent_shade * valuation.
    """

    rng = np.random.default_rng(seed)

    focal_utility = []
    focal_wins = []

    for _ in range(trials):
        values = rng.integers(10, 101, size=n_agents)

        bids = opponent_shade * values.astype(float)
        bids[0] = focal_shade * values[0]

        winner, price, utilities = first_price(values, bids)

        focal_utility.append(utilities[0])
        focal_wins.append(winner == 0)

    return {
        "shade": float(focal_shade),
        "average_utility": float(np.mean(focal_utility)),
        "win_rate": float(np.mean(focal_wins)),
    }


def custom_bidder_experiment(bid_rule, opponent_shade=0.80,
                             n_agents=N_AGENTS,
                             trials=N_TRIALS, seed=SEED):
    """Measure Agent 0's first-price performance with a custom rule.

    Agent 0 bids bid_rule(its valuation).
    Every opponent bids opponent_shade * valuation.
    """

    rng = np.random.default_rng(seed)

    focal_utility = []
    focal_wins = []

    for _ in range(trials):
        values = rng.integers(10, 101, size=n_agents)

        bids = opponent_shade * values.astype(float)
        bids[0] = bid_rule(values[0])

        winner, price, utilities = first_price(values, bids)

        focal_utility.append(utilities[0])
        focal_wins.append(winner == 0)

    return {
        "average_utility": float(np.mean(focal_utility)),
        "win_rate": float(np.mean(focal_wins)),
    }


def truthfulness_test_second_price(multiplier,
                                   n_agents=N_AGENTS,
                                   trials=N_TRIALS,
                                   seed=SEED):
    """Test one focal bidder in second-price auctions.

    Agent 0 bids multiplier * true value.
    Everyone else bids truthfully.
    """
    rng = np.random.default_rng(seed)

    utilities = []
    wins = []
    negative_utility = []

    for _ in range(trials):
        values = rng.integers(10, 101, size=n_agents).astype(float)
        bids = values.copy()
        bids[0] = multiplier * values[0]

        winner, price, u = second_price(values, bids)

        utilities.append(u[0])
        wins.append(winner == 0)
        negative_utility.append(u[0] < 0)

    return {
        "multiplier": float(multiplier),
        "average_utility": float(np.mean(utilities)),
        "win_rate": float(np.mean(wins)),
        "negative_utility_rate": float(np.mean(negative_utility)),
    }


def print_summary(label, result):
    print(f"\n{label}")
    print("-" * len(label))
    for key, value in result.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")


def main():
    # ========================================================
    # PART 1 - Implement and sanity-check the mechanisms
    # ========================================================
    rng = np.random.default_rng(SEED)
    values = rng.integers(10, 101, size=N_AGENTS)

    print("TRUE VALUATIONS:", values)

    first_bids = 0.80 * values
    print("\nFirst-price bids (80% shading):", first_bids)
    print("First-price result:", first_price(values, first_bids))

    second_bids = values.copy()
    print("\nSecond-price bids (truthful):", second_bids)
    print("Second-price result:", second_price(values, second_bids))

    # ========================================================
    # PART 2 - Compare mechanisms over many auctions
    # ========================================================
    fp = run_trials(
        first_price,
        bid_rule=lambda v: 0.80 * v,
    )

    sp = run_trials(
        second_price,
        bid_rule=lambda v: v.copy(),
    )

    print_summary("FIRST PRICE: all bid 80% of value", fp)
    print_summary("SECOND PRICE: truthful bidding", sp)

    # ========================================================
    # PART 3 - Empirically test truthfulness in second price
    # ========================================================
    print("\nSECOND-PRICE TRUTHFULNESS EXPERIMENT")

    for multiplier in [0.50, 0.75, 1.00, 1.25, 1.50]:
        result = truthfulness_test_second_price(multiplier)
        print_summary(f"Agent 0 bid multiplier = {multiplier:.2f}", result)

    # ========================================================
    # PART 4 - First-price strategy search
    # ========================================================
    print("\nFIRST-PRICE STRATEGY SEARCH")
    print("All opponents bid 80% of their value.")

    # TODO 8:
    # Replace the short list below with a grid from 0.50 to 1.00
    # in increments of 0.05. Hint: np.arange(0.50, 1.001, 0.05)
    shades = np.arange(0.50, 1.001, 0.05)

    results = []

    for shade in shades:
        result = focal_bidder_experiment(
            focal_shade=shade,
            opponent_shade=0.80,
        )
        results.append(result)
        print_summary(f"Agent 0 shade = {shade:.2f}", result)

    # TODO 9:
    # Find the shade with the highest average_utility.
    # Print that shade and its average utility.
    best = max(results, key=lambda r: r["average_utility"])
    print_summary("BEST SHADE", best)

    # ========================================================
    # PART 5 - What changes as competition increases?
    # ========================================================
    print("\nCOMPETITION EXPERIMENT")

    for n_agents in [2, 4, 6, 10]:
        # A useful theoretical benchmark for uniformly distributed
        # independent private values in a symmetric first-price
        # auction is (n-1)/n times valuation.
        theoretical_shade = (n_agents - 1) / n_agents

        fp_n = run_trials(
            first_price,
            bid_rule=lambda v, s=theoretical_shade: s * v,
            n_agents=n_agents,
        )

        sp_n = run_trials(
            second_price,
            bid_rule=lambda v: v.copy(),
            n_agents=n_agents,
        )

        print(f"\n--- {n_agents} BIDDERS ---")
        print(f"First-price benchmark shade: {theoretical_shade:.3f}")
        print_summary("First price", fp_n)
        print_summary("Second price", sp_n)

    # ========================================================
    # PART 6 - Create your own strategic agent
    # ========================================================
    # Bid 85% of value, but never more than 80. Opponents bid
    # 80% of a value that is at most 100, so none can bid above 80.
    custom = custom_bidder_experiment(lambda v: min(0.85 * v, 80))
    print_summary("CUSTOM AGENT: bid = min(0.85 * value, 80)", custom)


if __name__ == "__main__":
    main()
