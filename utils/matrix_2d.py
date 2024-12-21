UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP_LEFT = (-1, -1)
DOWN_LEFT = (1, -1)
UP_RIGHT = (-1, 1)
DOWN_RIGHT = (1, 1)

DIRECTIONS_CARDINAL = [UP, RIGHT, DOWN, LEFT]
DIRECTIONS_ALL = DIRECTIONS_CARDINAL + [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
TURNS_CLOCKWISE = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


def coord_add(one, two):
    return (one[0] + two[0], one[1] + two[1])


def find(grid, value):
    """
    Finds the first occurrence of a value in a grid.

    Args:
        grid (list of list): The grid to search.
        value: The value to find.

    Returns:
        tuple: Coordinates of the value or None.
    """
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == value:
                return r, c
    return None


def simulate_grid_movement(grid, commands, directions):
    """
    Simulates movements in a grid based on commands and directions.

    Args:
        grid (list of list): The grid to simulate on.
        commands (list of str): Movement commands.
        directions (dict): Mapping of commands to coordinate changes.

    Returns:
        list of list: Updated grid after simulation.
    """
    robot_pos = find(grid, "@")

    for command in commands:
        dr, dc = directions[command]
        r, c = robot_pos
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == ".":
            grid[r][c], grid[nr][nc] = ".", "@"
            robot_pos = (nr, nc)
    return grid
