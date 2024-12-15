from parser import parse
from collections import deque


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right


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

        for dx, dy in directions:
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
    print(f"1:example1 [Expect 1 : Actual {part1('example1')}]")
    print(f"1:example2 [Expect 2 : Actual {part1('example2')}]")
    print(f"1:example3 [Expect 4 : Actual {part1('example3')}]")
    print(f"1:example4 [Expect 3 : Actual {part1('example4')}]")
    print(f"1:example5 [Expect 36 : Actual {part1('example5')}]")
    print(f"1:puzzle_input [Expect 674 : Actual {part1('puzzle_input')}]")

    print(f"2:example_6 [Expect 3 : Actual {part2('example_6')}]")
    print(f"2:example_7 [Expect 13 : Actual {part2('example_7')}]")
    print(f"2:example_8 [Expect 227 : Actual {part2('example_8')}]")
    print(f"2:example_9 [Expect 81 : Actual {part2('example_9')}]")
    print(f"2:puzzle_input [Expect 1372 : Actual {part2('puzzle_input')}]")
