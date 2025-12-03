from aoc import (
    read_data_as_coord_pairs,
    run,
    TestCase,
    Coord,
    create_grid,
    grid_set,
    grid_get,
    grid_max_bounds,
    bfs,
)


def parse_input(data_file):
    return read_data_as_coord_pairs(data_file)


def simulate_memory_space(grid_size, byte_positions, total_bytes):
    # Initialize the grid using aoc utility
    grid = create_grid(grid_size, ".")

    # Corrupt the grid based on the incoming bytes
    for i in range(min(total_bytes, len(byte_positions))):
        x, y = byte_positions[i]
        coord = Coord(y, x)  # Convert (x,y) to (row, col)
        if coord.in_bounds(grid_max_bounds(grid)):
            grid_set(grid, coord, "#")

    return grid


def find_shortest_path(grid):
    grid_size = len(grid)
    start = Coord(0, 0)
    end = Coord(grid_size - 1, grid_size - 1)
    max_bounds = grid_max_bounds(grid)

    # Define neighbors function for BFS
    def neighbors_func(coord):
        return [
            neighbor
            for direction in Coord.DIRECTIONS_CARDINAL
            if (neighbor := coord + direction).in_bounds(max_bounds)
            and grid_get(grid, neighbor) == "."
        ]

    # Use aoc.bfs() to find distances
    distances = bfs(start, neighbors_func)

    # Return distance to end, or -1 if not found
    return distances.get(end, -1)


def find_blocking_byte(grid_size, byte_positions):
    """
    Find the first byte that blocks the path using binary search.

    We know that:
    - With 0 bytes, there's a path
    - With all bytes, there might not be a path
    - We want the first byte that blocks the path

    Returns the coordinates as a string "x,y"
    """
    left = 0
    right = len(byte_positions) - 1
    result = None

    while left <= right:
        mid = (left + right) // 2

        # Test with mid bytes
        grid = simulate_memory_space(grid_size, byte_positions, mid + 1)
        path_exists = find_shortest_path(grid) != -1

        if path_exists:
            # Path still exists, try more bytes
            left = mid + 1
        else:
            # Path is blocked, this could be our answer
            # But check if there's an earlier blocking byte
            result = mid
            right = mid - 1

    if result is not None:
        x, y = byte_positions[result]
        return f"{x},{y}"

    return None


def part1(args):
    file_path, grid_size, sim_bytes = args
    grid = simulate_memory_space(grid_size, parse_input(file_path), sim_bytes)
    return find_shortest_path(grid)


def part2(args):
    file_path, grid_size = args
    byte_positions = parse_input(file_path)
    return find_blocking_byte(grid_size, byte_positions)


if __name__ == "__main__":
    run(part1, [
        TestCase(("18_example", 7, 12), 22),
        TestCase(("18_puzzle_input", 71, 1024), 226),
    ])

    run(part2, [
        TestCase(("18_example", 7), "6,1"),
        TestCase(("18_puzzle_input", 71), "60,46"),
    ])
