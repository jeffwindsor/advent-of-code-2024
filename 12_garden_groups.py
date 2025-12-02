from aoc import read_data_as_lines, run
from collections import deque
from dataclasses import dataclass


# Constants
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


@dataclass
class Region:
    plant: str
    area: int
    perimeter: int


def parse(file: str) -> list[list[str]]:
    return [list(line) for line in read_data_as_lines(12, file)]


def is_valid_cell(x: int, y: int, rows: int, cols: int) -> bool:
    """Check if coordinates are within grid bounds."""
    return 0 <= x < rows and 0 <= y < cols


def is_valid_and_same_plant(
    x: int, y: int, plant: str, grid: list[list[str]], rows: int, cols: int
) -> bool:
    """Check if cell is valid and contains the same plant type."""
    return is_valid_cell(x, y, rows, cols) and grid[x][y] == plant


def flood_fill_region(
    r: int,
    c: int,
    plant: str,
    grid: list[list[str]],
    visited: list[list[bool]],
    rows: int,
    cols: int,
) -> tuple[int, int]:
    """
    Use flood fill (DFS) to find all cells in a region and calculate area/perimeter.

    Args:
        r, c: Starting coordinates
        plant: Plant type for this region
        grid: 2D grid of plant types
        visited: Tracking visited cells
        rows, cols: Grid dimensions

    Returns:
        Tuple of (area, perimeter)
    """
    stack = [(r, c)]
    visited[r][c] = True
    area, perimeter = 0, 0

    while stack:
        x, y = stack.pop()
        area += 1

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            if is_valid_and_same_plant(nx, ny, plant, grid, rows, cols):
                if not visited[nx][ny]:
                    stack.append((nx, ny))
                    visited[nx][ny] = True
            else:
                # Either out of bounds or different plant - counts as perimeter
                perimeter += 1

    return area, perimeter


def count_continuous_segments(sorted_coords: list[int]) -> int:
    """
    Count continuous segments in sorted coordinates.

    Examples:
        [0, 1, 2, 5, 6] -> 2 segments: [0,1,2] and [5,6]
        [0, 1, 2] -> 1 segment
        [0, 2, 4] -> 3 segments
    """
    if not sorted_coords:
        return 0

    segments = 1
    for i in range(1, len(sorted_coords)):
        if sorted_coords[i] != sorted_coords[i - 1] + 1:
            segments += 1  # Gap found, new segment starts
    return segments


def count_sides_from_boundaries(boundaries: set[tuple[tuple[int, int], str]]) -> int:
    """
    Count continuous fence sides from boundary edges.

    For horizontal directions (U/D): groups by row, finds continuous column sequences
    For vertical directions (L/R): groups by column, finds continuous row sequences

    Args:
        boundaries: Set of ((x, y), direction) tuples where direction is 'U', 'D', 'L', or 'R'

    Returns:
        Total number of continuous sides
    """
    total_sides = 0

    # Process horizontal sides (U and D)
    for direction in ["U", "D"]:
        edges = [(x, y) for (x, y), d in boundaries if d == direction]

        # Group by row (x coordinate)
        by_row = {}
        for x, y in edges:
            by_row.setdefault(x, []).append(y)

        # Count continuous segments in each row
        for row, cols in by_row.items():
            cols.sort()
            total_sides += count_continuous_segments(cols)

    # Process vertical sides (L and R)
    for direction in ["L", "R"]:
        edges = [(x, y) for (x, y), d in boundaries if d == direction]

        # Group by column (y coordinate)
        by_col = {}
        for x, y in edges:
            by_col.setdefault(y, []).append(x)

        # Count continuous segments in each column
        for col, rows in by_col.items():
            rows.sort()
            total_sides += count_continuous_segments(rows)

    return total_sides


def calculate_area_and_perimeter(grid: list[list[str]]) -> list[Region]:
    """
    Find all regions in the grid and calculate their areas and perimeters.

    A region is a connected group of cells with the same plant type.
    Perimeter counts edges that border different plants or the grid boundary.
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    results = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant = grid[r][c]
                area, perimeter = flood_fill_region(
                    r, c, plant, grid, visited, rows, cols
                )
                results.append(Region(plant, area, perimeter))

    return results


def price_perimeter(file: str) -> int:
    grid = parse(file)
    regions = calculate_area_and_perimeter(grid)
    return sum(region.area * region.perimeter for region in regions)


def find_region_cells(
    start_x: int,
    start_y: int,
    grid: list[list[str]],
    visited: list[list[bool]],
    rows: int,
    cols: int,
) -> list[tuple[int, int]]:
    """Find all cells in the same region using BFS."""
    queue = deque([(start_x, start_y)])
    region_cells = []
    plant = grid[start_x][start_y]
    visited[start_x][start_y] = True

    while queue:
        cx, cy = queue.popleft()
        region_cells.append((cx, cy))

        for dx, dy in DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            if (
                is_valid_and_same_plant(nx, ny, plant, grid, rows, cols)
                and not visited[nx][ny]
            ):
                visited[nx][ny] = True
                queue.append((nx, ny))

    return region_cells


def count_perimeter_sides(
    cells: list[tuple[int, int]], grid: list[list[str]], rows: int, cols: int
) -> int:
    """Count perimeter sides for a region."""
    sides = 0
    for x, y in cells:
        plant = grid[x][y]
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if not is_valid_and_same_plant(nx, ny, plant, grid, rows, cols):
                sides += 1
    return sides


def calculate_area_and_sides(grid: list[list[str]]) -> list[tuple[str, int, int]]:
    """Calculate area and sides for each region using flood fill with direction tracking."""
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def flood_fill(r: int, c: int, plant: str) -> tuple[int, int]:
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
                if is_valid_and_same_plant(nx, ny, plant, grid, rows, cols):
                    if not visited[nx][ny]:
                        stack.append((nx, ny))
                        visited[nx][ny] = True
                else:
                    # Out of bounds or different plant - add boundary segment
                    boundaries.add(((x, y), direction))

        # Count continuous sides from boundary edges
        sides = count_sides_from_boundaries(boundaries)
        return area, sides

    results = []
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant = grid[r][c]
                area, sides = flood_fill(r, c, plant)
                results.append((plant, area, sides))
    return results


def calculate_total_price(grid: list[list[str]]) -> int:
    """Calculate total price for all regions (area * perimeter)."""
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    total_price = 0

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                region_cells = find_region_cells(i, j, grid, visited, rows, cols)
                area = len(region_cells)
                sides = count_perimeter_sides(region_cells, grid, rows, cols)
                total_price += area * sides

    return total_price


def price_by_area_and_sides(file: str) -> int:
    grid = parse(file)
    regions = calculate_area_and_sides(grid)
    return sum(area * sides for plant, area, sides in regions)


if __name__ == "__main__":
    # Part 1
    run(
        price_perimeter,
        [
            ("example", 140),
            ("example_xo", 772),
            ("example_RIC", 1930),
            ("puzzle_input", 1488414),
        ],
    )

    # Part 2
    run(
        price_by_area_and_sides,
        [
            ("example", 80),
            ("example_xo", 436),
            ("example_EE", 236),
            ("example_AA", 368),
            ("puzzle_input", 911750),
        ],
    )
