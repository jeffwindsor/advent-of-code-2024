from aoc import read_data_as_lines, run
from collections import Counter


def parse_data(file):
    lines = read_data_as_lines(1, file)
    numbers_by_line = [list(map(int, line.split("   "))) for line in lines]
    # put first numbers in a list, and second number of line in a list
    return list(zip(*numbers_by_line))


def part1(file):
    xs, ys = parse_data(file)
    return sum(abs(x - y) for x, y in zip(sorted(xs), sorted(ys)))


def part2(file):
    xs, ys = parse_data(file)
    frequencies = Counter(ys)
    return sum(x * frequencies[x] for x in xs)


if __name__ == "__main__":
    run(part1, [("example", 11), ("puzzle_input", 2066446)])
    run(part2, [("example", 31), ("puzzle_input", 24931009)])
