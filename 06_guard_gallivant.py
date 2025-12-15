from aoc import Input, run, TestCase, Coord
from multiprocessing import Pool, cpu_count


def parse(data_file):
    GUARD_CHAR = "^"
    OBSTRUCTION_CHAR = "#"
    # read file contents
    lines = Input(data_file).as_lines()

    # Initialize variables
    guard_coordinate = None
    obstruction_coordinates = set()

    # Process each line
    for row, line in enumerate(lines):
        # Strip removes newlines and trailing spaces
        for col, char in enumerate(line.strip()):
            if char == GUARD_CHAR:
                guard_coordinate = Coord.from_rc(row, col)
            elif char == OBSTRUCTION_CHAR:
                obstruction_coordinates.add(Coord.from_rc(row, col))

    return guard_coordinate, obstruction_coordinates, Coord.from_rc(row, col)


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


def build_jump_table(obstructions, limits):
    """
    Precompute where guard ends up when moving in each direction until hitting obstacle.

    Returns dict: {(coord, direction): coord_before_obstacle}
    This eliminates cell-by-cell stepping during simulation.
    """
    jump_table = {}

    # For each position in the grid
    for row in range(limits.row + 1):
        for col in range(limits.col + 1):
            coord = Coord.from_rc(row, col)

            # For each cardinal direction
            for direction in Coord.DIRECTIONS_CARDINAL:
                # Walk in this direction until hitting obstacle or boundary
                current = coord
                while True:
                    next_coord = current + direction

                    # Stop if out of bounds or hit obstacle
                    if not next_coord.in_bounds(limits) or next_coord in obstructions:
                        break

                    current = next_coord

                # Store the last valid position before obstacle/boundary
                jump_table[(coord, direction)] = current

    return jump_table


def test_obstruction_worker(args):
    obstruction, guard_start_coord, obstructions, limits, jump_table = args
    return find_possible_loop_with_jumping(
        Coord.UP, guard_start_coord, obstructions, limits, jump_table, obstruction
    )


def part1(file):
    unique_path_coords = find_path_unique_coords(Coord.UP, *parse(file))
    return len(unique_path_coords)


def find_possible_loop_with_jumping(
    direction, coord, obstructions, limits, jump_table, extra_obstruction=None
):
    visited_turns = set()
    max_turns = (limits.row + 1) * (limits.col + 1) * 4
    turn_count = 0

    while coord.in_bounds(limits):
        # Jump to position just before next obstacle
        jumped_coord = jump_table.get((coord, direction), coord)

        # Check if extra obstruction blocks this jump
        if extra_obstruction is not None:
            # Walk from current to jumped position, checking for extra obstruction
            check_coord = coord
            while check_coord != jumped_coord:
                next_check = check_coord + direction
                if next_check == extra_obstruction:
                    # Extra obstruction blocks, stop here
                    jumped_coord = check_coord
                    break
                check_coord = next_check

        coord = jumped_coord

        # Check what's ahead
        next_coord = coord + direction
        is_obstructed = next_coord in obstructions or next_coord == extra_obstruction

        if is_obstructed:
            # Hit obstacle - check for loop at this turning point
            turn_state = (coord, direction)
            if turn_state in visited_turns:
                return True  # Loop detected

            visited_turns.add(turn_state)
            direction = Coord.TURN_CLOCKWISE[direction]
            turn_count += 1

            # Safety: too many turns means no loop
            if turn_count >= max_turns:
                return False
        elif not next_coord.in_bounds(limits):
            # Would exit bounds - no loop
            return False

    return False


def part2(file):
    guard_start_coord, obstructions, limits = parse(file)

    # Precompute jump table once (one-time cost)
    jump_table = build_jump_table(obstructions, limits)

    # Get candidate positions from original path
    unique_path_coords = find_path_unique_coords(
        Coord.UP, guard_start_coord, obstructions, limits
    )

    # Prepare arguments for parallel processing
    # Convert to list for multiprocessing
    obstruction_list = list(unique_path_coords)
    args_list = [
        (obstruction, guard_start_coord, obstructions, limits, jump_table)
        for obstruction in obstruction_list
    ]

    # Use all available CPU cores to test obstructions in parallel
    with Pool(cpu_count()) as pool:
        results = pool.map(test_obstruction_worker, args_list)

    # Count True results (loops found)
    return sum(results)


if __name__ == "__main__":
    run(
        part1,
        [
            TestCase("./data/06_example", 41),
            TestCase("./data/06_puzzle_input", 5095),
        ],
    )
    run(
        part2,
        [
            TestCase("./data/06_example", 6),
            TestCase("./data/06_puzzle_input", 1933),
        ],
    )
