from aoc import (
    read_data_as_lines,
    run,
    DIRECTIONS_CARDINAL,
    get_value,
    find_all,
    matrix_higher_bounds,
    coord_is_within_bounds_inclusive,
    coord_add,
    coord_is_within_matrix,
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
        next = coord_add(start, direction)
        if coord_is_within_matrix(matrix, next) and is_valid_step(matrix, start, next):
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
    :param start: Tuple (x, y) representing the starting position
    :param directions: list of coordinate offsets for each possible direction
    :return: List of visited positions in BFS order
    """
    hb = matrix_higher_bounds(matrix)
    queue = deque([start])
    visited = set([start])
    order = []
    while queue:
        x, y = queue.popleft()
        order.append((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check bounds and if the cell has not been visited
            if (
                coord_is_within_bounds_inclusive((nx, ny), hb)
                and (nx, ny) not in visited
                and can_visit((x, y), (nx, ny))
            ):
                visited.add((nx, ny))
                queue.append((nx, ny))

    return order


def parse(file):
    # problem wants to follow path of increasing values from 0, so EMPTY = -1
    return [
        list(map(lambda x: int(x) if x.isdigit() else -1, line))
        for line in read_data_as_lines(10, file)
    ]


def find_reachable_nines(topographic_map, start_coord):
    paths = bfs(
        topographic_map,
        start_coord,
        DIRECTIONS_CARDINAL,
        lambda p, n: get_value(topographic_map, p) + 1 == get_value(topographic_map, n),
    )
    nines = [coord for coord in set(paths) if get_value(topographic_map, coord) == 9]
    return len(nines)


def find_trailheads(topographic_map):
    return find_all(topographic_map, 0)


def is_valid_step(grid, current_coord, next_coord):
    return get_value(grid, next_coord) == get_value(grid, current_coord) + 1


def is_end_of_path(grid, coord):
    return get_value(grid, coord) == 9


def find_path_count(matrix, start):
    return len(
        find_paths_rec(
            matrix,
            start,
            [start],
            is_valid_step,
            is_end_of_path,
            DIRECTIONS_CARDINAL,
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
            ("example1", 1),
            ("example2", 2),
            ("example3", 4),
            ("example4", 3),
            ("example5", 36),
            ("puzzle_input", 674),
        ],
    )

    run(
        part2,
        [
            ("example_6", 3),
            ("example_7", 13),
            ("example_8", 227),
            ("example_9", 81),
            ("puzzle_input", 1372),
        ],
    )
