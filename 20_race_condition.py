from aoc import Input, run, TestCase, Coord, Grid, dfs_grid_path

WALL = "#"
SPACE = "."
START = "S"
END = "E"


def parse(data_file):
    return Input(data_file).as_grid()


def analyze_maze(maze, start, end):
    path = dfs_grid_path(maze, start, end, {SPACE, END})
    if not path:
        raise ValueError("No valid path between start and end in the original maze.")
    path_index_by_coord = {coord: i for i, coord in enumerate(path)}
    savings_count = {}
    for current_index, current_coord in enumerate(path):
        # look in cardinal directions for walls
        for direction in Coord.DIRECTIONS_CARDINAL:
            check_for_wall = current_coord + direction
            if check_for_wall in maze and maze[check_for_wall] == WALL:
                # then one more in same direction for non wall
                check_for_space = check_for_wall + direction
                if check_for_space in maze and maze[check_for_space] != WALL:
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
    Optimized to calculate distance directly and skip impossible cheats early.
    """
    path = dfs_grid_path(maze, start, end, {SPACE, END})
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
                # Calculate manhattan distance directly from drow/dcol
                cheat_duration = abs(drow) + abs(dcol)

                # Skip if no movement or exceeds max duration
                if cheat_duration == 0 or cheat_duration > max_cheat_duration:
                    continue

                cheat_end = Coord.from_rc(current_coord.row + drow, current_coord.col + dcol)

                # Check if cheat end is on the path
                if cheat_end in path_index_by_coord:
                    end_index = path_index_by_coord[cheat_end]

                    # Calculate time saved: path distance - cheat duration
                    path_distance = end_index - current_index
                    time_saved = path_distance - cheat_duration

                    # Only count if we actually save time (and move forward)
                    if time_saved > 0:
                        savings_count[time_saved] = savings_count.get(time_saved, 0) + 1

    return savings_count


def part1(file):
    maze = parse(file)
    start, end = maze.find_first(START), maze.find_first(END)
    savings_count = analyze_maze(maze, start, end)

    # print("  Savings breakdown:")
    # for saving, count in sorted(savings_count.items()):
    #     print(f"    {saving} spaces: {count}")

    return sum(count for saving, count in savings_count.items() if saving > 100)


def part2(file):
    maze = parse(file)
    start, end = maze.find_first(START), maze.find_first(END)
    savings_count = analyze_maze_with_longer_cheats(maze, start, end, 20)

    # print("  Savings breakdown (20ps cheats):")
    # for saving, count in sorted(savings_count.items()):
    #     if saving >= 50:
    #         print(f"    {saving} spaces: {count}")

    return sum(count for saving, count in savings_count.items() if saving >= 100)


if __name__ == "__main__":
    run(part1, [
        TestCase("data/20_example", 0),
        TestCase("data/20_puzzle_input", 1321),
    ])

    run(part2, [
        TestCase("data/20_example", 0),  # 0 cheats save >= 100ps in example
        TestCase("data/20_puzzle_input", 971737),
    ])
