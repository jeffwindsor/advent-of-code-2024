"""Grid utility functions."""

from typing import Any, Iterator
from .coord import Coord


# Type alias
Grid = list[list[Any]]


def grid_size(grid: Grid) -> Coord:
    """Return size of grid as Coord(rows, cols)."""
    return Coord(len(grid), len(grid[0]))


def grid_max_bounds(grid: Grid) -> Coord:
    """Return maximum valid indices as Coord(max_row, max_col)."""
    size = grid_size(grid)
    return Coord(size.row - 1, size.col - 1)


def grid_contains_coord(grid: Grid, coord: Coord) -> bool:
    """Check if coordinate is within grid bounds."""
    return coord.in_bounds(grid_max_bounds(grid))


def grid_get(grid: Grid, coord: Coord) -> Any:
    """Get value at coordinate in grid."""
    return grid[coord.row][coord.col]


def grid_set(grid: Grid, coord: Coord, value: Any) -> None:
    """Set value at coordinate in grid."""
    grid[coord.row][coord.col] = value


def find_first(grid: Grid, value: Any) -> Coord | None:
    """Find first occurrence of value in grid, return coordinate or None."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == value:
                return Coord(r, c)
    return None


def find_all(grid: Grid, value: Any) -> list[Coord]:
    """Find all occurrences of value in grid, return list of coordinates."""
    return [
        Coord(r, c)
        for r, row in enumerate(grid)
        for c, cell in enumerate(row)
        if cell == value
    ]


def grid_coords(grid: Grid) -> Iterator[tuple[Coord, Any]]:
    """
    Iterate over (coordinate, value) pairs in grid.

    Args:
        grid: 2D grid

    Yields:
        Tuples of (Coord, value) for each cell in the grid
    """
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            yield Coord(r, c), value


def search_in_direction(
    grid: Grid,
    start: Coord,
    direction: Coord,
    target: str
) -> bool:
    """
    Search for a string in the grid following a specific direction.

    Args:
        grid: 2D grid to search in
        start: Starting coordinate
        direction: Direction vector to follow
        target: String to search for

    Returns:
        True if the target string is found in the specified direction
    """
    max_bounds = grid_max_bounds(grid)
    for i, char in enumerate(target):
        coord = Coord(start.row + i * direction.row, start.col + i * direction.col)
        if not coord.in_bounds(max_bounds) or grid_get(grid, coord) != char:
            return False
    return True


def group_by_value(grid: Grid, exclude: Any | None = None) -> dict[Any, list[Coord]]:
    """
    Group coordinates by their cell values.

    Args:
        grid: 2D grid
        exclude: Optional value to exclude from grouping

    Returns:
        Dictionary mapping values to lists of coordinates with that value
    """
    result = {}
    for coord, value in grid_coords(grid):
        if value != exclude:
            result.setdefault(value, []).append(coord)
    return result


def create_visited_grid(size: Coord, initial_value: bool = False) -> list[list[bool]]:
    """
    Create a boolean grid for visited tracking.

    Args:
        size: Size of the grid as Coord(rows, cols)
        initial_value: Initial value for all cells (default: False)

    Returns:
        2D list of booleans
    """
    return [[initial_value] * size.col for _ in range(size.row)]


def create_grid(size: int, initial_value: Any = ".") -> Grid:
    """
    Create a square grid filled with initial value.

    Args:
        size: Size of the square grid (size x size)
        initial_value: Value to fill the grid with (default: '.')

    Returns:
        2D list initialized with the specified value
    """
    return [[initial_value for _ in range(size)] for _ in range(size)]


__all__ = [
    "Grid",
    "grid_size",
    "grid_max_bounds",
    "grid_contains_coord",
    "grid_get",
    "grid_set",
    "find_first",
    "find_all",
    "grid_coords",
    "search_in_direction",
    "group_by_value",
    "create_visited_grid",
    "create_grid",
]
