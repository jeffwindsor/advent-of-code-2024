from aoc import (
    read_data_as_lines,
    run,
    TestCase,
    find_first,
    grid_max_bounds,
    grid_get,
    Coord,
    dijkstra,
)

EAST = Coord.DIRECTIONS_CARDINAL.index(Coord.RIGHT)


def parse(data_file):
    matrix = read_data_as_lines(data_file)
    start = find_first(matrix, "S")
    end = find_first(matrix, "E")
    return matrix, start, end


def find_lowest_score(matrix, start, end):
    max_bounds = grid_max_bounds(matrix)
    direction_cost = 1000
    forward_cost = 1

    def neighbors_func(state):
        """Return list of (next_state, cost) tuples."""
        coord, direction = state
        neighbors = []

        # Try moving forward
        dc = Coord.DIRECTIONS_CARDINAL[direction]
        nc = coord + dc
        if nc.in_bounds(max_bounds) and grid_get(matrix, nc) != "#":
            neighbors.append(((nc, direction), forward_cost))

        # Try rotating left and right
        for turn in [-1, 1]:
            new_direction = (direction + turn) % 4
            neighbors.append(((coord, new_direction), direction_cost))

        return neighbors

    # Use generalized dijkstra with (coord, direction) state tuples
    start_state = (start, EAST)
    distances = dijkstra(start_state, neighbors_func)

    # Find minimum distance to end in any direction
    return min(
        distances.get((end, d), float('inf'))
        for d in range(4)
    )


def find_all_best_path_tiles(matrix, start, end):
    """Find all tiles that are part of at least one best path."""
    max_bounds = grid_max_bounds(matrix)
    direction_cost = 1000
    forward_cost = 1

    def neighbors_func(state):
        """Return list of (next_state, cost) tuples."""
        coord, direction = state
        neighbors = []

        # Try moving forward
        dc = Coord.DIRECTIONS_CARDINAL[direction]
        nc = coord + dc
        if nc.in_bounds(max_bounds) and grid_get(matrix, nc) != "#":
            neighbors.append(((nc, direction), forward_cost))

        # Try rotating left and right
        for turn in [-1, 1]:
            new_direction = (direction + turn) % 4
            neighbors.append(((coord, new_direction), direction_cost))

        return neighbors

    # First pass: find the minimum score to reach each (coord, direction) state
    start_state = (start, EAST)
    best_scores = dijkstra(start_state, neighbors_func)

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
        coord, direction = backtrack_queue.pop(0)
        tiles_on_best_paths.add(coord)
        current_score = best_scores[(coord, direction)]

        # Check if we can reverse the forward move
        dc = Coord.DIRECTIONS_CARDINAL[direction]
        prev_coord = coord - dc

        if prev_coord.in_bounds(max_bounds) and grid_get(matrix, prev_coord) != "#":
            prev_state = (prev_coord, direction)
            expected_score = current_score - forward_cost
            if prev_state in best_scores and best_scores[prev_state] == expected_score:
                if prev_state not in visited_backtrack:
                    visited_backtrack.add(prev_state)
                    backtrack_queue.append(prev_state)

        # Check if we rotated to get here
        for turn in [-1, 1]:
            prev_direction = (direction - turn) % 4
            prev_state = (coord, prev_direction)
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
