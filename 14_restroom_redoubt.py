from parser import parse_file

GRID_WIDTH = 101
GRID_HEIGHT = 103
SECONDS = 100


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


def part1(filepath, seconds, width, height):
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


def part2(filepath, max_seconds, width, height):
    robots = parse_file(filepath)
    return find_minimum_safety_factor(robots, max_seconds, width, height)


if __name__ == "__main__":
    print(f"P1 example (Expected: 12): {part1('example',SECONDS,11,7)}")
    print(
        f"P1 puzzle_input (Expected: 218619324): {
        part1('puzzle_input',SECONDS,GRID_WIDTH,GRID_HEIGHT)}"
    )
    print(
        f"P2 puzzle_input (Expected: 6446): {
        part2('puzzle_input', 7000, GRID_WIDTH,GRID_HEIGHT)}"
    )
