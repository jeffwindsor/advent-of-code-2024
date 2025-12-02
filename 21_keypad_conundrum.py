from aoc import read_data_as_lines, run, TestCase, Coord
from itertools import product
from collections import deque


def find_all_shortest_paths(matrix, start, end):
    """
    Find all shortest paths in a 2D matrix from start to end, avoiding cells with the value None.

    Args:
        matrix (list of list): The 2D grid where obstacles are represented by `None`.
        start (tuple): The starting cell as (row, col).
        end (tuple): The target cell as (row, col).
        avoid_value: The value in the matrix cells to avoid. Default is None.

    Returns:
        list of list of tuple: All shortest paths as lists of cells (row, col).
    """
    rows, cols = len(matrix), len(matrix[0])
    queue = deque([(start, [start])])  # Queue stores (current_cell, path_so_far)
    shortest_paths = []
    shortest_path_length = float("inf")  # To track the shortest path length

    while queue:
        cell, path = queue.popleft()

        # Stop if the current path exceeds the known shortest path length
        if len(path) > shortest_path_length:
            continue

        # Check if we reached the destination
        if cell == end:
            if len(path) < shortest_path_length:
                shortest_paths = [path]
                shortest_path_length = len(path)
            elif len(path) == shortest_path_length:
                shortest_paths.append(path)
            continue

        # Explore neighbors
        for direction in Coord.DIRECTIONS_CARDINAL:
            new_row, new_col = cell[0] + direction.row, cell[1] + direction.col
            new_cell = (new_row, new_col)

            if (
                0 <= new_row < rows
                and 0 <= new_col < cols
                and matrix[new_row][new_col] is not None
                and new_cell not in path
            ):
                queue.append((new_cell, path + [new_cell]))

    return shortest_paths


def sub_coord(a, b):
    return Coord(a[0] - b[0], a[1] - b[1])


def flatten(xss):
    return sum(xss, [])


#      number pad
#     +---+---+---+
#     | 7 | 8 | 9 |
#     +---+---+---+
#     | 4 | 5 | 6 |
#     +---+---+---+
#     | 1 | 2 | 3 |
#     +---+---+---+
#         | 0 | A |
#         +---+---+

num_pad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]
nums = [n for n in flatten(num_pad) if n is not None]
num_coords = {key: (r, c) for r, row in enumerate(num_pad) for c, key in enumerate(row)}

# direction pad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

dir_pad = [[None, "^", "A"], ["<", "v", ">"]]
dirs = [d for d in flatten(dir_pad) if d is not None]
dir_coords = {key: (r, c) for r, row in enumerate(dir_pad) for c, key in enumerate(row)}
diff_coord_dirs = {
    Coord(0, -1): "<",
    Coord(0, 1): ">",
    Coord(-1, 0): "^",
    Coord(1, 0): "v"
}


def to_direction_seq(coord_path):
    steps = zip(coord_path, coord_path[1:])
    dir_seq = [diff_coord_dirs.get(sub_coord(end, start)) for start, end in steps]
    # concatenate, add an A for pressing the button
    return "".join(dir_seq) + "A"


def shortest_path(pad, pad_coords, start, end):
    sc, ec = pad_coords.get(start), pad_coords.get(end)
    return [
        to_direction_seq(coord_path)
        for coord_path in find_all_shortest_paths(pad, sc, ec)
    ]


#
#     SHIP
#  ||======================================================================================||
#  || ME      || -40                || RADIATION         || DEPRESSURIZED    || ????       ||
#  || dpad-40 || robot-40 -> dpad-r || robot-r -> dpad-d ||robot-d -> npad-h ||historian   ||
#  ||======================================================================================||
#
#  start at [A] on d-pad
#  start at [A] on n-pad
#
#  d-pad [A] = robot move forward, pushing n-pad button
#  n-pad [A] = activate TODO
#


NUMBER_PAD = {p: shortest_path(num_pad, num_coords, *p) for p in product(nums, nums)}
DIRECTION_PAD = {p: shortest_path(dir_pad, dir_coords, *p) for p in product(dirs, dirs)}


def generate_combinations(list_of_lists):
    # Generate all combinations respecting the order of the sublists
    combinations = product(*list_of_lists)
    # Ensure strings are concatenated properly
    return ["".join(combination) for combination in combinations]


def find_shortest(strings):
    if not strings:
        return []
    min_length = min(len(s) for s in strings)
    return [s for s in strings if len(s) == min_length]


