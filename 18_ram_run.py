from aoc import parse_coord_pairs, run, TestCase, Coord
from collections import deque


def parse_input(data_file):
    return parse_coord_pairs(data_file)


def simulate_memory_space(grid_size, byte_positions, total_bytes):
    # Initialize the grid
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

    # Corrupt the grid based on the incoming bytes
    for i in range(min(total_bytes, len(byte_positions))):
        x, y = byte_positions[i]
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y][x] = "#"

    return grid


def find_shortest_path(grid):
    grid_size = len(grid)
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

    # BFS setup
    queue = deque([(start, 0)])  # (current_position, steps)
    visited = set()
    visited.add(start)

    while queue:
        (x, y), steps = queue.popleft()

        # Check if we've reached the end
        if (x, y) == end:
            return steps

        # Explore neighbors
        for direction in Coord.DIRECTIONS_CARDINAL:
            nx, ny = x + direction.col, y + direction.row

            # Check bounds and valid movement
            if (
                0 <= nx < grid_size
                and 0 <= ny < grid_size
                and grid[ny][nx] == "."
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))

    # If no path is found
    return -1


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
