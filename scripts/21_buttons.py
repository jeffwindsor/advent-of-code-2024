from collections import deque
from itertools import product


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
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
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
        for dr, dc in directions:
            new_row, new_col = cell[0] + dr, cell[1] + dc
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
    return (a[0] - b[0], a[1] - b[1])


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
diff_coord_dirs = {(0, -1): "<", (0, 1): ">", (-1, 0): "^", (1, 0): "v"}


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


if __name__ == "__main__":
    number_pad = {
        p: shortest_path(num_pad, num_coords, *p) for p in product(nums, nums)
    }
    direction_pad = {
        p: shortest_path(dir_pad, dir_coords, *p) for p in product(dirs, dirs)
    }

    with open("scripts/pads_for_21.py", "w") as file:
        file.write(f"NUMBER_PAD={number_pad}\n")
        file.write(f"DIRECTION_PAD={direction_pad}")
