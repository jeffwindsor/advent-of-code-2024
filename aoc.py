import os
import inspect
from dataclasses import dataclass
from typing import Callable, Any, Iterator
from collections import deque
from heapq import heappush, heappop


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

    def manhattan_distance(self, other: "Coord") -> int:
        """Calculate Manhattan distance to another coordinate."""
        return abs(self.row - other.row) + abs(self.col - other.col)

    def neighbors(
        self, max_bounds: "Coord", directions: list["Coord"] | None = None
    ) -> list["Coord"]:
        """
        Get valid neighbors within bounds.

        Args:
            max_bounds: Maximum coordinate bounds
            directions: List of direction vectors (default: DIRECTIONS_CARDINAL)

        Returns:
            List of valid neighbor coordinates
        """
        directions = directions or Coord.DIRECTIONS_CARDINAL
        return [
            neighbor
            for d in directions
            if (neighbor := self + d).in_bounds(max_bounds)
        ]


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
Coord.TURN_COUNTER_CLOCKWISE = {
    Coord.UP: Coord.LEFT,
    Coord.LEFT: Coord.DOWN,
    Coord.DOWN: Coord.RIGHT,
    Coord.RIGHT: Coord.UP,
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


# ========== Graph Algorithms ==========


def bfs(
    start: Coord,
    neighbors_func: Callable[[Coord], list[Coord]],
    goal_func: Callable[[Coord], bool] | None = None,
) -> dict[Coord, int] | list[Coord]:
    """
    Generic breadth-first search algorithm.

    Args:
        start: Starting coordinate
        neighbors_func: Function that returns valid neighbors for a coordinate
        goal_func: Optional function to check if goal is reached

    Returns:
        If goal_func is None: dict mapping coordinates to distances from start
        If goal_func provided: list of coordinates forming path to goal, or empty list if no path
    """
    queue = deque([(start, [start])])
    visited = {start}
    distances = {start: 0}

    while queue:
        current, path = queue.popleft()

        if goal_func and goal_func(current):
            return path

        for neighbor in neighbors_func(current):
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[current] + 1
                queue.append((neighbor, path + [neighbor]))

    return distances if not goal_func else []


def dfs(
    start: Coord,
    neighbors_func: Callable[[Coord], list[Coord]],
    goal_func: Callable[[Coord], bool],
) -> list[Coord] | None:
    """
    Generic depth-first search algorithm.

    Args:
        start: Starting coordinate
        neighbors_func: Function that returns valid neighbors for a coordinate
        goal_func: Function to check if goal is reached

    Returns:
        List of coordinates forming path to goal, or None if no path found
    """
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        if goal_func(current):
            return path

        for neighbor in neighbors_func(current):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None


def dijkstra(
    start: Coord,
    neighbors_func: Callable[[Coord], list[tuple[Coord, int]]],
    goal: Coord | None = None,
) -> dict[Coord, int]:
    """
    Dijkstra's shortest path algorithm.

    Args:
        start: Starting coordinate
        neighbors_func: Function returning list of (neighbor, cost) tuples
        goal: Optional goal coordinate (returns early if found)

    Returns:
        Dictionary mapping coordinates to shortest distances from start
    """
    pq = [(0, start)]
    distances = {start: 0}
    visited = set()

    while pq:
        dist, current = heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if goal and current == goal:
            return distances

        for neighbor, cost in neighbors_func(current):
            new_dist = dist + cost
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heappush(pq, (new_dist, neighbor))

    return distances


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


def matrix_coords(matrix: Grid) -> Iterator[tuple[Coord, Any]]:
    """
    Iterate over (coordinate, value) pairs in matrix.

    Args:
        matrix: 2D grid

    Yields:
        Tuples of (Coord, value) for each cell in the matrix
    """
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            yield Coord(r, c), value


def group_by_value(matrix: Grid, exclude: Any | None = None) -> dict[Any, list[Coord]]:
    """
    Group coordinates by their cell values.

    Args:
        matrix: 2D grid
        exclude: Optional value to exclude from grouping

    Returns:
        Dictionary mapping values to lists of coordinates with that value
    """
    result = {}
    for coord, value in matrix_coords(matrix):
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


def read_data_as_char_grid(data_file: str) -> Grid:
    """
    Read puzzle input file and return as 2D character grid.

    Returns:
        list[list[str]] where each inner list is a row of characters
    """
    return [list(line) for line in read_data_as_lines(data_file)]


def read_data_as_int_grid(data_file: str, empty_value: int = -1) -> Grid:
    """
    Read puzzle input file and return as 2D integer grid.

    Args:
        data_file: Path to input file
        empty_value: Value to use for non-digit characters (default: -1)

    Returns:
        list[list[int]] where each inner list is a row of integers
    """
    return [
        [int(char) if char.isdigit() else empty_value for char in line]
        for line in read_data_as_lines(data_file)
    ]


def parse_coord_pairs(data_file: str, separator: str = ",") -> list[tuple[int, int]]:
    """
    Parse lines of coordinate pairs into list of tuples.

    Args:
        data_file: Path to input file
        separator: Character separating coordinates (default: ',')

    Returns:
        List of (x, y) coordinate tuples

    Example:
        Input file with lines like "3,4" returns [(3, 4), ...]
    """
    return [
        tuple(map(int, line.split(separator)))
        for line in read_data_as_lines(data_file)
    ]


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
    # Graph algorithms
    "bfs",
    "dfs",
    "dijkstra",
    # Matrix functions
    "matrix_size",
    "matrix_max_bounds",
    "matrix_contains_coord",
    "matrix_get",
    "find_first",
    "find_all",
    "matrix_coords",
    "group_by_value",
    "create_visited_grid",
    # Data reading
    "read_data",
    "read_data_as_lines",
    "read_data_as_char_grid",
    "read_data_as_int_grid",
    "parse_coord_pairs",
]


if __name__ == "__main__":
    print("Advent of Code 2024")
