from aoc import (
    read_data_as_int_grid,
    run,
    TestCase,
    Coord,
    matrix_get,
    find_all,
    matrix_max_bounds,
    matrix_contains_coord,
)
from collections import deque


def find_paths_rec(
    matrix, start, current_path, is_valid_step, is_end, directions, memo
):
    """
    Generalized algorithm to find paths in a grid.

    Args:
        grid: 2D list representing the grid.
        row, col: Current position in the grid.
        current_path: List of (row, col) tuples representing the current path.
        memo: Dictionary to store previously computed results.
        is_valid_step: Function to validate a step (grid, row, col, next_row, next_col).
        is_end: Function to check if a position is the end condition (grid, row, col).

    Returns:
        A set of unique paths (as tuples of (row, col)).
    """
    key = (start, tuple(current_path))
    if key in memo:
        return memo[key]

    if is_end(matrix, start):
        return {tuple(current_path)}

    paths = set()
    for direction in directions:
        next = start + direction
        if matrix_contains_coord(matrix, next) and is_valid_step(matrix, start, next):
            paths |= find_paths_rec(
                matrix,
                next,
                current_path + [next],
                is_valid_step,
                is_end,
                directions,
                memo,
            )

    memo[key] = paths
    return paths


def bfs(matrix, start, directions, can_visit):
    """
    Perform BFS on a 2D matrix.

    :param matrix: 2D list representing the matrix
    :param start: Coord representing the starting position
    :param directions: list of coordinate offsets for each possible direction
    :return: List of visited positions in BFS order
    """
    hb = matrix_max_bounds(matrix)
    queue = deque([start])
    visited = set([start])
    order = []
    while queue:
        current = queue.popleft()
        order.append(current)

        for direction in directions:
            next_coord = current + direction
            # Check bounds and if the cell has not been visited
            if (
                next_coord.in_bounds(hb)
                and next_coord not in visited
                and can_visit(current, next_coord)
            ):
                visited.add(next_coord)
                queue.append(next_coord)

    return order


def parse(data_file):
    # problem wants to follow path of increasing values from 0, so EMPTY = -1
    return read_data_as_int_grid(data_file, empty_value=-1)


def find_reachable_nines(topographic_map, start_coord):
    paths = bfs(
        topographic_map,
        start_coord,
        Coord.DIRECTIONS_CARDINAL,
        lambda p, n: matrix_get(topographic_map, p) + 1 == matrix_get(topographic_map, n),
    )
    nines = [coord for coord in set(paths) if matrix_get(topographic_map, coord) == 9]
    return len(nines)


def find_trailheads(topographic_map):
    return find_all(topographic_map, 0)


def is_valid_step(grid, current_coord, next_coord):
    return matrix_get(grid, next_coord) == matrix_get(grid, current_coord) + 1


def is_end_of_path(grid, coord):
    return matrix_get(grid, coord) == 9


def find_path_count(matrix, start):
    return len(
        find_paths_rec(
            matrix,
            start,
            [start],
            is_valid_step,
            is_end_of_path,
            Coord.DIRECTIONS_CARDINAL,
            dict(),
        )
    )


def answer(file, path_function):
    topographic_map = parse(file)
    return sum(
        [path_function(topographic_map, th) for th in find_trailheads(topographic_map)]
    )


def part1(file):
    return answer(file, find_reachable_nines)


def part2(file):
    return answer(file, find_path_count)


# =============================================================================
if __name__ == "__main__":
    run(
        part1,
        [
            TestCase("10_example1", 1),
            TestCase("10_example2", 2),
            TestCase("10_example3", 4),
            TestCase("10_example4", 3),
            TestCase("10_example5", 36),
            TestCase("10_puzzle_input", 674),
        ],
    )

    run(
        part2,
        [
            TestCase("10_example_6", 3),
            TestCase("10_example_7", 13),
            TestCase("10_example_8", 227),
            TestCase("10_example_9", 81),
            TestCase("10_puzzle_input", 1372),
        ],
    )
