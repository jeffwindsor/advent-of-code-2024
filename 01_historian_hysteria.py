import utils.runners as R
import utils.files as F
from collections import Counter

DAY = 1


def parse_data(file):
    lines = F.read_data_as_lines(DAY, file)
    numbers_by_line = F.split_and_map(int, "   ", lines)
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
    R.run(part1, [("example", 11), ("puzzle_input", 2066446)])
    R.run(part2, [("example", 31), ("puzzle_input", 24931009)])
