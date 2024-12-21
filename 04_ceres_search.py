import utils.runners as R
import utils.files as F
import utils.matrix_2d as M2

DAY = 4
VALID_X_MAS = {"MSMS", "MMSS", "SSMM", "SMSM"}


def is_valid_position(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def search_word(word, grid):
    return sum(
        search_word_in_direction(grid, r, c, word, dr, dc)
        for r, row in enumerate(grid)
        for c, cell in enumerate(row)
        for dr, dc in M2.DIRECTIONS_ALL
    )


def search_word_in_direction(grid, r, c, word, dr, dc):
    for i, char in enumerate(word):
        new_row, new_col = r + i * dr, c + i * dc
        if (
            not is_valid_position(grid, new_row, new_col)
            or grid[new_row][new_col] != char
        ):
            return False
    return True


def search_x_mas(grid):
    return sum(
        is_valid_x_mas(grid, r, c)
        for r in range(1, len(grid) - 1)
        for c in range(1, len(grid[0]) - 1)
    )


def is_valid_x_mas(grid, r, c):
    if grid[r][c] != "A":
        return False
    corners = [
        grid[r - 1][c - 1],  # up-left
        grid[r - 1][c + 1],  # up-right
        grid[r + 1][c - 1],  # down-left
        grid[r + 1][c + 1],  # down-right
    ]
    return "".join(corners) in VALID_X_MAS


def part1(file):
    grid = F.read_data_as_lines(DAY, file)
    return search_word("XMAS", grid)


def part2(file):
    grid = F.read_data_as_lines(DAY, file)
    return search_x_mas(grid)


if __name__ == "__main__":
    R.run(part1, [("example1.1", 4), ("example1.2", 18), ("puzzle_input", 2662)])
    R.run(part2, [("example2.1", 1), ("example2.2", 9), ("puzzle_input", 2034)])
