from parser import parse_file

#     Simulate Movements:
#         Determine the robot's initial position (@).
#         For each command:
#             Compute the intended new position of the robot.
#             Check the tile at the intended position:
#                 If it's a wall (#), do nothing.
#                 If it's empty (.), move the robot.
#                 If it's a box (O), check if the box can be pushed. If the push is valid (the next tile in the direction is empty), move the robot and the box. Otherwise, do nothing.
#         Update the grid as moves are executed.
#
#     Calculate GPS Coordinates:
#         For each box (O) in the final grid:
#             Compute its GPS coordinate using the formula:
#             GPS = 100 * row_index + column_index.
#         Sum all the GPS coordinates.
#
#     Output the Result:
#         Return the total sum of the GPS coordinates.
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
    print_grid(final_grid)
    return calculate_gps_sum(final_grid)


if __name__ == "__main__":
    print(f"1: small example (Expected 2028, Actual {part1('small_example')})")
    print(f"1: example (Expected 10092, Actual {part1('example')})")
    print(f"1: puzzle_input (Expected 1465523, Actual {part1('puzzle_input')})")
