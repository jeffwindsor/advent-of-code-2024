from itertools import combinations
from utils.files import read_data_as_lines
from utils.runners import run
from utils.matrix_2d import higher_bounds
from utils.matrix_2d.coordinates import filter_within_bounds, is_within_bounds, add, sub
from utils.parsers.matrix_2D import parse_into_char_coords


def parse(file):
    lines = read_data_as_lines(8, file)
    return higher_bounds(lines), parse_into_char_coords(lines, ".")


def extend_in_direction(coord, diff, combine_func, matrix_size):
    valid_coordinates = []
    while is_within_bounds(coord, matrix_size):
        valid_coordinates.append(coord)
        coord = combine_func(coord, diff)
    return valid_coordinates


def extended_pair(a, b, matrix_size):
    diff = sub(a, b)
    potential_coords = [add(a, diff), sub(b, diff)]
    return filter_within_bounds(potential_coords, matrix_size)


def extended_line(a, b, matrix_size):
    diff = sub(a, b)
    return extend_in_direction(a, diff, add, matrix_size) + extend_in_direction(
        b, diff, sub, matrix_size
    )


def calculate_antinode_positions(extend_func, size, points_by_char):
    antinode_positions = set()
    for _, coords in points_by_char.items():
        for a, b in combinations(coords, 2):
            antinode_positions.update(extend_func(a, b, size))

    return len(antinode_positions)


def part1(file):
    return calculate_antinode_positions(extended_pair, *parse(file))


def part2(file):
    return calculate_antinode_positions(extended_line, *parse(file))


if __name__ == "__main__":
    run(part1, [("example", 14), ("puzzle_input", 426)])
    run(part2, [("example", 34), ("puzzle_input", 1359)])
