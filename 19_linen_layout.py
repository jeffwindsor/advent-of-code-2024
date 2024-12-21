# from collections import defaultdict


def parse_input(file_path: str):
    with open(file_path, "r") as file:
        input = file.read()

    ps, ds = input.strip().split("\n\n")
    patterns = [p.strip() for p in ps.split(",")]
    designs = [d.strip() for d in ds.splitlines()]
    return patterns, designs


def count_possible_arrangements(pattern, available_patterns, memo=None, start=0):
    if memo is None:
        memo = {}

    if start == len(pattern):
        return 1

    if start in memo:
        return memo[start]

    count = 0
    for towel in available_patterns:
        if (
            start + len(towel) <= len(pattern)
            and pattern[start : start + len(towel)] == towel
        ):
            count += count_possible_arrangements(
                pattern, available_patterns, memo, start + len(towel)
            )

    memo[start] = count
    return count


def solve_both_parts(patterns, designs):

    # Part 1: Count possible designs
    possible_count = 0
    # Part 2: Sum of all possible arrangements
    total_arrangements = 0

    for design in designs:
        arrangements = count_possible_arrangements(design, patterns)
        if arrangements > 0:
            possible_count += 1
        total_arrangements += arrangements

    return possible_count, total_arrangements


if __name__ == "__main__":
    print(f"parse e: {parse_input('example')}")
    print(f"example: {solve_both_parts(*parse_input('example'))}")
    print(f"puzzle input: {solve_both_parts(*parse_input('puzzle_input'))}")
