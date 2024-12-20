import utils.runners as R
import utils.files as F
from collections import Counter

DAY = 1


def parse_data(file):
    lines = F.read_data_as_lines(DAY, file)
    numbers_by_line = F.split_and_map(int, "   ", lines)
    # put first numbers in a list, and second number of line in a list
    return list(zip(*numbers_by_line))


def calculate_total_distance(file):
    xs, ys = parse_data(file)
    return sum(abs(x - y) for x, y in zip(sorted(xs), sorted(ys)))


def calculate_weighted_sum(file):
    xs, ys = parse_data(file)
    frequencies = Counter(ys)
    return sum(x * frequencies[x] for x in xs)


if __name__ == "__main__":
    R.run(
        [
            ("p1.e ", calculate_total_distance, "example", 11),
            ("p1.pi", calculate_total_distance, "puzzle_input", 2066446),
            ("p2.e ", calculate_weighted_sum, "example", 31),
            ("p2.pi", calculate_weighted_sum, "puzzle_input", 24931009),
        ]
    )