def flatten(nested_list):
    # Check if the input is a list of lists
    if not isinstance(nested_list, list) or not all(
        isinstance(sublist, list) for sublist in nested_list
    ):
        return nested_list

    return sum(nested_list, [])


def robot_moves(pad, button_pushes):
    options = []
    current_button = "A"
    for push_button in button_pushes:
        # append movements from button to button then A for press
        paths = pad[(current_button, push_button)]
        options.append(paths)
        current_button = push_button
    # print("  options", options)
    results = generate_combinations(options)
    return list(results)


def shortest_robot_moves(pad, sequences):
    return find_shortest(flatten([robot_moves(pad, s) for s in sequences]))


def find_min_length(from_button, to_button, depth, memo):
    """
    Find the minimum sequence length needed to move from from_button to to_button
    at the given depth.

    depth = 0: Base case - direct button presses (I'm at my directional pad)
    depth > 0: Recursive case - need to control robots at lower depths

    Uses memoization to avoid recalculating the same states.
    """
    # Memoization key
    key = (from_button, to_button, depth)
    if key in memo:
        return memo[key]

    # Base case: depth == 0 means I'm directly pressing buttons
    # The cost is just the number of moves in the path
    if depth == 0:
        # Direct path on direction pad
        paths = DIRECTION_PAD[(from_button, to_button)]
        result = min(len(path) for path in paths)
        memo[key] = result
        return result

    # Recursive case: need to control a robot at depth-1
    # Get all possible paths on the direction pad
    paths = DIRECTION_PAD[(from_button, to_button)]

    min_total = float('inf')

    # Try each possible path and find which one results in the shortest sequence
    for path in paths:
        # For this path, calculate the total length by summing the costs
        # of each button press at the next level up
        current_total = 0
        current_pos = "A"  # Robot starts at A

        for next_button in path:
            # Recursively find the cost to move from current_pos to next_button
            # at depth - 1
            current_total += find_min_length(current_pos, next_button, depth - 1, memo)
            current_pos = next_button

        min_total = min(min_total, current_total)

    memo[key] = min_total
    return min_total


def solve(data_file, num_directional_robots):
    """
    Solve the keypad problem with a given number of directional robots.

    Args:
        data_file: Input file with door codes
        num_directional_robots: Number of directional keypads (2 for part1, 25 for part2)
    """
    result = []
    memo = {}

    for button_seq in read_data_as_lines(data_file):
        # Calculate the minimum length needed to type this sequence
        total_length = 0
        current_button = "A"  # Robot at numeric keypad starts at A

        for target_button in button_seq:
            # Get the paths on the numeric keypad for this transition
            paths = NUMBER_PAD[(current_button, target_button)]

            min_path_length = float('inf')
            for path in paths:
                # For each possible path on the numeric keypad,
                # calculate the cost through all directional robots
                path_length = 0
                pos = "A"  # All directional robots start at A
                for button in path:
                    # Cost to type this button through num_directional_robots robots
                    path_length += find_min_length(pos, button, num_directional_robots, memo)
                    pos = button
                min_path_length = min(min_path_length, path_length)

            total_length += min_path_length
            current_button = target_button

        button_seq_as_num = int(button_seq[:-1])
        result.append(button_seq_as_num * total_length)

    return sum(result)


def part1(data_file):
    # 2 directional robots means depth 1 (0-indexed: robot1, robot2)
    # Actually, let me verify with the original logic
    return solve(data_file, 1)


def part2(data_file):
    return solve(data_file, 24)


#      number pad           direction pad
#     +---+---+---+            +---+---+
#     | 7 | 8 | 9 |            | ^ | A |
#     +---+---+---+        +---+---+---+
#     | 4 | 5 | 6 |        | < | v | > |
#     +---+---+---+        +---+---+---+
#     | 1 | 2 | 3 |
#     +---+---+---+
#         | 0 | A |
#         +---+---+

if __name__ == "__main__":
    # print(generate_combinations([["<"], ["^"], ["^^>", "^>^", ">^^"], ["vvv"]]))
    run(
        part1,
        [
            TestCase("21_pre_example", 1972),
            # TestCase("21_pre_example2", 2660),
            TestCase("21_example", 126384),
            TestCase("21_puzzle_input", 278748),
        ],
    )

    run(
        part2,
        [
            TestCase("21_example", 154115708116294),
            TestCase("21_puzzle_input", 337744744231414),
        ],
    )
