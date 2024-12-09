from parser import parse
from itertools import combinations

def is_out_of_bounds(limits, coord):
    return (coord[0] < 0 or coord[0] > limits[0] or
            coord[1] < 0 or coord[1] > limits[1])

def part1(file):
    antinodes = []
    limits, frequency_coords = parse(file)

    def add_if_in_bounds(c):
        if not is_out_of_bounds(limits, c):
            antinodes.append(c)

    for _, coords in frequency_coords.items():
        for (x1, y1), (x2, y2) in combinations(coords, 2):
            dx, dy = x1 - x2, y1 - y2
            add_if_in_bounds((x2 - dx, y2 - dy))
            add_if_in_bounds((x1 + dx, y1 + dy))

    return len(set(antinodes))


def part2(file):
    antinodes = []
    limits, frequency_coords = parse(file)

    def add_if_in_bounds(c):
        if not is_out_of_bounds(limits, c):
            antinodes.append(c)
            return True
        return False

    for _, coords in frequency_coords.items():
        for (x1, y1), (x2, y2) in combinations(coords, 2):
            dx, dy = x1 - x2, y1 - y2

            while add_if_in_bounds((x2, y2)):
                x2 -= dx
                y2 -= dy

            while add_if_in_bounds((x1, y1)):
                x1 += dx
                y1 += dy

    return len(set(antinodes))


if __name__ == "__main__":
    print(f"part 1 (  14): {part1('example')}")
    print(f"part 1 ( 426): {part1('puzzle_input')}")
    print(f"part 2 (  34): {part2('example')}")
    print(f"part 2 (1359): {part2('puzzle_input')}")

