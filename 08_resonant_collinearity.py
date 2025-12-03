from itertools import combinations
from aoc import (
    read_data_as_lines,
    run,
    TestCase,
    Coord,
    grid_max_bounds,
    filter_coords_in_bounds,
    group_by_value,
)


def parse(data_file):
    lines = read_data_as_lines(data_file)
    return grid_max_bounds(lines), group_by_value(lines, exclude=".")


def extend_in_direction(coord, diff, forward, bounds):
    """Extend coordinates in a direction. forward=True adds diff, False subtracts."""
    valid_coordinates = []
    while coord.in_bounds(bounds):
        valid_coordinates.append(coord)
        coord = coord + diff if forward else coord - diff
    return valid_coordinates


def extended_pair(a, b, bounds):
    diff = a - b
    potential_coords = [a + diff, b - diff]
    return filter_coords_in_bounds(potential_coords, bounds)


def extended_line(a, b, bounds):
    diff = a - b
    return extend_in_direction(a, diff, True, bounds) + extend_in_direction(
        b, diff, False, bounds
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
    run(part1, [
        TestCase("08_example", 14),
        TestCase("08_puzzle_input", 426),
    ])
    run(part2, [
        TestCase("08_example", 34),
        TestCase("08_puzzle_input", 1359),
    ])
