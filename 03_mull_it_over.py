from aoc import read_data, run, TestCase
from re import findall


def mul(match):
    return int(match[0]) * int(match[1])


def score(multiplies):
    return sum(map(mul, multiplies))


def apply_do_and_dont(matches):
    include = True
    for match in matches:
        if match == "don't()":
            include = False
        elif match == "do()":
            include = True
        elif include:
            yield tuple(findall(r"\d+", match))


def part1(data_file):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    # find all returns tuple of (x,y)
    multiplies = findall(pattern, read_data(data_file))
    return score(multiplies)


def part2(data_file):
    pattern = r"(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don't\(\))"
    # flatten since findall returns a tuple per match ('mul(x,y)','do()', "don't()")
    instructions = [
        m[0] or m[1] or m[2] for m in findall(pattern, read_data(data_file))
    ]
    multiplies = apply_do_and_dont(instructions)
    return score(multiplies)


if __name__ == "__main__":
    run(part1, [
        TestCase("03_example", 161),
        TestCase("03_puzzle_input", 170807108),
    ])
    run(part2, [
        TestCase("03_example2", 48),
        TestCase("03_puzzle_input", 74838033),
    ])
