from itertools import islice

def parse(file):
    with open(file, "r") as file:
        numbers = file.read().strip()

    file_blocks = list(map(int, islice(numbers, 0, None, 2)))  # first numbers
    free_blocks = list(map(int, islice(numbers, 1, None, 2)))  # second numbers

    if len(file_blocks) > len(free_blocks):
        free_blocks.append(0)

    return file_blocks, free_blocks

if __name__ == "__main__":
    print(f"simple : {parse('example_simple')}")
    print(f"example: {parse('example')}")
