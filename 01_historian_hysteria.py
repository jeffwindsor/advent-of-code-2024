from aoc import read_data_as_columns, run, TestCase
from collections import Counter


def part1(file):
    xs, ys = read_data_as_columns(file, separator="   ")
    return sum(abs(x - y) for x, y in zip(sorted(xs), sorted(ys)))


def part2(file):
    xs, ys = read_data_as_columns(file, separator="   ")
    frequencies = Counter(ys)
    return sum(x * frequencies[x] for x in xs)


if __name__ == "__main__":
    run(part1, [
        TestCase("01_example", 11),
        TestCase("01_puzzle_input", 2066446),
    ])
    run(part2, [
        TestCase("01_example", 31),
        TestCase("01_puzzle_input", 24931009),
    ])
