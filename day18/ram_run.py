from collections import deque


def parse_input(file_path: str) -> list[tuple[int, int]]:
    with open(file_path, "r") as file:
        # Read the file content and split it into lines
        content = file.read()
        # Split the content by newlines, then split by commas and convert to tuples
        coordinates = [
            tuple(map(int, line.split(","))) for line in content.strip().split("\n")
        ]
    return coordinates


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

    # Directions for movement: right, left, down, up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

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
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

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


def part1(file_path, grid_size, sim_bytes):
    # Simulate the grid
    grid = simulate_memory_space(grid_size, parse_input(file_path), sim_bytes)

    # Find the shortest path
    return find_shortest_path(grid)


if __name__ == "__main__":
    print(f"p1.e1 (22): {part1('example',7,12)}")
    print(f"p1.pi (): {part1('puzzle_input',71,1024)}")
