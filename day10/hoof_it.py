from parser import parse
from collections import deque


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right


# =============================================================================
def find_reachable_nines(matrix, starts):
    rows, cols = len(matrix), len(matrix[0])
    queue = deque([starts])
    visited = set([starts])
    leaves = set()

    while queue:
        (x, y) = queue.popleft()
        v = matrix[x][y]

        if v == 9:
            leaves.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                next = (nx, ny)
                if next not in visited and v + 1 == matrix[nx][ny]:
                    queue.append(next)
                    visited.add(next)
    return leaves


def find_zeros(matrix):
    rows, cols = len(matrix), len(matrix[0])
    return [(x, y) for y in range(rows) for x in range(cols) if matrix[x][y] == 0]


def part1(file):
    topo_map = parse(file)
    zeros = find_zeros(topo_map)
    return sum([len(find_reachable_nines(topo_map, z)) for z in zeros])


# =============================================================================
def dfs_paths(matrix, start):
    def inner(matrix, rows, cols, start, count, path=None):
        if path is None:
            path = [start]

        x, y = start
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                next = (nx, ny)
                print(f"[{count}]{path} : {next}")
                if matrix[nx][ny] == 9:
                    count = +1
                    continue

                if next not in path and matrix[x][y] + 1 == matrix[nx][ny]:
                    new_path = path + [next]
                    count += inner(matrix, rows, cols, next, count, new_path)

        return count

    return inner(matrix, len(matrix), len(matrix[0]), start, 0)


def part2(file):
    topo = parse(file)
    zeros = find_zeros(topo)
    results = [dfs_paths(topo, zero) for zero in zeros]
    print(results)
    return sum(results)


# =============================================================================
if __name__ == "__main__":
    # print(f"1:example1 (1): {part1('example1')}")
    # print(f"1:example2 (2): {part1('example2')}")
    # print(f"1:example3 (4): {part1('example3')}")
    # print(f"1:example4 (3): {part1('example4')}")
    # print(f"1:example5 (36): {part1('example5')}")
    # print(f"1:example (674): {part1('puzzle_input')}")

    print(f"2:example_6 (3): {part2('example_6')}")
    # print(f"2:example_7 (13): {part1('example_7')}")
    # print(f"2:example_8 (121): {part1('example_8')}")
    # print(f"2:example_9 (81): {part1('example_9')}")
    # print(f"2:example (): {part1('puzzle_input')}")
