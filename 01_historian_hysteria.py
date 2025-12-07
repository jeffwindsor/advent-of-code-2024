from aoc import Input, run, TestCase
from collections import Counter


def parse(file):
    return Input(file).as_columns(separator="   ", converter=int)


def part1(file):
    xs, ys = parse(file)
    return sum(abs(x - y) for x, y in zip(sorted(xs), sorted(ys)))


def part2(file):
    xs, ys = parse(file)
    frequencies = Counter(ys)
    return sum(x * frequencies[x] for x in xs)


if __name__ == "__main__":
    run(
        part1,
        [
            TestCase("./data/01_example", 11),
            TestCase("./data/01_puzzle_input", 2066446),
        ],
    )
    run(
        part2,
        [
            TestCase("./data/01_example", 31),
            TestCase("./data/01_puzzle_input", 24931009),
        ],
    )
