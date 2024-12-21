import utils.files as F
import utils.runners as R
from itertools import pairwise

DAY = 2


def parse(filepath):
    lines = F.read_data_as_lines(DAY, filepath)
    return F.split_and_map(int, " ", lines)


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
    R.run(part1, [("example", 2), ("puzzle_input", 306)])
    R.run(part2, [("example", 4), ("puzzle_input", 366)])
