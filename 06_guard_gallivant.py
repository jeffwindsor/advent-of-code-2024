from aoc import read_data_as_lines, run, TestCase, TURN_CLOCKWISE, UP, coord_add


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
                guard_coordinate = (row, col)
            elif char == OBSTRUCTION_CHAR:
                obstruction_coordinates.add((row, col))

    return guard_coordinate, obstruction_coordinates, (row, col)


def is_out_of_bounds(limits, coord):
    return coord[0] < 0 or coord[0] > limits[0] or coord[1] < 0 or coord[1] > limits[1]


def find_path_unique_coords(direction, coord, obstructions, limits):
    unique_coords = set()
    while not is_out_of_bounds(limits, coord):
        next_coord = coord_add(coord, direction)
        if next_coord in obstructions:
            # Obstructed must turn
            direction = TURN_CLOCKWISE[direction]
        else:
            # Unobstructed must advance
            unique_coords.add(coord)
            coord = next_coord
    return unique_coords


def part1(file):
    unique_path_coords = find_path_unique_coords(UP, *parse(file))
    return len(unique_path_coords)


def find_possible_loop_in_path(direction, coord, obstructions, limits):
    visited_vectors = set()
    while not is_out_of_bounds(limits, coord):
        vector = (coord, direction)
        # check it we have been here before
        # print("Current: ", vector, vector in visited_vectors)
        if vector in visited_vectors:
            # this is a loop
            return True

        visited_vectors.add(vector)
        next_coord = coord_add(coord, direction)
        if next_coord in obstructions:
            # print("Turn Vec: ", visited_vectors)
            # Obstructed must turn
            direction = TURN_CLOCKWISE[direction]
        else:
            # Unobstructed must advance
            coord = next_coord

    # no loops found
    return False


def part2(file):
    guard_start_coord, obstructions, limits = parse(file)
    # test added obstructions one by one, using path coords to lower test set
    results = []
    unique_path_coords = find_path_unique_coords(
        UP, guard_start_coord, obstructions, limits
    )
    for obstruction in unique_path_coords:
        test_obstructions = obstructions.copy()
        test_obstructions.add(obstruction)
        results.append(
            find_possible_loop_in_path(UP, guard_start_coord, test_obstructions, limits)
        )

    return sum(results)


if __name__ == "__main__":
    run(part1, [
        TestCase("06_example", 41),
        TestCase("06_puzzle_input", 5095),
    ])
    run(part2, [
        TestCase("06_example", 6),
        TestCase("06_puzzle_input", 1933),
    ])
