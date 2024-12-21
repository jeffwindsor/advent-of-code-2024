from parser import parse

from collections import defaultdict


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


def answer(file, blinks):
    stones = parse(file)
    return count_stones_after_blinks_optimized(stones, blinks)


# =============================================================================
if __name__ == "__main__":
    print(f"1:example1 (Expected 7 : Accepted {answer('example1',1)})")
    print(f"1:example2 (Expected 22 : Accepted {answer('example2',6)})")
    print(f"1:example2 (Expected 55312 : Accepted {answer('example2', 25)})")
    print(f"1: (Expected 222461: Accepted {answer('puzzle_input', 25)})")
    print(f"2: (Expected 264350935776416 : Accepted {answer('puzzle_input', 75)})")
