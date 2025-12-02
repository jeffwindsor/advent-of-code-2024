import os
import inspect
import time
import tracemalloc
from dataclasses import dataclass
from typing import Callable, Any, Iterator
from collections import deque
from heapq import heappush, heappop


# ========== Configuration ==========


def _is_perf_enabled() -> bool:
    """Check if performance metrics should be collected via AOC_PERF env var."""
    value = os.getenv('AOC_PERF', '').lower()
    return value in ('1', 'true', 'yes')


# Cache at module load time for zero per-test overhead
PERF_ENABLED = _is_perf_enabled()


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

TITLE_COLOR = "\033[34m"
FALSE_COLOR = "\033[91m"
TRUE_COLOR = "\033[92m"
END_COLOR = "\033[0m"


def format_time(seconds: float) -> str:
    """Format time duration for display."""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.0f}µs"
    elif seconds < 1.0:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def format_memory(bytes_used: int) -> str:
    """Format memory usage for display."""
    if bytes_used < 1024:
        return f"{bytes_used}B"
    elif bytes_used < 1024 * 1024:
        return f"{bytes_used / 1024:.1f}KB"
    else:
        return f"{bytes_used / (1024 * 1024):.1f}MB"


@dataclass
class TestCase:
    """A single test case with data file and expected output."""

    data_file: str
    expected: Any


def run(func: Callable[[str], Any], test_cases: list[TestCase]) -> None:
    """
    Execute test cases for a given function and report results with performance metrics.

    Args:
        func: Function to test (takes string data_file, returns any value)
        test_cases: List of TestCase objects

    The function prints colored output:
    - Green for passing tests showing the actual result with time and memory
    - Red for failing tests showing expected vs actual
    - Summary line showing total pass/fail count
    """
    filename = os.path.basename(inspect.stack()[1].filename)
    print(f"{TITLE_COLOR}{func.__name__}{END_COLOR}")

    passed = 0
    failed = 0

    for test_case in test_cases:
        try:
            # Start performance tracking (if enabled)
            if PERF_ENABLED:
                tracemalloc.start()
                start_time = time.perf_counter()

            # Execute test
            actual = func(test_case.data_file)

            # Capture and format metrics (if enabled)
            if PERF_ENABLED:
                elapsed_time = time.perf_counter() - start_time
                current_mem, peak_mem = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                time_str = format_time(elapsed_time)
                mem_str = format_memory(peak_mem)
                metrics = f" ({time_str}, {mem_str})"
            else:
                metrics = ""

            # Report results
            if test_case.expected == actual:
                print(f"  {test_case.data_file}: {TRUE_COLOR}{actual}{metrics}{END_COLOR}")
                passed += 1
            else:
                print(
                    f"  {test_case.data_file}: {FALSE_COLOR}Expected {test_case.expected} but actual is {actual}{metrics}{END_COLOR}"
                )
                failed += 1
        except Exception as e:
            # Stop tracking on error (if enabled)
            if PERF_ENABLED and tracemalloc.is_tracing():
                tracemalloc.stop()
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
    start: Any,
    neighbors_func: Callable[[Any], list[Any]],
    goal_func: Callable[[Any], bool] | None = None,
) -> dict[Any, int] | list[Any]:
    """
    Generic breadth-first search algorithm.

    Args:
        start: Starting state (Coord, tuple, or any hashable type)
        neighbors_func: Function that returns valid neighbors for a state
        goal_func: Optional function to check if goal is reached

    Returns:
        If goal_func is None: dict mapping states to distances from start
        If goal_func provided: list of states forming path to goal, or empty list if no path

    Examples:
        # Find all distances
        >>> distances = bfs(start_coord, neighbors_func)

        # Find path to goal
        >>> path = bfs(start_coord, neighbors_func, lambda c: c == goal)
    """
    queue = deque([start])
    visited = {start}
    distances = {start: 0}
    parents = {start: None}

    while queue:
        current = queue.popleft()

        if goal_func and goal_func(current):
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parents[node]
            return list(reversed(path))

        for neighbor in neighbors_func(current):
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[current] + 1
                parents[neighbor] = current
                queue.append(neighbor)

    return distances if not goal_func else []


def dfs(
    start: Coord,
    neighbors_func: Callable[[Coord], list[Coord]],
    goal_func: Callable[[Coord], bool],
) -> list[Coord] | None:
    """
    Generic depth-first search algorithm.
    Optimized with parent tracking for O(n) time and memory complexity.

    Args:
        start: Starting coordinate
        neighbors_func: Function that returns valid neighbors for a coordinate
        goal_func: Function to check if goal is reached

    Returns:
        List of coordinates forming path to goal, or None if no path found

    Note:
        Uses parent tracking and backtracking for efficient O(n) path construction,
        avoiding the O(n²) cost of incrementally building paths during search.
    """
    stack = [(start, None)]  # (current, parent)
    parent_map = {}
    visited = set()

    while stack:
        current, parent = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        parent_map[current] = parent

        if goal_func(current):
            # Reconstruct path by backtracking from goal to start
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent_map[node]
            return list(reversed(path))

        for neighbor in neighbors_func(current):
            if neighbor not in visited:
                stack.append((neighbor, current))

    return None


