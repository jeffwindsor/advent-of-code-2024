from aoc import read_data_as_lines, run
from collections import deque


def parse(file):
    return [list(line) for line in read_data_as_lines(12, file)]


area = "a"
perimeter = "p"


def calculate_area_and_perimeter(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def analyze_grid_regions(r, c, char):
        stack, area, perimeter = [(r, c)], 0, 0
        visited[r][c] = True
        while stack:
            x, y = stack.pop()
            area += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if grid[nx][ny] == char and not visited[nx][ny]:
                        stack.append((nx, ny))
                        visited[nx][ny] = True
                    elif grid[nx][ny] != char:
                        perimeter += 1
                else:
                    perimeter += 1
        return area, perimeter

    results = []
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                char = grid[r][c]
                area, perimeter = analyze_grid_regions(r, c, char)
                results.append((char, area, perimeter))
    return results


def part1(file):
    grid = parse(file)
    shapes = calculate_area_and_perimeter(grid)
    # print(shapes)
    return sum([shape[1] * shape[2] for shape in shapes])


def calculate_area_and_sides(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def flood_fill(r, c, char):
        stack = [(r, c)]
        visited[r][c] = True
        area = 0
        boundaries = set()  # Store all boundary edges as unique segments

        while stack:
            x, y = stack.pop()
            area += 1
            # Check all 4 directions
            for dx, dy, direction in [
                (-1, 0, "U"),
                (1, 0, "D"),
                (0, -1, "L"),
                (0, 1, "R"),
            ]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if grid[nx][ny] == char and not visited[nx][ny]:
                        stack.append((nx, ny))
                        visited[nx][ny] = True
                    elif grid[nx][ny] != char:
                        # Add the boundary segment
                        boundaries.add(((x, y), direction))
                else:
                    # Out of bounds is also a boundary
                    boundaries.add(((x, y), direction))

        # Group boundaries into sides
        sides = set()
        for edge, direction in boundaries:
            sides.add((direction, edge))
        return area, len(sides)

    results = []
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                char = grid[r][c]
                area, sides = flood_fill(r, c, char)
                results.append((char, area, sides))
    return results


def calculate_total_price(grid):
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def bfs(x, y):
        # Perform BFS to find all cells in the same region
        queue = deque([(x, y)])
        region_cells = []
        visited[x][y] = True
        while queue:
            cx, cy = queue.popleft()
            region_cells.append((cx, cy))
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if (
                    is_valid(nx, ny)
                    and not visited[nx][ny]
                    and grid[nx][ny] == grid[cx][cy]
                ):
                    visited[nx][ny] = True
                    queue.append((nx, ny))
        return region_cells

    def count_sides(cells):
        sides = 0
        for x, y in cells:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not is_valid(nx, ny) or grid[nx][ny] != grid[x][y]:
                    sides += 1
        return sides

    # Initialize variables
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    total_price = 0

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                # Find a new region
                region_cells = bfs(i, j)
                area = len(region_cells)
                sides = count_sides(region_cells)
                total_price += area * sides

    return total_price


def part2(file):
    grid = parse(file)
    print(grid)
    return calculate_total_price(grid)


if __name__ == "__main__":
    run(
        part1,
        [
            ("example", 140),
            ("example_xo", 772),
            ("example_RIC", 1930),
            ("puzzle_input", 1488414),
        ],
    )
    # run(
    #     part2,
    #     [
    #         ("example", 80),
    #         ("example_xo", 436),
    #         ("example_EE", 236),
    #         ("example_AA", 386),
    #         ("puzzle_input", None),
    #     ],
    # )
