from .coordinates import is_within_bounds_inclusive, add
from collections import deque


def size(matrix):
    return (len(matrix), len(matrix[0]))


def higher_bounds(matrix):
    r, c = size(matrix)
    return (r - 1, c - 1)


def is_within_bounds(matrix, coord):
    return is_within_bounds_inclusive(coord, higher_bounds(matrix), (0, 0))


def get_value(matrix, coord):
    return matrix[coord[0]][coord[1]]


def find_first(matrix, value):
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == value:
                return r, c
    return None


def find_all(matrix, value):
    return [
        (r, c)
        for r, row in enumerate(matrix)
        for c, cell in enumerate(row)
        if cell == value
    ]


def always_true(coord):
    return True


def bfs(matrix, start, directions, can_visit):
    """
    Perform BFS on a 2D matrix.

    :param matrix: 2D list representing the matrix
    :param start: Tuple (x, y) representing the starting position
    :param directions: list of coordinate offsets for each possible direction
    :return: List of visited positions in BFS order
    """
    hb = higher_bounds(matrix)
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
                is_within_bounds_inclusive((nx, ny), hb)
                and (nx, ny) not in visited
                and can_visit((x, y), (nx, ny))
            ):
                visited.add((nx, ny))
                queue.append((nx, ny))

    return order


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
        next = add(start, direction)
        if is_within_bounds(matrix, next) and is_valid_step(matrix, start, next):
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


def flood_fill(matrix, x, y, new_value):
    """
    Perform a flood fill on an matrix starting at (x, y) replacing the target value with new_value.

    :param matrix: 2D list representing the matrix
    :param x: X-coordinate (row index) to start the flood fill
    :param y: Y-coordinate (column index) to start the flood fill
    :param new_value: value to fill the region with
    :return: Modified matrix
    """
    # Get dimensions of the image
    rows, cols = len(matrix), len(matrix[0])

    # The color to be replaced
    target_color = matrix[x][y]

    # If the target color is the same as the new color, return early
    if target_color == new_value:
        return matrix

    # Initialize a queue for BFS
    queue = deque([(x, y)])

    while queue:
        cx, cy = queue.popleft()

        # Check bounds and if the current cell matches the target color
        if 0 <= cx < rows and 0 <= cy < cols and matrix[cx][cy] == target_color:
            # Replace the color
            matrix[cx][cy] = new_value

            # Add neighboring cells to the queue
            queue.append((cx + 1, cy))  # Down
            queue.append((cx - 1, cy))  # Up
            queue.append((cx, cy + 1))  # Right
            queue.append((cx, cy - 1))  # Left

    return matrix
