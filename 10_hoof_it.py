from utils.matrix_2d import bfs, get_value, find_all, find_paths_rec
from utils.matrix_2d.coordinates import DIRECTIONS_CARDINAL
from utils.files import read_data_as_lines
from utils.runners import run


def parse(file):
    # problem wants to follow path of increasing values from 0, so EMPTY = -1
    return [
        list(map(lambda x: int(x) if x.isdigit() else -1, line))
        for line in read_data_as_lines(10, file)
    ]


def find_reachable_nines(topographic_map, start_coord):
    paths = bfs(
        topographic_map,
        start_coord,
        DIRECTIONS_CARDINAL,
        lambda p, n: get_value(topographic_map, p) + 1 == get_value(topographic_map, n),
    )
    nines = [coord for coord in set(paths) if get_value(topographic_map, coord) == 9]
    return len(nines)


def find_trailheads(topographic_map):
    return find_all(topographic_map, 0)


def is_valid_step(grid, current_coord, next_coord):
    return get_value(grid, next_coord) == get_value(grid, current_coord) + 1


def is_end_of_path(grid, coord):
    return get_value(grid, coord) == 9


def find_path_count(matrix, start):
    return len(
        find_paths_rec(
            matrix,
            start,
            [start],
            is_valid_step,
            is_end_of_path,
            DIRECTIONS_CARDINAL,
            dict(),
        )
    )


def answer(file, path_function):
    topographic_map = parse(file)
    return sum(
        [path_function(topographic_map, th) for th in find_trailheads(topographic_map)]
    )


def part1(file):
    return answer(file, find_reachable_nines)


def part2(file):
    return answer(file, find_path_count)


# =============================================================================
if __name__ == "__main__":
    run(
        part1,
        [
            ("example1", 1),
            ("example2", 2),
            ("example3", 4),
            ("example4", 3),
            ("example5", 36),
            ("puzzle_input", 674),
        ],
    )

    run(
        part2,
        [
            ("example_6", 3),
            ("example_7", 13),
            ("example_8", 227),
            ("example_9", 81),
            ("puzzle_input", 1372),
        ],
    )
