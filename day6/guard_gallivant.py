from parser import parse

directions = [
    (-1, 0),     # ^ up
    (0, 1),      # > right
    (1, 0),      # v down
    (0, -1)      # < left
]


def turn(current_direction):
    current_index = directions.index(current_direction)
    turn_to_index = (current_index + 1) % len(directions)
    return directions[turn_to_index]


def is_out_of_bounds(grid_limit, coord):
    return (coord[0] < 0 or coord[0] > grid_limit[0]
            or coord[1] < 0 or coord[1] > grid_limit[1])


def find_path(file):
    guard_coord, obstruction_coords, grid_limit = parse(file)
    guard_direction = directions[0]  # initial direction is up
    visited = set()

    while not is_out_of_bounds(grid_limit, guard_coord):
        next_guard_coord = (guard_coord[0] + guard_direction[0],
                            guard_coord[1] + guard_direction[1])
        if next_guard_coord in obstruction_coords:
            guard_direction = turn(guard_direction)
        else:
            visited.add(guard_coord)
            guard_coord = next_guard_coord

    return visited


def part1(file):
    visited = find_path(file)
    return len(visited)


def part2(file):
    pass


if __name__ == "__main__":
    print(f"part 1 example should be 41: {part1('example')}")
    print(f"part 1: {part1('puzzle_input')}")
    # print(f"part 2 example should be _: {part2('example')}")
    # print(f"part 2: {part2('puzzle_input')}")
