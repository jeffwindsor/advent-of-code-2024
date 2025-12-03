from aoc import read_data_as_sections, run, TestCase

# Puzzle constants
LOCK_TOP_ROW = "#####"
KEY_BOTTOM_ROW = "#####"
AVAILABLE_HEIGHT = 5  # Total rows (7) minus top and bottom rows


def parse_schematic(schematic):
    """
    Parse a lock or key schematic into heights.

    Returns:
        tuple: (is_lock: bool, heights: list[int])
    """
    lines = schematic.strip().split("\n")

    # Determine if lock (top filled) or key (bottom filled)
    is_lock = lines[0] == LOCK_TOP_ROW

    # Calculate heights for each column
    num_cols = len(lines[0])
    heights = []

    for col in range(num_cols):
        # Count # symbols in this column, excluding the always-filled row
        if is_lock:
            # For locks, count from row 1 onwards (skip top row)
            count = sum(1 for row in range(1, len(lines)) if lines[row][col] == "#")
        else:
            # For keys, count up to second-to-last row (skip bottom row)
            count = sum(1 for row in range(len(lines) - 1) if lines[row][col] == "#")

        heights.append(count)

    return is_lock, heights


def fits(lock_heights, key_heights):
    """Check if a key fits a lock without overlapping."""
    return all(
        lock_h + key_h <= AVAILABLE_HEIGHT
        for lock_h, key_h in zip(lock_heights, key_heights)
    )


def parse_data(data_file):
    """Parse the input data into locks and keys."""
    sections = read_data_as_sections(data_file)

    locks = []
    keys = []

    for section in sections:
        is_lock, heights = parse_schematic(section)
        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)

    return locks, keys


def count_fitting_pairs_part1(data_file):
    """Count unique lock/key pairs that fit together without overlapping."""
    locks, keys = parse_data(data_file)

    count = 0
    for lock in locks:
        for key in keys:
            if fits(lock, key):
                count += 1

    return count


if __name__ == "__main__":
    run(
        count_fitting_pairs_part1,
        [
            TestCase("25_example", 3),
            TestCase("25_puzzle_input", 3439),
        ],
    )
