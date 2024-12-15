from parser import parse
from itertools import combinations


def is_within_bounds(limits, coord):
    """Check if a coordinate is within the grid limits."""
    return 0 <= coord[0] <= limits[0] and 0 <= coord[1] <= limits[1]


def get_in_bounds_coords(limits, coords):
    """Filter coordinates to include only those within bounds."""
    return [c for c in coords if is_within_bounds(limits, c)]


def calculate_antinode_positions(limits, frequency_coords, add_func):
    """Calculate unique antinode positions based on a specific adding strategy."""
    antinode_positions = set()

    for _, coords in frequency_coords.items():
        for (x1, y1), (x2, y2) in combinations(coords, 2):
            dx, dy = x1 - x2, y1 - y2
            antinode_positions.update(add_func(limits, dx, dy, (x1, y1), (x2, y2)))

    return len(antinode_positions)


def part1_add(limits, dx, dy, coord1, coord2):
    """Add antinodes for part 1 logic."""
    x1, y1 = coord1
    x2, y2 = coord2
    potential_coords = [
        (x2 - dx, y2 - dy),
        (x1 + dx, y1 + dy),
    ]
    return get_in_bounds_coords(limits, potential_coords)


def part2_add(limits, dx, dy, coord1, coord2):
    """Add antinodes for part 2 logic (extend until bounds)."""
    x1, y1 = coord1
    x2, y2 = coord2

    coords = []
    # Extend in one direction
    while is_within_bounds(limits, (x2, y2)):
        coords.append((x2, y2))
        x2 -= dx
        y2 -= dy

    # Extend in the other direction
    while is_within_bounds(limits, (x1, y1)):
        coords.append((x1, y1))
        x1 += dx
        y1 += dy

    return coords


def part1(file):
    """Solve part 1 of the problem."""
    limits, frequency_coords = parse(file)
    return calculate_antinode_positions(limits, frequency_coords, part1_add)


def part2(file):
    """Solve part 2 of the problem."""
    limits, frequency_coords = parse(file)
    return calculate_antinode_positions(limits, frequency_coords, part2_add)


if __name__ == "__main__":
    print(f"Part 1 (Example, Expected: 14): {part1('example')}")
    print(f"Part 1 (Puzzle Input, Expected: 426): {part1('puzzle_input')}")
    print(f"Part 2 (Example, Expected: 34): {part2('example')}")
    print(f"Part 2 (Puzzle Input, Expected: 1359): {part2('puzzle_input')}")
