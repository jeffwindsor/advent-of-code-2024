from parser import parse
from itertools import pairwise

def diff(pair):
    return pair[0] - pair[1]

def is_safe(report):
    diffs = list(map(diff, pairwise(report)))
    all_positive = all(diff > 0 for diff in diffs)
    all_negative = all(diff < 0 for diff in diffs)
    all_within_bounds = all(abs(diff) > 0 and abs(diff) < 4 for diff in diffs)
    return all_within_bounds and (all_positive or all_negative)

def is_safe_dampered(report):
    if is_safe(report):
        return True
    damped_reports = [report[:i] + report[i+1:] for i in range(len(report))]
    results = map(is_safe, damped_reports)
    return any(results)


def part1(file):
    return sum(map(is_safe, parse(file)))

def part2(file):
    return sum(map(is_safe_dampered, parse(file)))

if __name__ == "__main__":
    print(f"part 1 example should be 2: {part1('example')}")
    print(f"part 1: {part1('puzzle_input')}")
    print(f"part 2 example should be 4: {part2('example')}")
    print(f"part 2: {part2('puzzle_input')}")
