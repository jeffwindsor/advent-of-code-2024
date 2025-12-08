from aoc import Input, extract_ints, run, TestCase
from itertools import pairwise


def parse(data_file):
    return [extract_ints(line) for line in Input(data_file).as_lines()]


def is_safe(report):
    diffs = list(map(lambda xs: xs[0] - xs[1], pairwise(report)))
    all_positive = all(diff > 0 for diff in diffs)
    all_negative = all(diff < 0 for diff in diffs)
    all_within_bounds = all(abs(diff) > 0 and abs(diff) < 4 for diff in diffs)
    return all_within_bounds and (all_positive or all_negative)


def is_safe_dampered(report):
    if is_safe(report):
        return True
    damped_reports = [report[:i] + report[i + 1 :] for i in range(len(report))]
    results = map(is_safe, damped_reports)
    return any(results)


def part1(file):
    return sum(map(is_safe, parse(file)))


def part2(file):
    return sum(map(is_safe_dampered, parse(file)))


if __name__ == "__main__":
    run(
        part1,
        [
            TestCase("./data/02_example", 2),
            TestCase("./data/02_puzzle_input", 306),
        ],
    )
    run(
        part2,
        [
            TestCase("./data/02_example", 4),
            TestCase("./data/02_puzzle_input", 366),
        ],
    )
