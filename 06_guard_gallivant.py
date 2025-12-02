from aoc import read_data_as_lines, run, TestCase, Coord


def parse(data_file):
    GUARD_CHAR = "^"
    OBSTRUCTION_CHAR = "#"
    # read file contents
    lines = read_data_as_lines(data_file)

    # Initialize variables
    guard_coordinate = None
    obstruction_coordinates = set()

    # Process each line
    for row, line in enumerate(lines):
        # Strip removes newlines and trailing spaces
        for col, char in enumerate(line.strip()):
            if char == GUARD_CHAR:
                guard_coordinate = Coord(row, col)
            elif char == OBSTRUCTION_CHAR:
                obstruction_coordinates.add(Coord(row, col))

    return guard_coordinate, obstruction_coordinates, Coord(row, col)


def find_path_unique_coords(direction, coord, obstructions, limits):
    unique_coords = set()
    while coord.in_bounds(limits):
        next_coord = coord + direction
        if next_coord in obstructions:
            # Obstructed must turn
            direction = Coord.TURN_CLOCKWISE[direction]
        else:
            # Unobstructed must advance
            unique_coords.add(coord)
            coord = next_coord
    return unique_coords


def part1(file):
    unique_path_coords = find_path_unique_coords(Coord.UP, *parse(file))
    return len(unique_path_coords)


def find_possible_loop_in_path(direction, coord, obstructions, limits, extra_obstruction=None):
    """
    Check if the guard's path forms a loop.
    Optimized to avoid copying the obstructions set by accepting an optional extra obstruction.

    Args:
        direction: Current direction of movement
        coord: Starting coordinate
        obstructions: Set of obstruction coordinates
        limits: Boundary limits
        extra_obstruction: Optional single additional obstruction coordinate

    Returns:
        True if a loop is detected, False otherwise
    """
    visited_vectors = set()
    while coord.in_bounds(limits):
        vector = (coord, direction)
        # check if we have been here before
        if vector in visited_vectors:
            # this is a loop
            return True

        visited_vectors.add(vector)
        next_coord = coord + direction

        # Check both original obstructions and optional extra one
        is_obstructed = next_coord in obstructions or next_coord == extra_obstruction

        if is_obstructed:
            # Obstructed must turn
            direction = Coord.TURN_CLOCKWISE[direction]
        else:
            # Unobstructed must advance
            coord = next_coord

    # no loops found
    return False


def part2(file):
    """
    Test loop detection by adding one obstruction at a time from the guard's path.
    Optimized to avoid copying the obstructions set for each test.
    """
    guard_start_coord, obstructions, limits = parse(file)
    # test added obstructions one by one, using path coords to lower test set
    unique_path_coords = find_path_unique_coords(
        Coord.UP, guard_start_coord, obstructions, limits
    )

    # Count loops by testing each path coordinate as an additional obstruction
    return sum(
        1 for obstruction in unique_path_coords
        if find_possible_loop_in_path(
            Coord.UP, guard_start_coord, obstructions, limits, obstruction
        )
    )


if __name__ == "__main__":
    run(part1, [
        TestCase("06_example", 41),
        TestCase("06_puzzle_input", 5095),
    ])
    run(part2, [
        TestCase("06_example", 6),
        TestCase("06_puzzle_input", 1933),
    ])
