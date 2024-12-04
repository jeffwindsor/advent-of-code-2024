from parser import parse

search_word_directions = [
        (0, 1),   # right
        (0, -1),  # left
        (1, 0),   # down
        (-1, 0),  # up
        (1, 1),   # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1)  # up-left
    ]

def search_word(word,grid):
    grid_rows, grid_cols = len(grid), len(grid[0])
    for r in range(grid_rows):
        for c in range(grid_cols):
            yield sum(search_word_at_point(word, grid, grid_rows, grid_cols, r, c))

def search_word_at_point(word, grid, grid_rows, grid_cols, r, c):
    for dr, dc in search_word_directions:
        yield search_word_in_direction(word, grid, grid_rows, grid_cols, r, c, dr, dc)

def search_word_in_direction(word, grid, grid_rows, grid_cols, r, c, dr, dc):
    for i in range(len(word)):
        nr, nc = r + i * dr, c + i * dc
        #short circuit any boundry violation or non char match
        if (nr < 0 
        or nr >= grid_rows 
        or nc < 0 
        or nc >= grid_cols 
        or grid[nr][nc] != word[i]):
            return False
    return True

def part1(file):
    return sum(search_word("XMAS", parse(file)))


def search_x_mas(grid):
    rows, cols = len(grid) , len(grid[0])
    # rotate through inside of grid using a one cell border
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            yield search_x_mas_at_point(grid, r, c)

valid_x_mas = ["MSMS","MMSS","SSMM","SMSM"] 
def search_x_mas_at_point(grid, r, c):
    # center point must be A
    if grid[r][c] != 'A': return False

    x = ''.join([ 
        grid[r-1][c-1], # up-left
        grid[r-1][c+1], # up-right
        grid[r+1][c-1], # down-left
        grid[r+1][c+1]  # down-right
    ])
    return x in valid_x_mas

def part2(file):
    return sum(search_x_mas(parse(file)))

if __name__ == "__main__":
    print(f"part 1 example 1 should be 4: {part1('example1.1')}")
    print(f"part 1 example 2 should be 18: {part1('example1.2')}")
    print(f"part 1: {part1('puzzle_input')}")
    print(f"part 2 example 1 should be 1: {part2('example2.1')}")
    print(f"part 2 example 2 should be 9: {part2('example2.2')}")
    print(f"part 2: {part2('puzzle_input')}")
