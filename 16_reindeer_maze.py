from heapq import heappush, heappop
from aoc import (
    read_data_as_lines,
    run,
    TestCase,
    find_first,
    matrix_max_bounds,
    matrix_get,
    Coord,
)

EAST = Coord.DIRECTIONS_CARDINAL.index(Coord.RIGHT)


def parse(data_file):
    matrix = read_data_as_lines(data_file)
    start = find_first(matrix, "S")
    end = find_first(matrix, "E")
    return matrix, start, end


def find_lowest_score(matrix, start, end):
    hb = matrix_max_bounds(matrix)
    direction_cost = 1000
    forward_cost = 1

    pq = []  # Priority queue: (score, counter, coord, direction)
    counter = 0
    heappush(pq, (0, counter, start, EAST))
    counter += 1
    visited = set()

    while pq:
        score, _, cc, direction = heappop(pq)

        # Skip if already visited
        if (cc, direction) in visited:
            continue
        visited.add((cc, direction))

        # If we reach the end, return the score
        if cc == end:
            return score

        # Try moving forward
        dc = Coord.DIRECTIONS_CARDINAL[direction]
        nc = cc + dc

        if nc.in_bounds(hb) and matrix_get(matrix, nc) != "#":
            heappush(pq, (score + forward_cost, counter, nc, direction))
            counter += 1

        # Try rotating left and right
        for turn in [-1, 1]:  # Left and right
            new_direction = (direction + turn) % 4
            heappush(pq, (score + direction_cost, counter, cc, new_direction))
            counter += 1


def part1(file):
    return find_lowest_score(*parse(file))


if __name__ == "__main__":
    run(part1, [
        TestCase("16_example", 7036),
        TestCase("16_example2", 11048),
        TestCase("16_puzzle_input", 94444),
    ])
