guard_char = '^'
obstruction_char = '#'


def parse(file):
    # read file contents
    with open(file, "r") as file:
        lines = file.readlines()

    # Initialize variables
    guard_coordinate = None
    obstruction_coordinates = set()

    # Process each line
    for row, line in enumerate(lines):
        # Strip removes newlines and trailing spaces
        for col, char in enumerate(line.strip()):
            if char == '^':
                guard_coordinate = (row, col)
            elif char == '#':
                obstruction_coordinates.add((row, col))

    return guard_coordinate, obstruction_coordinates, (row, col)


if __name__ == "__main__":
    print(parse('example'))
