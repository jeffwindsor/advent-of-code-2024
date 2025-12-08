"""Grid utility functions and Grid class."""

from typing import Any, Iterator
from dataclasses import dataclass
from .coord import Coord


@dataclass
class Grid:
    """
    2D grid wrapper with coordinate-based access.

    Provides clean syntax for grid operations:
    - grid[coord] to access values
    - coord in grid to check bounds
    - Integrates seamlessly with Coord class
    """
    data: list[list[Any]]

    def __getitem__(self, coord: Coord) -> Any:
        """Access grid value using coordinate: grid[coord]."""
        return self.data[coord.row][coord.col]

    def __setitem__(self, coord: Coord, value: Any) -> None:
        """Set grid value using coordinate: grid[coord] = value."""
        self.data[coord.row][coord.col] = value

    def __contains__(self, coord: Coord) -> bool:
        """Check if coordinate is within bounds: coord in grid."""
        return coord.in_bounds(self.max_bounds)

    @property
    def size(self) -> Coord:
        """Return size of grid as Coord(rows, cols)."""
        return Coord(len(self.data), len(self.data[0]) if self.data else 0)

    @property
    def max_bounds(self) -> Coord:
        """Return maximum valid indices as Coord(max_row, max_col)."""
        size = self.size
        return Coord(size.row - 1, size.col - 1)

    def coords(self) -> Iterator[tuple[Coord, Any]]:
        """
        Iterate over (coordinate, value) pairs in grid.

        Yields:
            Tuples of (Coord, value) for each cell in the grid
        """
        for r, row in enumerate(self.data):
            for c, value in enumerate(row):
                yield Coord(r, c), value

    def find_first(self, value: Any) -> Coord | None:
        """Find first occurrence of value in grid, return coordinate or None."""
        for coord, cell_value in self.coords():
            if cell_value == value:
                return coord
        return None

    def find_all(self, value: Any) -> list[Coord]:
        """Find all occurrences of value in grid, return list of coordinates."""
        return [coord for coord, cell_value in self.coords() if cell_value == value]

    def group_by_value(self, exclude: Any | None = None) -> dict[Any, list[Coord]]:
        """
        Group coordinates by their cell values.

        Args:
            exclude: Optional value to exclude from grouping

        Returns:
            Dictionary mapping values to lists of coordinates with that value
        """
        result = {}
        for coord, value in self.coords():
            if value != exclude:
                result.setdefault(value, []).append(coord)
        return result

    def search_in_direction(self, start: Coord, direction: Coord, target: str) -> bool:
        """
        Search for a string in the grid following a specific direction.

        Args:
            start: Starting coordinate
            direction: Direction vector to follow
            target: String to search for

        Returns:
            True if the target string is found in the specified direction
        """
        for i, char in enumerate(target):
            coord = Coord(start.row + i * direction.row, start.col + i * direction.col)
            if coord not in self or self[coord] != char:
                return False
        return True

    @staticmethod
    def create_visited(size: Coord, initial_value: bool = False) -> "Grid":
        """
        Create a boolean grid for visited tracking.

        Args:
            size: Size of the grid as Coord(rows, cols)
            initial_value: Initial value for all cells (default: False)

        Returns:
            Grid instance with boolean values
        """
        data = [[initial_value] * size.col for _ in range(size.row)]
        return Grid(data)

    @staticmethod
    def create(size: int, initial_value: Any = ".") -> "Grid":
        """
        Create a square grid filled with initial value.

        Args:
            size: Size of the square grid (size x size)
            initial_value: Value to fill the grid with (default: '.')

        Returns:
            Grid instance initialized with the specified value
        """
        data = [[initial_value for _ in range(size)] for _ in range(size)]
        return Grid(data)


__all__ = ["Grid"]
