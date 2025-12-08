from aoc import Input, run, TestCase, Coord, Grid


def parse(data_file):
    return Input(data_file).as_grid()


def search_word(word, grid):
    return sum(
        grid.search_in_direction(coord, direction, word)
        for coord, _ in grid.coords()
        for direction in Coord.DIRECTIONS_ALL
    )


def is_valid_x_mas(grid, coord):
    if grid[coord] != "A":
        return False
    corners = [grid[coord + cc] for cc in Coord.DIRECTIONS_INTERCARDINAL]
    return "".join(corners) in {"MSMS", "MMSS", "SSMM", "SMSM"}


def search_x_mas(grid):
    return sum(
        is_valid_x_mas(grid, coord)
        for r in range(1, grid.size.row - 1)
        for c in range(1, grid.size.col - 1)
        if (coord := Coord(r, c))
    )


def part1(file):
    return search_word("XMAS", parse(file))


def part2(file):
    return search_x_mas(parse(file))


if __name__ == "__main__":
    run(part1, [
        TestCase("./data/04_example1.1", 4),
        TestCase("./data/04_example1.2", 18),
        TestCase("./data/04_puzzle_input", 2662),
    ])
    run(part2, [
        TestCase("./data/04_example2.1", 1),
        TestCase("./data/04_example2.2", 9),
        TestCase("./data/04_puzzle_input", 2034),
    ])
