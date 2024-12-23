from utils.files import read_data
from utils.runners import run


def parse_file(filepath):
    warehouse_map, move_lines = read_data(15, filepath).split("\n\n")
    grid = [list(row) for row in warehouse_map.splitlines()]
    commands = "".join(move_lines.splitlines())
    return grid, commands


ROBOT = "@"
SPACE = "."
WALL = "#"
BOX = "O"


def print_grid(g):
    for row in g:
        print("".join(row))
    print()


def print_move(m):
    print(f"Move {m}:")


def find_robot(grid):
    """
    Locate the robot's position in the grid.
    """
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ROBOT:
                return r, c
    return None


def moveable_boxes(grid, dr, dc, r, c):
    boxes = 0
    nr, nc = r + dr, c + dc

    while grid[nr][nc] == BOX:
        nr += dr
        nc += dc
        boxes += 1

    return (grid[nr][nc] == SPACE), boxes


def simulate_moves(grid, commands):
    """
    Simulate the robot's movements and box pushes.
    """
    directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    robot_pos = find_robot(grid)

    for command in commands:
        dr, dc = directions[command]
        r, c = robot_pos

        # print_grid(grid)
        # print_move(command)

        moveable, boxes = moveable_boxes(grid, dr, dc, r, c)
        # print(moveable, boxes)
        if moveable:
            nr, nc = r + dr, c + dc
            grid[r][c] = SPACE
            grid[nr][nc], robot_pos = ROBOT, (nr, nc)
            if boxes > 0:
                grid[nr + (dr * boxes)][nc + (dc * boxes)] = BOX

    return grid


def calculate_gps_sum(grid):
    """
    Calculate the sum of GPS coordinates for all boxes.
    """
    total_gps = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "O":
                total_gps += 100 * r + c
    return total_gps


def part1(filepath):
    final_grid = simulate_moves(*parse_file(filepath))
    return calculate_gps_sum(final_grid)


if __name__ == "__main__":
    run(part1, [("small_example", 2028), ("example", 10092), ("puzzle_input", 1465523)])
