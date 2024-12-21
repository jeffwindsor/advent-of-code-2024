from utils.runners import run
from utils.files import read_data_as_lines
from utils.matrix_2d import higher_bounds
from utils.matrix_2d.coordinates import (
    is_within_bounds,
    DIRECTIONS_ALL,
    DIRECTIONS_INTERCARDINAL,
)

VALID_X_MAS = {"MSMS", "MMSS", "SSMM", "SMSM"}


def parse(file):
    return read_data_as_lines(4, file)


def search_word_in_direction(word, matrix, r, c, dr, dc):
    hb = higher_bounds(matrix)
    for i, char in enumerate(word):
        new_row, new_col = r + i * dr, c + i * dc
        if (
            not is_within_bounds((new_row, new_col), hb)
            or matrix[new_row][new_col] != char
        ):
            return False
    return True


def search_word(word, matrix):
    return sum(
        search_word_in_direction(word, matrix, r, c, dr, dc)
        for r, row in enumerate(matrix)
        for c, cell in enumerate(row)
        for dr, dc in DIRECTIONS_ALL
    )


def is_valid_x_mas(matrix, r, c):
    if matrix[r][c] != "A":
        return False
    corners = map(lambda cc: matrix[r + cc[0]][c + cc[1]], DIRECTIONS_INTERCARDINAL)
    return "".join(corners) in VALID_X_MAS


def search_x_mas(matrix):
    return sum(
        is_valid_x_mas(matrix, r, c)
        for r in range(1, len(matrix) - 1)
        for c in range(1, len(matrix[0]) - 1)
    )


def part1(file):
    return search_word("XMAS", parse(file))


def part2(file):
    return search_x_mas(parse(file))


if __name__ == "__main__":
    run(part1, [("example1.1", 4), ("example1.2", 18), ("puzzle_input", 2662)])
    run(part2, [("example2.1", 1), ("example2.2", 9), ("puzzle_input", 2034)])
