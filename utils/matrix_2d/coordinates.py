import operator

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


def add(a, b):
    return combine(a, b, operator.add)


def sub(a, b):
    return combine(a, b, operator.sub)


def combine(a, b, combine_func):
    return (combine_func(a[0], b[0]), combine_func(a[1], b[1]))


def is_between(x, higher, lower):
    return lower <= x <= higher


def is_within_bounds_inclusive(coord, higher_bounds, lower_bounds=ZERO):
    """Check if a coordinate is between 0,0 and bounds."""
    return is_between(coord[0], higher_bounds[0], lower_bounds[0]) and is_between(
        coord[1], higher_bounds[1], lower_bounds[1]
    )


def filter_within_bounds(coords, higher_bounds, lower_bounds=ZERO):
    return [
        c for c in coords if is_within_bounds_inclusive(c, higher_bounds, lower_bounds)
    ]
