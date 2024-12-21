from collections import deque
from utils.matrix_2d import DIRECTIONS_CARDINAL
from utils.files import read_data_as_lines
from utils.runners import run


def parse(file):
    EMPTY = -1
    return [
        list(map(lambda x: int(x) if x.isdigit() else EMPTY, line.strip()))
        for line in read_data_as_lines(10, file)
    ]


# =============================================================================
def find_reachable_nines(matrix, starts):
    """BFS all reachable trailends shown as a nine"""
    rows, cols = len(matrix), len(matrix[0])
    queue = deque([starts])
    visited = set([starts])
    leaves = set()

    while queue:
        (x, y) = queue.popleft()
        v = matrix[x][y]

        if v == 9:
            leaves.add((x, y))

        for dx, dy in DIRECTIONS_CARDINAL:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                next = (nx, ny)
                if next not in visited and v + 1 == matrix[nx][ny]:
                    queue.append(next)
                    visited.add(next)
    return leaves


def find_trailheads(topographic_map):
    """Identify all positions with height 0 as trailheads."""
    trailheads = []
    for r, row in enumerate(topographic_map):
        for c, height in enumerate(row):
            if height == 0:
                trailheads.append((r, c))
    return trailheads


def dfs(map, row, col, current_path, memo):
    """Recursive DFS to explore all distinct hiking trails."""
    key = (row, col, tuple(current_path))
    if key in memo:
        return memo[key]

    height = map[row][col]
    if height == 9:
        # Reached the end of a trail
        return {tuple(current_path)}

    trails = set()
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(map) and 0 <= nc < len(map[0]) and map[nr][nc] == height + 1:
            trails |= dfs(map, nr, nc, current_path + [(nr, nc)], memo)

    memo[key] = trails
    return trails


def calculate_ratings(map, trailheads):
    """Calculate the rating for each trailhead."""
    total_rating = 0
    memo = {}

    for r, c in trailheads:
        trails = dfs(map, r, c, [(r, c)], memo)
        total_rating += len(trails)

    return total_rating


def part1(file):
    topo_map = parse(file)
    trailheads = find_trailheads(topo_map)
    return sum([len(find_reachable_nines(topo_map, z)) for z in trailheads])


def part2(file):
    topo = parse(file)
    trailheads = find_trailheads(topo)
    return calculate_ratings(topo, trailheads)


# =============================================================================
if __name__ == "__main__":
    run(
        part1,
        [
            ("example1", 1),
            ("example2", 2),
            ("example3", 4),
            ("example4", 3),
            ("example5", 36),
            ("puzzle_input", 674),
        ],
    )

    run(
        part2,
        [
            ("example_6", 3),
            ("example_7", 13),
            ("example_8", 227),
            ("example_9", 81),
            ("puzzle_input", 1372),
        ],
    )
