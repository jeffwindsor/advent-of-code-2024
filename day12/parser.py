def parse(file):
    with open(file, "r") as file:
        lines = file.readlines()

    return [list(line.strip()) for line in lines]


if __name__ == "__main__":
    print(f"example: {parse('example')}")
