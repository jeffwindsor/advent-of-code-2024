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


def find_all_best_path_tiles(matrix, start, end):
    """Find all tiles that are part of at least one best path."""
    hb = matrix_max_bounds(matrix)
    direction_cost = 1000
    forward_cost = 1

    # First pass: find the minimum score to reach each (coord, direction) state
    pq = []
    counter = 0
    heappush(pq, (0, counter, start, EAST))
    counter += 1
    best_scores = {}  # (coord, direction) -> best score

    while pq:
        score, _, cc, direction = heappop(pq)

        state = (cc, direction)
        # Skip if we've already found a better path to this state
        if state in best_scores and best_scores[state] < score:
            continue
        best_scores[state] = score

        # If we reach the end, continue to explore other paths
        if cc == end:
            continue

        # Try moving forward
        dc = Coord.DIRECTIONS_CARDINAL[direction]
        nc = cc + dc

        if nc.in_bounds(hb) and matrix_get(matrix, nc) != "#":
            new_state = (nc, direction)
            new_score = score + forward_cost
            if new_state not in best_scores or best_scores[new_state] >= new_score:
                heappush(pq, (new_score, counter, nc, direction))
                counter += 1

        # Try rotating left and right
        for turn in [-1, 1]:
            new_direction = (direction + turn) % 4
            new_state = (cc, new_direction)
            new_score = score + direction_cost
            if new_state not in best_scores or best_scores[new_state] >= new_score:
                heappush(pq, (new_score, counter, cc, new_direction))
                counter += 1

    # Find the minimum score to reach the end in any direction
    min_end_score = min(
        best_scores.get((end, d), float('inf'))
        for d in range(4)
    )

    # Second pass: backtrack from end to find all tiles on best paths
    tiles_on_best_paths = set()
    # Start from all end states with the minimum score
    backtrack_queue = [
        (end, d) for d in range(4)
        if best_scores.get((end, d), float('inf')) == min_end_score
    ]
    visited_backtrack = set(backtrack_queue)

    while backtrack_queue:
        cc, direction = backtrack_queue.pop(0)
        tiles_on_best_paths.add(cc)
        current_score = best_scores[(cc, direction)]

        # Check if we can reverse the forward move
        dc = Coord.DIRECTIONS_CARDINAL[direction]
        pc = cc - dc  # previous coord

        if pc.in_bounds(hb) and matrix_get(matrix, pc) != "#":
            prev_state = (pc, direction)
            expected_score = current_score - forward_cost
            if prev_state in best_scores and best_scores[prev_state] == expected_score:
                if prev_state not in visited_backtrack:
                    visited_backtrack.add(prev_state)
                    backtrack_queue.append(prev_state)

        # Check if we rotated to get here
        for turn in [-1, 1]:
            prev_direction = (direction - turn) % 4
            prev_state = (cc, prev_direction)
            expected_score = current_score - direction_cost
            if prev_state in best_scores and best_scores[prev_state] == expected_score:
                if prev_state not in visited_backtrack:
                    visited_backtrack.add(prev_state)
                    backtrack_queue.append(prev_state)

    return len(tiles_on_best_paths)


def part1(file):
    return find_lowest_score(*parse(file))


def part2(file):
    return find_all_best_path_tiles(*parse(file))


if __name__ == "__main__":
    run(part1, [
        TestCase("16_example", 7036),
        TestCase("16_example2", 11048),
        TestCase("16_puzzle_input", 94444),
    ])

    run(part2, [
        TestCase("16_example", 45),
        TestCase("16_example2", 64),
        TestCase("16_puzzle_input", 502),
    ])
