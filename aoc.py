import os
import inspect
from dataclasses import dataclass
from typing import Callable, Any


# ========== Type Aliases ==========

Coord = tuple[int, int]
Grid = list[list[Any]]


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
                print(f"  {test_case.data_file}: {FALSE_COLOR}Expected {test_case.expected} but actual is {actual}{END_COLOR}")
                failed += 1
        except Exception as e:
            print(f"  {test_case.data_file}: {FALSE_COLOR}ERROR: {type(e).__name__}: {e}{END_COLOR}")
            failed += 1

    # Print summary
    total = passed + failed
    summary_color = TRUE_COLOR if failed == 0 else FALSE_COLOR
    print(f"{summary_color}  {passed}/{total} tests passed{END_COLOR}")
    print()


# ========== Direction Constants ==========

ZERO: Coord = (0, 0)
UP: Coord = (-1, 0)
RIGHT: Coord = (0, 1)
DOWN: Coord = (1, 0)
LEFT: Coord = (0, -1)
UP_LEFT: Coord = (-1, -1)
DOWN_LEFT: Coord = (1, -1)
UP_RIGHT: Coord = (-1, 1)
DOWN_RIGHT: Coord = (1, 1)

DIRECTIONS_CARDINAL: list[Coord] = [UP, RIGHT, DOWN, LEFT]
DIRECTIONS_INTERCARDINAL: list[Coord] = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
DIRECTIONS_ALL: list[Coord] = DIRECTIONS_CARDINAL + DIRECTIONS_INTERCARDINAL
TURN_CLOCKWISE: dict[Coord, Coord] = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


# ========== Coordinate Functions ==========

def is_in_range(value: int, min_val: int, max_val: int) -> bool:
    """Check if value is between min_val and max_val (inclusive)."""
    return min_val <= value <= max_val


def coord_add(a: Coord, b: Coord) -> Coord:
    """Add two coordinates element-wise."""
    return (a[0] + b[0], a[1] + b[1])


def coord_sub(a: Coord, b: Coord) -> Coord:
    """Subtract coordinate b from a element-wise."""
    return (a[0] - b[0], a[1] - b[1])


def coord_in_bounds(coord: Coord, max_bounds: Coord, min_bounds: Coord = ZERO) -> bool:
    """Check if coordinate is within bounds (inclusive)."""
    return (is_in_range(coord[0], min_bounds[0], max_bounds[0]) and
            is_in_range(coord[1], min_bounds[1], max_bounds[1]))


def filter_coords_in_bounds(coords: list[Coord], max_bounds: Coord, min_bounds: Coord = ZERO) -> list[Coord]:
    """Filter coordinates to only those within bounds."""
    return [c for c in coords if coord_in_bounds(c, max_bounds, min_bounds)]


# ========== Matrix/Grid Functions ==========

def matrix_size(matrix: Grid) -> Coord:
    """Return (rows, cols) size of matrix."""
    return (len(matrix), len(matrix[0]))


def matrix_max_bounds(matrix: Grid) -> Coord:
    """Return maximum valid indices as (max_row, max_col)."""
    rows, cols = matrix_size(matrix)
    return (rows - 1, cols - 1)


def matrix_contains_coord(matrix: Grid, coord: Coord) -> bool:
    """Check if coordinate is within matrix bounds."""
    return coord_in_bounds(coord, matrix_max_bounds(matrix), ZERO)


def matrix_get(matrix: Grid, coord: Coord) -> Any:
    """Get value at coordinate in matrix."""
    return matrix[coord[0]][coord[1]]


def find_first(matrix: Grid, value: Any) -> Coord | None:
    """Find first occurrence of value in matrix, return coordinate or None."""
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == value:
                return (r, c)
    return None


def find_all(matrix: Grid, value: Any) -> list[Coord]:
    """Find all occurrences of value in matrix, return list of coordinates."""
    return [
        (r, c)
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
    # Type aliases
    'Coord',
    'Grid',
    # Testing
    'TestCase',
    'run',
    # Colors
    'TITLE_COLOR',
    'FALSE_COLOR',
    'TRUE_COLOR',
    'END_COLOR',
    # Direction constants
    'ZERO',
    'UP',
    'DOWN',
    'LEFT',
    'RIGHT',
    'UP_LEFT',
    'UP_RIGHT',
    'DOWN_LEFT',
    'DOWN_RIGHT',
    'DIRECTIONS_CARDINAL',
    'DIRECTIONS_INTERCARDINAL',
    'DIRECTIONS_ALL',
    'TURN_CLOCKWISE',
    # Coordinate functions
    'is_in_range',
    'coord_add',
    'coord_sub',
    'coord_in_bounds',
    'filter_coords_in_bounds',
    # Matrix functions
    'matrix_size',
    'matrix_max_bounds',
    'matrix_contains_coord',
    'matrix_get',
    'find_first',
    'find_all',
    # Data reading
    'read_data',
    'read_data_as_lines',
]


if __name__ == "__main__":
    print("Advent of Code 2024")
