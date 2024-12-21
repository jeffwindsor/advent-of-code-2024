from heapq import heappush, heappop


def read_input(filepath):
    with open(filepath, "r") as file:
        return file.read()


def parse_maze(maze):
    start, end = None, None
    grid = []
    for y, line in enumerate(maze.strip().split("\n")):
        row = list(line)
        grid.append(row)
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)
    return grid, start, end


def find_lowest_score(maze):
    # Parse the maze
    grid, start, end = parse_maze(maze)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # E, S, W, N
    direction_cost = 1000
    forward_cost = 1

    # Priority queue: (score, x, y, direction)
    pq = []
    heappush(pq, (0, start[0], start[1], 0))  # Start facing East

    # Visited set: (x, y, direction)
    visited = set()

    while pq:
        score, x, y, direction = heappop(pq)

        # Skip if already visited
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

        # If we reach the end, return the score
        if (x, y) == end:
            return score

        # Try moving forward
        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != "#":
            heappush(pq, (score + forward_cost, nx, ny, direction))

        # Try rotating left and right
        for turn in [-1, 1]:  # Left and right
            new_direction = (direction + turn) % 4
            heappush(pq, (score + direction_cost, x, y, new_direction))


def part1(filepath):
    return find_lowest_score(read_input(filepath))


if __name__ == "__main__":
    print(f"part 1 example (7036): {part1('example')}")
    print(f"part 1 example 2 (11048): {part1('example2')}")
    print(f"part 1 (): {part1('puzzle_input')}")
