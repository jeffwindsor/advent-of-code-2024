from utils.files import read_data_as_lines
from utils.matrix_2d import find_first
from utils.runners import run
from collections import deque

START = "S"
END = "E"


def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # BFS queue: (position, steps)
    queue = deque([(start, 0)])
    visited = set()

    while queue:
        (x, y), steps = queue.popleft()

        # If reached the end, return the steps
        if (x, y) == end:
            return steps

        # Mark as visited
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < rows
                and 0 <= ny < cols
                and (grid[nx][ny] == "." or grid[nx][ny] == END)
            ):
                queue.append(((nx, ny), steps + 1))

    return float("inf")  # Return infinity if no path is found


def solve_race_condition(grid):
    start, end = find_first(grid, START), find_first(grid, END)
    shortest_time = bfs(grid, start, end)
    return shortest_time


def part1(filename):
    grid = read_data_as_lines(20, filename)
    shortest_time = solve_race_condition(grid)
    return shortest_time


if __name__ == "__main__":
    run(part1, [("example", 84)])
