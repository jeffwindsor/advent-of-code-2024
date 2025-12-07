from aoc import Input, run, TestCase, Coord

# Constants
ROBOT = "@"
SPACE = "."
WALL = "#"
BOX = "O"
BOX_LEFT = "["
BOX_RIGHT = "]"

DIRECTIONS = {
    "^": Coord.UP,
    "v": Coord.DOWN,
    "<": Coord.LEFT,
    ">": Coord.RIGHT
}


def parse_file(data_file):
    warehouse_map, move_lines = Input(data_file).content.split("\n\n")
    grid = [list(row) for row in warehouse_map.splitlines()]
    commands = "".join(move_lines.splitlines())
    return grid, commands


def find_robot(grid):
    """Locate the robot's position in the grid."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ROBOT:
                return r, c
    return None


def moveable_boxes(grid, dr, dc, r, c):
    """Check how many boxes can be pushed in a direction.
    Returns (can_move, box_count)."""
    boxes = 0
    nr, nc = r + dr, c + dc

    while grid[nr][nc] == BOX:
        nr += dr
        nc += dc
        boxes += 1

    return (grid[nr][nc] == SPACE), boxes


def simulate_moves(grid, commands):
    """Simulate the robot's movements and box pushes for part 1."""
    robot_pos = find_robot(grid)

    for command in commands:
        direction = DIRECTIONS[command]
        dr, dc = direction.row, direction.col
        r, c = robot_pos

        moveable, boxes = moveable_boxes(grid, dr, dc, r, c)
        if moveable:
            nr, nc = r + dr, c + dc
            grid[r][c] = SPACE
            grid[nr][nc], robot_pos = ROBOT, (nr, nc)
            if boxes > 0:
                grid[nr + (dr * boxes)][nc + (dc * boxes)] = BOX

    return grid


def calculate_gps_sum(grid):
    """Calculate the sum of GPS coordinates for all boxes."""
    total_gps = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == BOX:
                total_gps += 100 * r + c
    return total_gps


def part1(filepath):
    final_grid = simulate_moves(*parse_file(filepath))
    return calculate_gps_sum(final_grid)


# ============================================================
# Part 2 - Wide warehouse with 2-unit boxes
# ============================================================


def scale_warehouse(grid):
    """Scale warehouse to be twice as wide.
    # → ##, O → [], . → .., @ → @."""
    scaling = {
        WALL: [WALL, WALL],
        BOX: [BOX_LEFT, BOX_RIGHT],
        SPACE: [SPACE, SPACE],
        ROBOT: [ROBOT, SPACE],
    }
    return [[char for cell in row for char in scaling[cell]] for row in grid]


def find_boxes_to_push_vertical(grid, r, c, dr):
    """Find all boxes that need to be pushed for a vertical move.

    Uses layer-by-layer propagation to handle cascading pushes where one box
    pushes multiple boxes above/below it.

    Returns None if blocked by wall, otherwise set of box positions (left edges).
    """
    all_boxes = set()
    current_layer = set()

    # Check what's directly in front of the starting position
    next_r = r + dr
    cell = grid[next_r][c]

    if cell == WALL:
        return None
    if cell == SPACE:
        return set()

    # Found a box - identify its left edge position
    if cell == BOX_LEFT:
        current_layer.add((next_r, c))
    elif cell == BOX_RIGHT:
        current_layer.add((next_r, c - 1))

    # Process boxes layer by layer to find all boxes in the cascade
    while current_layer:
        next_layer = set()

        for box_r, box_c in current_layer:
            if (box_r, box_c) in all_boxes:
                continue
            all_boxes.add((box_r, box_c))

            # Check what's in front of BOTH parts of this box ([ and ])
            for col_offset in [0, 1]:
                check_r = box_r + dr
                check_c = box_c + col_offset
                check_cell = grid[check_r][check_c]

                if check_cell == WALL:
                    return None  # Blocked
                elif check_cell == BOX_LEFT:
                    next_layer.add((check_r, check_c))
                elif check_cell == BOX_RIGHT:
                    next_layer.add((check_r, check_c - 1))

        current_layer = next_layer

    return all_boxes


def move_boxes_vertical(grid, boxes, dr):
    """Move all boxes vertically.

    Boxes is a set of (r, c) positions representing left edges.
    Sort by row to move furthest boxes first, avoiding overwrites.
    """
    sorted_boxes = sorted(boxes, key=lambda b: b[0], reverse=(dr > 0))

    for r, c in sorted_boxes:
        grid[r + dr][c] = BOX_LEFT
        grid[r + dr][c + 1] = BOX_RIGHT
        grid[r][c] = SPACE
        grid[r][c + 1] = SPACE


def can_push_horizontal(grid, r, c, dc):
    """Check if horizontal push is possible."""
    col = c + dc
    while grid[r][col] in [BOX_LEFT, BOX_RIGHT]:
        col += dc
    return grid[r][col] == SPACE


def push_horizontal(grid, r, c, dc):
    """Push boxes horizontally by shifting the entire sequence.

    Find empty space, then shift everything (robot + boxes) into it.
    """
    # Find the empty space at the end of the box chain
    col = c + dc
    while grid[r][col] in [BOX_LEFT, BOX_RIGHT]:
        col += dc

    # Shift the entire sequence by copying from empty space toward robot
    if dc > 0:  # Moving right
        for pos in range(col, c, -1):
            grid[r][pos] = grid[r][pos - 1]
    else:  # Moving left
        for pos in range(col, c):
            grid[r][pos] = grid[r][pos + 1]

    grid[r][c] = SPACE


def simulate_moves_wide(grid, commands):
    """Simulate robot movements in wide warehouse with 2-unit boxes."""
    robot_pos = find_robot(grid)

    for command in commands:
        direction = DIRECTIONS[command]
        dr, dc = direction.row, direction.col
        r, c = robot_pos
        nr, nc = r + dr, c + dc
        next_cell = grid[nr][nc]

        if next_cell == WALL:
            continue
        elif next_cell == SPACE:
            grid[r][c] = SPACE
            grid[nr][nc] = ROBOT
            robot_pos = (nr, nc)
        elif next_cell in [BOX_LEFT, BOX_RIGHT]:
            if dr != 0:  # Vertical movement
                boxes = find_boxes_to_push_vertical(grid, r, c, dr)
                if boxes is not None:
                    move_boxes_vertical(grid, boxes, dr)
                    grid[r][c] = SPACE
                    grid[nr][nc] = ROBOT
                    robot_pos = (nr, nc)
            else:  # Horizontal movement
                if can_push_horizontal(grid, r, c, dc):
                    push_horizontal(grid, r, c, dc)
                    robot_pos = (nr, nc)

    return grid


def calculate_gps_sum_wide(grid):
    """Calculate GPS sum for wide boxes (using left edge [)"""
    total_gps = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == BOX_LEFT:
                total_gps += 100 * r + c
    return total_gps


def part2(filepath):
    grid, commands = parse_file(filepath)
    wide_grid = scale_warehouse(grid)
    final_grid = simulate_moves_wide(wide_grid, commands)
    return calculate_gps_sum_wide(final_grid)


if __name__ == "__main__":
    run(part1, [
        TestCase("./data/15_small_example", 2028),
        TestCase("./data/15_example", 10092),
        TestCase("./data/15_puzzle_input", 1465523),
    ])

    run(part2, [
        TestCase("./data/15_example", 9021),
        TestCase("./data/15_puzzle_input", 1471049),
    ])
