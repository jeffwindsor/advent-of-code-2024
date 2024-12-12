from parser import parse
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class Cell:
    x: int
    y: int
    value: int


def bfs(matrix, start_cell):
    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    queue = deque([start_cell])
    visited = set([start_cell])
    leaves = set()

    while queue:
        cell = queue.popleft()

        if cell.value == 9:
            leaves.add(cell)

        for dx, dy in directions:
            nx, ny = cell.x + dx, cell.y + dy
            if (0 <= nx < rows and 0 <= ny < cols):
                next_cell = Cell(nx, ny, matrix[nx][ny])
                if next_cell not in visited and cell.value + 1 == next_cell.value:
                    queue.append(next_cell)
                    visited.add(next_cell)
    return leaves


def find_zeros(matrix):
    rows, cols = len(matrix), len(matrix[0])
    return [Cell(x, y, matrix[x][y])
            for y in range(rows)
            for x in range(cols)
            if matrix[x][y] == 0]


def part1(file):
    topo_map = parse(file)
    return sum([len(bfs(topo_map, zero_cell)) for zero_cell in find_zeros(topo_map)])


def part2(file):
    topo_map = parse(file)
    # return sum([len(bfs(topo_map, zero_cell)) for zero_cell in find_zeros(topo_map)])
    pass

if __name__ == "__main__":
    print(f"1:example1 (1): {part1('example1')}")
    print(f"1:example2 (2): {part1('example2')}")
    print(f"1:example3 (4): {part1('example3')}")
    print(f"1:example4 (3): {part1('example4')}")
    print(f"1:example5 (36): {part1('example5')}")
    print(f"1:example (674): {part1('puzzle_input')}")
