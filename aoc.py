import os
import inspect
from dataclasses import dataclass
from typing import Callable, Any


# ========== Type Aliases ==========

Grid = list[list[Any]]


# ========== Coordinate Class ==========


@dataclass(frozen=True)
class Coord:
    """Immutable 2D coordinate with row and column components."""

    row: int
    col: int

    def __add__(self, other: "Coord") -> "Coord":
        """Add two coordinates component-wise."""
        return Coord(self.row + other.row, self.col + other.col)

    def __sub__(self, other: "Coord") -> "Coord":
        """Subtract two coordinates component-wise."""
        return Coord(self.row - other.row, self.col - other.col)

    def in_bounds(
        self, max_bounds: "Coord", min_bounds: "Coord | None" = None
    ) -> bool:
        """Check if coordinate is within bounds (inclusive)."""
        min_bounds = min_bounds or Coord(0, 0)
        return (
            min_bounds.row <= self.row <= max_bounds.row
            and min_bounds.col <= self.col <= max_bounds.col
        )


# Direction constants as class attributes
Coord.ZERO = Coord(0, 0)
Coord.UP = Coord(-1, 0)
Coord.RIGHT = Coord(0, 1)
Coord.DOWN = Coord(1, 0)
Coord.LEFT = Coord(0, -1)
Coord.UP_LEFT = Coord(-1, -1)
Coord.DOWN_LEFT = Coord(1, -1)
Coord.UP_RIGHT = Coord(-1, 1)
Coord.DOWN_RIGHT = Coord(1, 1)

Coord.DIRECTIONS_CARDINAL = [Coord.UP, Coord.RIGHT, Coord.DOWN, Coord.LEFT]
Coord.DIRECTIONS_INTERCARDINAL = [Coord.UP_LEFT, Coord.UP_RIGHT, Coord.DOWN_LEFT, Coord.DOWN_RIGHT]
Coord.DIRECTIONS_ALL = Coord.DIRECTIONS_CARDINAL + Coord.DIRECTIONS_INTERCARDINAL
Coord.TURN_CLOCKWISE = {
    Coord.UP: Coord.RIGHT,
    Coord.RIGHT: Coord.DOWN,
    Coord.DOWN: Coord.LEFT,
    Coord.LEFT: Coord.UP,
}


# ========== Testing Utilities ==========

TITLE_COLOR = "\033[100m"
FALSE_COLOR = "\033[91m"
TRUE_COLOR = "\033[92m"
END_COLOR = "\033[0m"


@dataclass
class TestCase:
    """A single test case with data file and expected output."""

    data_file: str
    expected: Any


def run(func: Callable[[str], Any], test_cases: list[TestCase]) -> None:
    """
    Execute test cases for a given function and report results.

    Args:
        func: Function to test (takes string data_file, returns any value)
        test_cases: List of TestCase objects

    The function prints colored output:
    - Green for passing tests showing the actual result
    - Red for failing tests showing expected vs actual
    - Summary line showing total pass/fail count
    """
    filename = os.path.basename(inspect.stack()[1].filename)
    print(f"{TITLE_COLOR}{filename}: {func.__name__}{END_COLOR}")

    passed = 0
    failed = 0

    for test_case in test_cases:
        try:
            actual = func(test_case.data_file)
            if test_case.expected == actual:
                print(f"  {test_case.data_file}: {TRUE_COLOR}{actual}{END_COLOR}")
                passed += 1
            else:
                print(
                    f"  {test_case.data_file}: {FALSE_COLOR}Expected {test_case.expected} but actual is {actual}{END_COLOR}"
                )
                failed += 1
        except Exception as e:
            print(
                f"  {test_case.data_file}: {FALSE_COLOR}ERROR: {type(e).__name__}: {e}{END_COLOR}"
            )
            failed += 1

    # Print summary
    total = passed + failed
    summary_color = TRUE_COLOR if failed == 0 else FALSE_COLOR
    print(f"{summary_color}  {passed}/{total} tests passed{END_COLOR}")
    print()




# ========== Coordinate Functions ==========


def filter_coords_in_bounds(
    coords: list[Coord], max_bounds: Coord, min_bounds: Coord | None = None
) -> list[Coord]:
    """Filter coordinates to only those within bounds."""
    return [c for c in coords if c.in_bounds(max_bounds, min_bounds)]


# ========== Matrix/Grid Functions ==========


def matrix_size(matrix: Grid) -> Coord:
    """Return size of matrix as Coord(rows, cols)."""
    return Coord(len(matrix), len(matrix[0]))


def matrix_max_bounds(matrix: Grid) -> Coord:
    """Return maximum valid indices as Coord(max_row, max_col)."""
    size = matrix_size(matrix)
    return Coord(size.row - 1, size.col - 1)


def matrix_contains_coord(matrix: Grid, coord: Coord) -> bool:
    """Check if coordinate is within matrix bounds."""
    return coord.in_bounds(matrix_max_bounds(matrix))


def matrix_get(matrix: Grid, coord: Coord) -> Any:
    """Get value at coordinate in matrix."""
    return matrix[coord.row][coord.col]


def find_first(matrix: Grid, value: Any) -> Coord | None:
    """Find first occurrence of value in matrix, return coordinate or None."""
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == value:
                return Coord(r, c)
    return None


def find_all(matrix: Grid, value: Any) -> list[Coord]:
    """Find all occurrences of value in matrix, return list of coordinates."""
    return [
        Coord(r, c)
        for r, row in enumerate(matrix)
        for c, cell in enumerate(row)
        if cell == value
    ]


# ========== Data Reading ==========


def read_data(data_file: str) -> str:
    """Read puzzle input file and return contents as string."""
    try:
        with open(f"./data/{data_file}", "r") as f:
            return f.read().strip()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}")
    except IOError as e:
        raise IOError(f"Error reading file: {e}")


def read_data_as_lines(data_file: str, strip_whitespace: bool = True) -> list[str]:
    """Read puzzle input file and return as list of lines."""
    lines = read_data(data_file).splitlines()
    return (
        [line.strip() for line in lines if line.strip()] if strip_whitespace else lines
    )


# ========== Exports ==========

__all__ = [
    # Coordinate class and Grid type
    "Coord",
    "Grid",
    # Testing
    "TestCase",
    "run",
    # Coordinate functions
    "filter_coords_in_bounds",
    # Matrix functions
    "matrix_size",
    "matrix_max_bounds",
    "matrix_contains_coord",
    "matrix_get",
    "find_first",
    "find_all",
    # Data reading
    "read_data",
    "read_data_as_lines",
]


if __name__ == "__main__":
    print("Advent of Code 2024")
