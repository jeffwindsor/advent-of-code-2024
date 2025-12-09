from aoc import Input, run, TestCase


def parse_input(data_file):
    section1, section2 = Input(data_file).as_sections()
    patterns = [p.strip() for p in section1.content.split(",")]
    designs = section2.as_lines()
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


def parts(file):
    return solve_both_parts(*parse_input(file))


if __name__ == "__main__":
    run(parts, [
        TestCase("./data/19_example", (6, 16)),
        TestCase("./data/19_puzzle_input", (304, 705756472327497)),
    ])
