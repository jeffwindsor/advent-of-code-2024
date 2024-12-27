import os
import inspect

TITLE_COLOR = "\033[100m"
FALSE_COLOR = "\033[91m"
TRUE_COLOR = "\033[92m"
END_COLOR = "\033[0m"

ZERO = (0, 0)
UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP_LEFT = (-1, -1)
DOWN_LEFT = (1, -1)
UP_RIGHT = (-1, 1)
DOWN_RIGHT = (1, 1)

DIRECTIONS_CARDINAL = [UP, RIGHT, DOWN, LEFT]
DIRECTIONS_INTERCARDINAL = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
DIRECTIONS_ALL = DIRECTIONS_CARDINAL + DIRECTIONS_INTERCARDINAL
TURN_CLOCKWISE = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


def is_between(x, higher, lower):
    return lower <= x <= higher


def coord_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def coord_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def coord_is_within_bounds_inclusive(coord, higher_bounds, lower_bounds=ZERO):
    return is_between(coord[0], higher_bounds[0], lower_bounds[0]) and is_between(
        coord[1], higher_bounds[1], lower_bounds[1]
    )


def filter_within_bounds(coords, higher_bounds, lower_bounds=ZERO):
    return [
        c
        for c in coords
        if coord_is_within_bounds_inclusive(c, higher_bounds, lower_bounds)
    ]


def matrix_size(matrix):
    return (len(matrix), len(matrix[0]))


def matrix_higher_bounds(matrix):
    r, c = matrix_size(matrix)
    return (r - 1, c - 1)


def coord_is_within_matrix(matrix, coord):
    return coord_is_within_bounds_inclusive(coord, matrix_higher_bounds(matrix), (0, 0))


def get_value(matrix, coord):
    return matrix[coord[0]][coord[1]]


def find_first(matrix, value):
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == value:
                return r, c
    return None


def find_all(matrix, value):
    return [
        (r, c)
        for r, row in enumerate(matrix)
        for c, cell in enumerate(row)
        if cell == value
    ]


def run(func, test_cases):
    filename = os.path.basename(inspect.stack()[1].filename)

    print(f"{TITLE_COLOR}{filename}: {func.__name__}{END_COLOR}")
    for tc in test_cases:
        # default any missing execute_test to True
        input, expected, execute_test = (tc + (True,))[:3]
        if execute_test:
            actual = func(input)
            result = expected == actual
            print(
                f"  {input}: {TRUE_COLOR if result else FALSE_COLOR}{result} ",
                end="",
            )
            if result:
                print(f"{actual}{END_COLOR}")
            else:
                print(f"{expected} != {actual}{END_COLOR}")
        else:
            print(f"  {FALSE_COLOR}{input} not run{END_COLOR}")
    print()


def read_data(day, file):
    try:
        with open(f"./data/{day}_{file}", "r") as file:
            return file.read().strip()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}")
    except IOError as e:
        raise IOError(f"Error reading file: {e}")


def read_data_as_lines(day, file, strip_whitespace=True):
    lines = read_data(day, file).splitlines()
    return (
        [line.strip() for line in lines if line.strip()] if strip_whitespace else lines
    )


if __name__ == "__main__":
    print("Advent of Code 2024")
