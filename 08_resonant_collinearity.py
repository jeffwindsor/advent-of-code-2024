from itertools import combinations
from aoc import (
    read_data_as_lines,
    run,
    coord_add,
    coord_sub,
    coord_is_within_bounds_inclusive,
    matrix_higher_bounds,
    filter_within_bounds,
)

# from utils.matrix_2d import higher_bounds
# from utils.matrix_2d.coordinates import (
#     filter_within_bounds,
#     is_within_bounds_inclusive,
#     add,
#     sub,
# )


def parse_into_char_coords(lines, empty_char):
    result = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line.strip()):
            if char == empty_char:
                continue
            if char not in result:
                result[char] = []
            result[char].append((row, col))
    return result


def parse(file):
    lines = read_data_as_lines(8, file)
    return matrix_higher_bounds(lines), parse_into_char_coords(lines, ".")


def extend_in_direction(coord, diff, combine_func, bounds):
    valid_coordinates = []
    while coord_is_within_bounds_inclusive(coord, bounds):
        valid_coordinates.append(coord)
        coord = combine_func(coord, diff)
    return valid_coordinates


def extended_pair(a, b, bounds):
    diff = coord_sub(a, b)
    potential_coords = [coord_add(a, diff), coord_sub(b, diff)]
    return filter_within_bounds(potential_coords, bounds)


def extended_line(a, b, bounds):
    diff = coord_sub(a, b)
    return extend_in_direction(a, diff, coord_add, bounds) + extend_in_direction(
        b, diff, coord_sub, bounds
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
