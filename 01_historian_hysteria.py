from collections import Counter
from utils import read_data_as_lines, run


def parse_data(file):
    lines = read_data_as_lines(1, file)
    number_pairs = [tuple(map(int, line.split("   "))) for line in lines]
    return tuple(zip(*number_pairs))


def calculate_total_distance(file):
    xs, ys = parse_data(file)
    return sum(abs(x - y) for x, y in zip(sorted(xs), sorted(ys)))


def calculate_weighted_sum(file):
    xs, ys = parse_data(file)
    frequencies = Counter(ys)
    return sum(x * frequencies[x] for x in xs)


if __name__ == "__main__":
    run(
        [
            ("p1.e ", calculate_total_distance, "example", 11),
            ("p1.pi", calculate_total_distance, "puzzle_input", 2066446),
            ("p2.e ", calculate_weighted_sum, "example", 31),
            ("p2.pi", calculate_weighted_sum, "puzzle_input", 24931009),
        ]
    )
