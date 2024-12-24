from collections import deque

# Define the keypad grid with coordinates
num_keypad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "3": (2, 0),
    "2": (2, 1),
    "1": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
dir_keypad = {"^": (1, 1), "<": (0, 0), "v": (0, 1), ">": (0, 2), "A": (1, 2)}

# Define valid moves
moves = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


# Check if a position is valid
def is_valid(keypad, pos):
    return pos in keypad.values()


# BFS to find the shortest path between two buttons
def find_shortest_path(keypad, start, end):
    start_pos, end_pos = keypad[start], keypad[end]
    queue = deque([(start_pos, [])])  # (current_position, path_taken)
    visited = set()

    while queue:
        current_pos, path = queue.popleft()
        if current_pos == end_pos:
            return path

        if current_pos in visited:
            continue
        visited.add(current_pos)

        for move, (dx, dy) in moves.items():
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if is_valid(keypad, new_pos) and new_pos not in visited:
                queue.append((new_pos, path + [move]))
    return []


def button_moves(keypad):
    # Generate all shortest paths for button pairs
    button_pairs = [(a, b) for a in keypad for b in keypad if a != b]
    return {
        pair: "".join(find_shortest_path(keypad, pair[0], pair[1]))
        for pair in button_pairs
    }


if __name__ == "__main__":
    print(f"NPAD_MOVES = {button_moves(num_keypad)}")
    print(f"DPAD_MOVES = {button_moves(dir_keypad)}")
