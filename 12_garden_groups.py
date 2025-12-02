from aoc import (
    read_data_as_char_grid,
    run,
    TestCase,
    Coord,
    create_visited_grid,
    matrix_size,
    matrix_max_bounds,
    matrix_get,
    count_continuous_segments,
)
from collections import deque
from dataclasses import dataclass


@dataclass
class Region:
    plant: str
    area: int
    perimeter: int


def parse(data_file: str) -> list[list[str]]:
    return read_data_as_char_grid(data_file)


def is_valid_and_same_plant(
    coord: Coord, plant: str, grid: list[list[str]]
) -> bool:
    """Check if cell is valid and contains the same plant type."""
    return coord.in_bounds(matrix_max_bounds(grid)) and matrix_get(grid, coord) == plant


def flood_fill_region(
    start: Coord,
    plant: str,
    grid: list[list[str]],
    visited: list[list[bool]],
) -> tuple[int, int]:
    """
    Use flood fill (DFS) to find all cells in a region and calculate area/perimeter.

    Args:
        start: Starting coordinate
        plant: Plant type for this region
        grid: 2D grid of plant types
        visited: Tracking visited cells

    Returns:
        Tuple of (area, perimeter)
    """
    stack = [start]
    visited[start.row][start.col] = True
    area, perimeter = 0, 0

    while stack:
        current = stack.pop()
        area += 1

        for direction in Coord.DIRECTIONS_CARDINAL:
            neighbor = current + direction

            if is_valid_and_same_plant(neighbor, plant, grid):
                if not visited[neighbor.row][neighbor.col]:
                    stack.append(neighbor)
                    visited[neighbor.row][neighbor.col] = True
            else:
                # Either out of bounds or different plant - counts as perimeter
                perimeter += 1

    return area, perimeter


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
    size = matrix_size(grid)
    visited = create_visited_grid(size)
    results = []

    for r in range(size.row):
        for c in range(size.col):
            if not visited[r][c]:
                coord = Coord(r, c)
                plant = matrix_get(grid, coord)
                area, perimeter = flood_fill_region(coord, plant, grid, visited)
                results.append(Region(plant, area, perimeter))

    return results


def price_perimeter(file: str) -> int:
    grid = parse(file)
    regions = calculate_area_and_perimeter(grid)
    return sum(region.area * region.perimeter for region in regions)


def find_region_cells(
    start: Coord,
    grid: list[list[str]],
    visited: list[list[bool]],
) -> list[Coord]:
    """Find all cells in the same region using BFS."""
    queue = deque([start])
    region_cells = []
    plant = matrix_get(grid, start)
    visited[start.row][start.col] = True

    while queue:
        current = queue.popleft()
        region_cells.append(current)

        for direction in Coord.DIRECTIONS_CARDINAL:
            neighbor = current + direction
            if (
                is_valid_and_same_plant(neighbor, plant, grid)
                and not visited[neighbor.row][neighbor.col]
            ):
                visited[neighbor.row][neighbor.col] = True
                queue.append(neighbor)

    return region_cells


def count_perimeter_sides(cells: list[Coord], grid: list[list[str]]) -> int:
    """Count perimeter sides for a region."""
    sides = 0
    for coord in cells:
        plant = matrix_get(grid, coord)
        for direction in Coord.DIRECTIONS_CARDINAL:
            neighbor = coord + direction
            if not is_valid_and_same_plant(neighbor, plant, grid):
                sides += 1
    return sides


def calculate_area_and_sides(grid: list[list[str]]) -> list[tuple[str, int, int]]:
    """Calculate area and sides for each region using flood fill with direction tracking."""
    size = matrix_size(grid)
    visited = create_visited_grid(size)

    def flood_fill(start: Coord, plant: str) -> tuple[int, int]:
        stack = [start]
        visited[start.row][start.col] = True
        area = 0
        boundaries = set()  # Store all boundary edges as unique segments

        direction_map = {
            Coord.UP: "U",
            Coord.DOWN: "D",
            Coord.LEFT: "L",
            Coord.RIGHT: "R",
        }

        while stack:
            current = stack.pop()
            area += 1
            # Check all 4 directions
            for direction in Coord.DIRECTIONS_CARDINAL:
                neighbor = current + direction
                if is_valid_and_same_plant(neighbor, plant, grid):
                    if not visited[neighbor.row][neighbor.col]:
                        stack.append(neighbor)
                        visited[neighbor.row][neighbor.col] = True
                else:
                    # Out of bounds or different plant - add boundary segment
                    boundaries.add(((current.row, current.col), direction_map[direction]))

        # Count continuous sides from boundary edges
        sides = count_sides_from_boundaries(boundaries)
        return area, sides

    results = []
    for r in range(size.row):
        for c in range(size.col):
            if not visited[r][c]:
                coord = Coord(r, c)
                plant = matrix_get(grid, coord)
                area, sides = flood_fill(coord, plant)
                results.append((plant, area, sides))
    return results


def calculate_total_price(grid: list[list[str]]) -> int:
    """Calculate total price for all regions (area * perimeter)."""
    size = matrix_size(grid)
    visited = create_visited_grid(size)
    total_price = 0

    for r in range(size.row):
        for c in range(size.col):
            if not visited[r][c]:
                coord = Coord(r, c)
                region_cells = find_region_cells(coord, grid, visited)
                area = len(region_cells)
                sides = count_perimeter_sides(region_cells, grid)
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
            TestCase("12_example", 140),
            TestCase("12_example_xo", 772),
            TestCase("12_example_RIC", 1930),
            TestCase("12_puzzle_input", 1488414),
        ],
    )

    # Part 2
    run(
        price_by_area_and_sides,
        [
            TestCase("12_example", 80),
            TestCase("12_example_xo", 436),
            TestCase("12_example_EE", 236),
            TestCase("12_example_AA", 368),
            TestCase("12_puzzle_input", 911750),
        ],
    )
