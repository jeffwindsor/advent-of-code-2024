from itertools import islice

def parse(file):
    with open(file, "r") as file:
        numbers = file.read().strip()

    # if no free space is given for last file block,
    # then add a zero for no following free space
    if len(numbers) % 2 == 1:
        numbers += '0'

    file_block_sizes = islice(numbers, 0, None, 2)  # first numbers
    free_spaces = islice(numbers, 1, None, 2)       # second numbers
    pairs = zip(file_block_sizes, free_spaces)

    # original_index, file_block_size, free_space
    return [(i, int(fb), int(fs)) for i, (fb, fs) in enumerate(pairs)]

if __name__ == "__main__":
    print(f"simple : {list(parse('example_simple'))}")
    print(f"example: {list(parse('example'))}")
