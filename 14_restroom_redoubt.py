from re import findall
from utils.files import read_data_as_lines
from utils.runners import run


def parse_line(line):
    px, py, vx, vy = map(int, findall(r"-?\d+", line))
    return ((px, py), (vx, vy))


def parse_file(filepath):
    return [parse_line(line) for line in read_data_as_lines(14, filepath)]


def simulate_robot_positions(robots, seconds, width, height):
    """Simulate robot positions after a given time."""
    positions = []
    for (px, py), (vx, vy) in robots:
        x = (px + vx * seconds) % width
        y = (py + vy * seconds) % height
        positions.append((x, y))
    return positions


def count_quadrants(positions, width, height):
    """Count robots in each quadrant excluding middle row/column."""
    middle_x, middle_y = width // 2, height // 2
    quadrants = [0, 0, 0, 0]  # Q1, Q2, Q3, Q4

    for x, y in positions:
        if x == middle_x or y == middle_y:
            continue  # Ignore robots on the middle line

        if x > middle_x and y < middle_y:  # Q1
            quadrants[0] += 1
        elif x < middle_x and y < middle_y:  # Q2
            quadrants[1] += 1
        elif x < middle_x and y > middle_y:  # Q3
            quadrants[2] += 1
        elif x > middle_x and y > middle_y:  # Q4
            quadrants[3] += 1

    return quadrants


def calculate_safety_factor(quadrants):
    """Calculate the safety factor as the product of quadrant counts."""
    result = 1
    for count in quadrants:
        result *= count
    return result


def part1(args):
    filepath, seconds, width, height = args
    robots = parse_file(filepath)
    final_positions = simulate_robot_positions(robots, seconds, width, height)
    quadrants = count_quadrants(final_positions, width, height)
    safety_factor = calculate_safety_factor(quadrants)
    return safety_factor


def find_minimum_safety_factor(robots, max_seconds, width, height):
    """Find the second with the minimum safety factor."""
    min_safety_factor = float("inf")
    best_second = None

    for t in range(max_seconds + 1):
        positions = simulate_robot_positions(robots, t, width, height)
        quadrants = count_quadrants(positions, width, height)
        safety_factor = calculate_safety_factor(quadrants)

        if safety_factor < min_safety_factor:
            min_safety_factor = safety_factor
            best_second = t

    return best_second


def part2(args):
    filepath, max_seconds, width, height = args
    robots = parse_file(filepath)
    return find_minimum_safety_factor(robots, max_seconds, width, height)


if __name__ == "__main__":
    run(
        part1,
        [(("example", 100, 11, 7), 12), (("puzzle_input", 100, 101, 103), 218619324)],
    )
    run(part2, [(("puzzle_input", 7000, 101, 103), 6446)])
