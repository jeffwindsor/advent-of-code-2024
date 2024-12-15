from parser import parse_file

GRID_WIDTH = 101
GRID_HEIGHT = 103
SECONDS = 100


def simulate_robots(robots, seconds, width, height):
    """Simulate robot positions after a given time."""
    final_positions = []
    for (px, py), (vx, vy) in robots:
        new_x = (px + vx * seconds) % width
        new_y = (py + vy * seconds) % height
        final_positions.append((new_x, new_y))
    return final_positions


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


def part1(filepath, seconds, grid_width, grid_height):
    robots = parse_file(filepath)
    final_positions = simulate_robots(robots, seconds, grid_width, grid_height)
    quadrants = count_quadrants(final_positions, grid_width, grid_height)
    safety_factor = calculate_safety_factor(quadrants)
    return safety_factor


def part2(filepath):
    pass


if __name__ == "__main__":
    print(f"P1 example (12): {part1('example',SECONDS,11,7)}")
    print(
        f"P1 example (218619324): {part1('puzzle_input',SECONDS,GRID_WIDTH,GRID_HEIGHT)}"
    )
