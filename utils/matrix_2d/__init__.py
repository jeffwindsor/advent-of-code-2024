from .coordinates import is_within_bounds as c_is_within_bounds
from collections import deque


def higher_bounds(matrix):
    return (len(matrix) - 1, len(matrix[0]) - 1)


def is_within_bounds(matrix, coord):
    return c_is_within_bounds(coord, higher_bounds(matrix), (0, 0))


def find(matrix, value):
    """
    Finds the first occurrence of a value in a matrix.

    Args:
        matrix (list of list): The matrix to search.
        value: The value to find.

    Returns:
        tuple: Coordinates of the value or None.
    """
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == value:
                return r, c
    return None


def bfs(matrix, start):
    """
    Perform BFS on a 2D matrix.

    :param matrix: 2D list representing the matrix
    :param start: Tuple (x, y) representing the starting position
    :return: List of visited positions in BFS order
    """
    rows, cols = len(matrix), len(matrix[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    queue = deque([start])
    visited = set()
    visited.add(start)
    order = []

    while queue:
        x, y = queue.popleft()
        order.append((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check bounds and if the cell has not been visited
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))

    return order


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


# def simulate_matrix_movement(matrix, commands, directions):
#     """
#     Simulates movements in a matrix based on commands and directions.

#     Args:
#         matrix (list of list): The matrix to simulate on.
#         commands (list of str): Movement commands.
#         directions (dict): Mapping of commands to coordinate changes.

#     Returns:
#         list of list: Updated matrix after simulation.
#     """
#     robot_pos = find(matrix, "@")

#     for command in commands:
#         dr, dc = directions[command]
#         r, c = robot_pos
#         nr, nc = r + dr, c + dc
#         if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]) and matrix[nr][nc] == ".":
#             matrix[r][c], matrix[nr][nc] = ".", "@"
#             robot_pos = (nr, nc)
#     return matrix
