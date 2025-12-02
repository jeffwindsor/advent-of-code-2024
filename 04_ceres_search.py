from aoc import (
    read_data_as_lines,
    run,
    TestCase,
    Coord,
    search_in_direction,
)


def parse(data_file):
    return read_data_as_lines(data_file)


def search_word(word, matrix):
    return sum(
        search_in_direction(matrix, Coord(r, c), direction, word)
        for r, row in enumerate(matrix)
        for c, cell in enumerate(row)
        for direction in Coord.DIRECTIONS_ALL
    )


def is_valid_x_mas(matrix, r, c):
    if matrix[r][c] != "A":
        return False
    corners = map(lambda cc: matrix[r + cc.row][c + cc.col], Coord.DIRECTIONS_INTERCARDINAL)
    return "".join(corners) in {"MSMS", "MMSS", "SSMM", "SMSM"}


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
    run(part1, [
        TestCase("04_example1.1", 4),
        TestCase("04_example1.2", 18),
        TestCase("04_puzzle_input", 2662),
    ])
    run(part2, [
        TestCase("04_example2.1", 1),
        TestCase("04_example2.2", 9),
        TestCase("04_puzzle_input", 2034),
    ])
