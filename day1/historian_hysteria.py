from parser import parse
from collections import Counter


def distance(ps):
    return abs(ps[0] - ps[1])


def part1(file):
    first, second = parse(file)
    data = zip(sorted(first), sorted(second))
    return sum(map(distance, data))


def similarity_score(dy, number):
    return number * dy[number]


def part2(file):
    xs, ys = parse(file)
    dy = Counter(ys)
    scores = list(map(lambda n: similarity_score(dy, n), xs))
    return sum(scores)


if __name__ == "__main__":
    print(f"part 1 example (11): {part1('example')}")
    print(f"part 1 (2066446): {part1('puzzle_input')}")
    print(f"part 2 example (31): {part2('example')}")
    print(f"part 2 (24931009): {part2('puzzle_input')}")
