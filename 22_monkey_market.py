from aoc import Input, run, TestCase
from collections import defaultdict


# Puzzle constants
PRUNE_MODULO = 16777216  # 2^24
SECRET_MULTIPLY_1 = 64
SECRET_DIVIDE = 32
SECRET_MULTIPLY_2 = 2048
ITERATIONS = 2000
PRICE_MODULO = 10
SEQUENCE_LENGTH = 4


def mix(value, secret):
    """Mix a value into the secret number using bitwise XOR."""
    return value ^ secret


def prune(secret):
    """Prune the secret number using modulo."""
    return secret % PRUNE_MODULO


def next_secret(secret):
    """Generate the next secret number in the sequence."""
    # Step 1: multiply, mix, and prune
    secret = prune(mix(secret * SECRET_MULTIPLY_1, secret))

    # Step 2: divide (round down), mix, and prune
    secret = prune(mix(secret // SECRET_DIVIDE, secret))

    # Step 3: multiply, mix, and prune
    secret = prune(mix(secret * SECRET_MULTIPLY_2, secret))

    return secret


def generate_nth_secret(initial, n):
    """Generate the nth secret number from an initial secret."""
    secret = initial
    for _ in range(n):
        secret = next_secret(secret)
    return secret


def sum_final_secrets(data_file):
    """Sum the final evolved secret numbers for all buyers."""
    initial_secrets = [int(line) for line in Input(data_file).as_lines()]

    return sum(generate_nth_secret(secret, ITERATIONS) for secret in initial_secrets)


def generate_price_sequence(initial_secret, iterations):
    """
    Generate sequence of prices from secret number evolution.
    """
    secret = initial_secret
    prices = [secret % PRICE_MODULO]

    for _ in range(iterations):
        secret = next_secret(secret)
        prices.append(secret % PRICE_MODULO)

    changes = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]

    return prices, changes


def find_first_occurrence_prices(prices, changes):
    """
    Find the price at first occurrence of each change sequence for a buyer.
    """
    first_occurrence = {}

    for i in range(len(changes) - SEQUENCE_LENGTH + 1):
        sequence = tuple(changes[i : i + SEQUENCE_LENGTH])

        if sequence not in first_occurrence:
            first_occurrence[sequence] = prices[i + SEQUENCE_LENGTH]

    return first_occurrence


def maximize_banana_profit(data_file):
    """
    Find optimal change sequence to maximize total bananas across all buyers.

    Each buyer sells once at the first occurrence of the chosen sequence.
    We need to find which sequence yields the maximum total across all buyers.
    """
    initial_secrets = [int(line) for line in Input(data_file).as_lines()]
    sequence_totals = defaultdict(int)

    for secret in initial_secrets:
        prices, changes = generate_price_sequence(secret, ITERATIONS)
        buyer_sequences = find_first_occurrence_prices(prices, changes)

        for sequence, price in buyer_sequences.items():
            sequence_totals[sequence] += price

    return max(sequence_totals.values())


if __name__ == "__main__":
    run(
        sum_final_secrets,
        [
            TestCase("./data/22_example_01", 37327623),
            TestCase("./data/22_puzzle_input", 17262627539),
        ],
    )

    run(
        maximize_banana_profit,
        [
            TestCase("./data/22_example_02", 23),
            TestCase("./data/22_puzzle_input", 1986),
        ],
    )
