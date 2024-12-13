from parser import parse

area = "a"
perimeter = "p"


def calculate_area_and_perimeter(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def flood_fill(r, c, char):
        stack, area, perimeter = [(r, c)], 0, 0
        visited[r][c] = True
        while stack:
            x, y = stack.pop()
            area += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if grid[nx][ny] == char and not visited[nx][ny]:
                        stack.append((nx, ny))
                        visited[nx][ny] = True
                    elif grid[nx][ny] != char:
                        perimeter += 1
                else:
                    perimeter += 1
        return area, perimeter

    results = []
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                char = grid[r][c]
                area, perimeter = flood_fill(r, c, char)
                results.append((char, area, perimeter))
    return results


def part1(file):
    grid = parse(file)
    shapes = calculate_area_and_perimeter(grid)
    # print(shapes)
    return sum([shape[1] * shape[2] for shape in shapes])


def part2(files):
    pass


if __name__ == "__main__":
    print(f"part1 example (140): {part1('example')}")
    print(f"part1 example_xo (772): {part1('example_xo')}")
    print(f"part1 example_RIC (1930): {part1('example_RIC')}")
    print(f"part1 puzzle_input (1488414): {part1('puzzle_input')}")
