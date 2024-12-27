from itertools import repeat, islice
from aoc import read_data, run


def parse(file):
    numbers = read_data(9, file)
    file_blocks = list(map(int, islice(numbers, 0, None, 2)))  # first numbers
    free_blocks = list(map(int, islice(numbers, 1, None, 2)))  # second numbers

    if len(file_blocks) > len(free_blocks):
        free_blocks.append(0)

    return file_blocks, free_blocks


EMPTY_BLOCK = "."


def checksum(disk):
    return sum([i * int(n) for i, n in enumerate(disk) if n != EMPTY_BLOCK])


def part1(file):
    def expand(file_blocks, free_space):
        result = []
        for i in range(len(file_blocks)):
            result += repeat(str(i), file_blocks[i])
            result += repeat(EMPTY_BLOCK, free_space[i])
        return list(result)

    disk = expand(*parse(file))
    right = len(disk) - 1
    for left in range(len(disk)):
        if disk[left] == EMPTY_BLOCK:
            while disk[right] == EMPTY_BLOCK:
                right -= 1

            if left >= right:
                break
            else:
                disk[left] = disk[right]
                disk[right] = EMPTY_BLOCK
                # print(f"Move {right} to {left}")
                # print("".join(disk))
    return checksum(disk)


def find_available_free_space(free_space, block_size):
    for id, size in enumerate(free_space):
        if block_size <= size:
            # print(f"moves to {id}({size})")
            # reduce free space at fid by block size now there
            free_space[id] -= block_size
            return id
    return None


def part2(file):
    def expand(moved_blocks, free_space):
        result = []
        for i in range(len(moved_blocks)):
            for id, size in moved_blocks[i]:
                result += repeat(str(id), size)
            result += repeat(EMPTY_BLOCK, free_space[i])
        return list(result)

    file_blocks, free_space = parse(file)
    # 2d array of moved_blocks
    moved_blocks = [[] for _ in range(len(file_blocks))]

    for id, size in reversed(list(enumerate(file_blocks))):
        # print(f"{str(id) * size} ", end="")

        # remove file blocks, leaving more free space
        # worst case the blocks are moved back to original space
        free_space[id] += size
        file_blocks[id] = 0
        move_to_id = find_available_free_space(free_space, size)
        if move_to_id == id:
            # insert original at front of id/index list
            moved_blocks[move_to_id] = [(id, size)] + moved_blocks[move_to_id]
            continue

        elif move_to_id is not None:
            # edge case of moving a block after other block at index
            if moved_blocks[id]:
                # reduce free space at id by size
                free_space[id] -= size
                # insert a free space of size to front of list [244.] => [.44.]
                moved_blocks[id] = [(EMPTY_BLOCK, size)] + moved_blocks[id]

            # add to end of id/index list
            moved_blocks[move_to_id] += [(id, size)]
            continue

    disk = expand(moved_blocks, free_space)
    return checksum(disk)


if __name__ == "__main__":
    test_cases_part1 = [
        ("example_simple", 60),
        ("example", 1928),
        ("puzzle_input", 6332189866718),
    ]

    test_cases_part2 = [
        ("example_simple", 132),  # Expected: 132
        ("example", 2858),  # Expected: 2858
        ("puzzle_input", 6353648390778),  # Expected: 6353648390778
    ]

    # Run the tests
    run(part1, test_cases_part1)
    run(part2, test_cases_part2)