def dfs_grid_path(
    grid: Grid,
    start: Coord,
    end: Coord,
    walkable_values: set[Any],
) -> list[Coord]:
    """
    Convenience wrapper for depth-first search through a grid maze.

    This is a specialized interface to the generic dfs() function,
    optimized for grid-based pathfinding problems.

    Args:
        grid: 2D grid/matrix to search through
        start: Starting coordinate
        end: Goal coordinate
        walkable_values: Set of grid values that can be traversed

    Returns:
        List of coordinates forming path from start to end, or empty list if no path found

    Example:
        >>> maze = [['#', '.', '#'], ['.', '.', '.'], ['#', '.', '#']]
        >>> path = dfs_grid_path(maze, Coord(0,1), Coord(2,1), {'.'}  )
        >>> len(path) > 0
        True

    Note:
        This wrapper uses the generic dfs() implementation with parent tracking
        for efficient O(n) time and memory complexity.
    """
    def neighbors_func(coord: Coord) -> list[Coord]:
        """Get valid neighboring coordinates in the grid."""
        neighbors = []
        for direction in Coord.DIRECTIONS_CARDINAL:
            next_position = coord + direction
            if (
                matrix_contains_coord(grid, next_position)
                and matrix_get(grid, next_position) in walkable_values
            ):
                neighbors.append(next_position)
        return neighbors

    def goal_func(coord: Coord) -> bool:
        """Check if we've reached the goal."""
        return coord == end

    # Use the generic dfs implementation
    result = dfs(start, neighbors_func, goal_func)
    return result if result is not None else []


def dijkstra(
    start: Any,
    neighbors_func: Callable[[Any], list[tuple[Any, int]]],
    goal: Any | None = None,
) -> dict[Any, int]:
    """
    Dijkstra's shortest path algorithm (generalized for any hashable state).

    Args:
        start: Starting state (can be Coord, tuple, or any hashable type)
        neighbors_func: Function returning list of (neighbor_state, cost) tuples
        goal: Optional goal state (returns early if found)

    Returns:
        Dictionary mapping states to shortest distances from start

    Examples:
        # Original usage with Coord
        >>> distances = dijkstra(Coord(0,0), neighbors_func)

        # New usage with state tuples (coord, direction)
        >>> distances = dijkstra((Coord(0,0), 0), state_neighbors_func)
    """
    counter = 0
    pq = [(0, counter, start)]
    distances = {start: 0}
    visited = set()

    while pq:
        dist, _, current = heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if goal and current == goal:
            return distances

        for neighbor, cost in neighbors_func(current):
            new_dist = dist + cost
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                counter += 1
                heappush(pq, (new_dist, counter, neighbor))

    return distances


# ========== Number/Math Utilities ==========


def count_continuous_segments(sorted_coords: list[int]) -> int:
    """
    Count continuous segments in sorted coordinates.

    Args:
        sorted_coords: List of sorted integers

    Returns:
        Number of continuous segments

    Examples:
        >>> count_continuous_segments([0, 1, 2, 5, 6])
        2  # Two segments: [0,1,2] and [5,6]
        >>> count_continuous_segments([0, 1, 2])
        1  # One segment
        >>> count_continuous_segments([0, 2, 4])
        3  # Three segments
    """
    if not sorted_coords:
        return 0

    segments = 1
    for i in range(1, len(sorted_coords)):
        if sorted_coords[i] != sorted_coords[i - 1] + 1:
            segments += 1
    return segments


def count_digits(n: int) -> int:
    """
    Count the number of digits in a positive integer.

    Args:
        n: A non-negative integer

    Returns:
        The number of digits in n (e.g., 123 -> 3, 0 -> 1)

    Examples:
        >>> count_digits(0)
        1
        >>> count_digits(123)
        3
        >>> count_digits(9999)
        4
    """
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count


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


def matrix_set(matrix: Grid, coord: Coord, value: Any) -> None:
    """Set value at coordinate in matrix."""
    matrix[coord.row][coord.col] = value


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


def search_in_direction(
    matrix: Grid,
    start: Coord,
    direction: Coord,
    target: str
) -> bool:
    """
    Search for a string in the matrix following a specific direction.

    Args:
        matrix: 2D grid to search in
        start: Starting coordinate
        direction: Direction vector to follow
        target: String to search for

    Returns:
        True if the target string is found in the specified direction
    """
    max_bounds = matrix_max_bounds(matrix)
    for i, char in enumerate(target):
        coord = Coord(start.row + i * direction.row, start.col + i * direction.col)
        if not coord.in_bounds(max_bounds) or matrix_get(matrix, coord) != char:
            return False
    return True


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
    "dfs_grid_path",
    "dijkstra",
    # Number/Math utilities
    "count_continuous_segments",
    "count_digits",
    # Matrix functions
    "matrix_size",
    "matrix_max_bounds",
    "matrix_contains_coord",
    "matrix_get",
    "matrix_set",
    "find_first",
    "find_all",
    "matrix_coords",
    "search_in_direction",
    "group_by_value",
    "create_visited_grid",
    "create_grid",
    # Data reading
    "read_data",
    "read_data_as_lines",
    "read_data_as_char_grid",
    "read_data_as_int_grid",
    "parse_coord_pairs",
]


if __name__ == "__main__":
    print("Advent of Code 2024")
