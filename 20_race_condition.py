from aoc import (
    read_data_as_lines,
    run,
    TestCase,
    Coord,
    matrix_contains_coord,
    matrix_get,
    find_first,
    matrix_size,
)

WALL = "#"
SPACE = "."
START = "S"
END = "E"


def parse(data_file):
    return [list(row) for row in read_data_as_lines(data_file)]


def dfs(maze, start, end):
    stack = [
        (start, [])
    ]  # Stack contains tuples of (current_position, path_to_position)
    visited = set()

    while stack:
        current, path = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        path = path + [current]  # Update the path to include the current position

        if current == end:
            return path  # Return the path when the end is reached

        for direction in Coord.DIRECTIONS_CARDINAL:
            next_position = current + direction
            if (
                matrix_contains_coord(maze, next_position)
                and next_position not in visited
                and matrix_get(maze, next_position) in (SPACE, END)
            ):
                stack.append((next_position, path))

    return []  # Return an empty list if no path is found


def analyze_maze(maze, start, end):
    path = dfs(maze, start, end)
    if not path:
        raise ValueError("No valid path between start and end in the original maze.")
    path_index_by_coord = {coord: i for i, coord in enumerate(path)}
    savings_count = {}
    for current_index, current_coord in enumerate(path):
        # look in cardinal directions for walls
        for direction in Coord.DIRECTIONS_CARDINAL:
            check_for_wall = current_coord + direction
            if (
                matrix_contains_coord(maze, check_for_wall)
                and matrix_get(maze, check_for_wall) == WALL
            ):
                # then one more in same direction for non wall
                check_for_space = check_for_wall + direction
                if (
                    matrix_contains_coord(maze, check_for_space)
                    and matrix_get(maze, check_for_space) != WALL
                ):
                    space_index = path_index_by_coord[check_for_space]
                    savings_index = space_index - current_index
                    if savings_index > 0:
                        # check index existence
                        if savings_index not in savings_count:
                            savings_count[savings_index] = 0
                        # increment count for savings amount
                        savings_count[savings_index] += 1

    return savings_count


def analyze_maze_with_longer_cheats(maze, start, end, max_cheat_duration):
    """
    Find cheats that can last up to max_cheat_duration picoseconds.
    A cheat is defined by its start and end positions on the path.
    The cheat duration is the Manhattan distance between start and end.
    """
    path = dfs(maze, start, end)
    if not path:
        raise ValueError("No valid path between start and end in the original maze.")

    path_index_by_coord = {coord: i for i, coord in enumerate(path)}
    savings_count = {}

    # For each position on the path
    for current_index, current_coord in enumerate(path):
        # Check all positions within Manhattan distance of max_cheat_duration
        for drow in range(-max_cheat_duration, max_cheat_duration + 1):
            remaining = max_cheat_duration - abs(drow)
            for dcol in range(-remaining, remaining + 1):
                cheat_end = Coord(current_coord.row + drow, current_coord.col + dcol)

                # Check if cheat end is on the path
                if cheat_end in path_index_by_coord:
                    end_index = path_index_by_coord[cheat_end]

                    # Calculate actual cheat duration (Manhattan distance)
                    cheat_duration = abs(drow) + abs(dcol)

                    # Calculate time saved: path distance - cheat duration
                    path_distance = end_index - current_index
                    time_saved = path_distance - cheat_duration

                    # Only count if we actually save time (and move forward)
                    if time_saved > 0:
                        if time_saved not in savings_count:
                            savings_count[time_saved] = 0
                        savings_count[time_saved] += 1

    return savings_count


def part1(file):
    maze = parse(file)
    start, end = find_first(maze, START), find_first(maze, END)
    savings_count = analyze_maze(maze, start, end)

    # print("  Savings breakdown:")
    # for saving, count in sorted(savings_count.items()):
    #     print(f"    {saving} spaces: {count}")

    return sum(count for saving, count in savings_count.items() if saving > 100)


def part2(file):
    maze = parse(file)
    start, end = find_first(maze, START), find_first(maze, END)
    savings_count = analyze_maze_with_longer_cheats(maze, start, end, 20)

    # print("  Savings breakdown (20ps cheats):")
    # for saving, count in sorted(savings_count.items()):
    #     if saving >= 50:
    #         print(f"    {saving} spaces: {count}")

    return sum(count for saving, count in savings_count.items() if saving >= 100)


if __name__ == "__main__":
    run(part1, [
        TestCase("20_example", 0),
        TestCase("20_puzzle_input", 1321),
    ])

    run(part2, [
        TestCase("20_example", 0),  # 0 cheats save >= 100ps in example
        TestCase("20_puzzle_input", 971737),
    ])
