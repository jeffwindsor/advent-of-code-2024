from parser import parse

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)


def turn(direction):
    if direction == UP:
        return RIGHT
    elif direction == RIGHT:
        return DOWN
    elif direction == DOWN:
        return LEFT
    elif direction == LEFT:
        return UP
    else:
        raise Exception("Direction not recognized")


def add(coord, direction):
    return (coord[0] + direction[0], coord[1] + direction[1])


def is_out_of_bounds(limits, coord):
    return (coord[0] < 0 or coord[0] > limits[0]
            or coord[1] < 0 or coord[1] > limits[1])


def find_path_unique_coords(direction, coord, obstructions, limits):
    unique_coords = set()
    while not is_out_of_bounds(limits, coord):
        next_coord = add(coord, direction)
        if next_coord in obstructions:
            # Obstructed must turn
            direction = turn(direction)
        else:
            # Unobstructed must advance
            unique_coords.add(coord)
            coord = next_coord
    return unique_coords


def part1(file):
    unique_path_coords = find_path_unique_coords(UP, *parse(file))
    return len(unique_path_coords)


def find_possible_loop_in_path(direction, coord, obstructions, limits):
    visited_vectors = set()
    while not is_out_of_bounds(limits, coord):
        vector = (coord, direction)
        # check it we have been here before
        # print("Current: ", vector, vector in visited_vectors)
        if vector in visited_vectors:
            # this is a loop
            return True

        visited_vectors.add(vector)
        next_coord = add(coord, direction)
        if next_coord in obstructions:
            # print("Turn Vec: ", visited_vectors)
            # Obstructed must turn
            direction = turn(direction)
        else:
            # Unobstructed must advance
            coord = next_coord

    # no loops found
    return False


def part2(file):
    coord, obstructions, limits = parse(file)
    # test added obstructions one by one, using path coords to lower test set
    results = []
    unique_path_coords = find_path_unique_coords(
        UP, coord, obstructions, limits)
    for obc in unique_path_coords:
        test_obstructions = obstructions.copy()
        test_obstructions.add(obc)
        results.append(find_possible_loop_in_path(
            UP, coord, test_obstructions, limits))

    return sum(results)


if __name__ == "__main__":
    print(f"part 1 example should be 41: {part1('example')}")
    print(f"part 1 should be 5095: {part1('puzzle_input')}")
    print(f"part 2 loop_test should be True: {
          find_possible_loop_in_path(UP, *parse('loop_test'))}")
    print(f"part 2 example should be 6: {part2('example')}")
    print(f"part 2: {part2('puzzle_input')}")
