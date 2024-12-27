from collections import defaultdict
from aoc import read_data, run


def parse(file):
    numbers = read_data(11, file).split()
    return [int(n) for n in numbers]


def count_stones_after_blinks_optimized(initial_stones, blinks):
    """
    Simulates the evolution of stones using a dictionary to track counts of unique stones.

    :param initial_stones: List[int] - The initial arrangement of stones.
    :param blinks: int - The number of blinks to simulate.
    :return: int - The total number of stones after the simulation.
    """
    # Initialize the dictionary with counts of initial stones
    stone_counts = defaultdict(int)
    for stone in initial_stones:
        stone_counts[stone] += 1

    for _ in range(blinks):
        next_stone_counts = defaultdict(int)

        for stone, count in stone_counts.items():
            if stone == 0:
                # Rule 1: Replace 0 with 1
                next_stone_counts[1] += count
            elif len(str(stone)) % 2 == 0:
                # Rule 2: Split the stone into two halves
                str_stone = str(stone)
                mid = len(str_stone) // 2
                left = int(str_stone[:mid])
                right = int(str_stone[mid:])
                next_stone_counts[left] += count
                next_stone_counts[right] += count
            else:
                # Rule 3: Multiply the stone by 2024
                next_stone_counts[stone * 2024] += count

        stone_counts = next_stone_counts

    # Return the total number of stones
    return sum(stone_counts.values())


def answer(args):
    file, blinks = args
    stones = parse(file)
    return count_stones_after_blinks_optimized(stones, blinks)


# =============================================================================
if __name__ == "__main__":
    run(
        answer,
        [
            (("example1", 1), 7),
            (("example2", 6), 22),
            (("example2", 25), 55312),
            (("puzzle_input", 25), 222461),
            (("puzzle_input", 75), 264350935776416),
        ],
    )
