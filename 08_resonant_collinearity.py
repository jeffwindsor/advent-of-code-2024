from itertools import combinations
from aoc import Input, run, TestCase, Coord, filter_coords_in_bounds


def parse(data_file):
    grid = Input(data_file).as_grid()
    return grid.max_bounds, grid.group_by_value(exclude=".")


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
        TestCase("data/08_example", 14),
        TestCase("data/08_puzzle_input", 426),
    ])
    run(part2, [
        TestCase("data/08_example", 34),
        TestCase("data/08_puzzle_input", 1359),
    ])
