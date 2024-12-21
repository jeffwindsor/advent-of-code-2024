def parse(file):
    with open(file, "r") as file:
        lines = file.readlines()

    result = {}

    for row, line in enumerate(lines):
        for col, char in enumerate(line.strip()):
            if char == ".":
                continue
            if char not in result:
                result[char] = []
            result[char].append((row, col))

    return (row, col), result

if __name__ == "__main__":
    print(f"example: {parse('example')}")
