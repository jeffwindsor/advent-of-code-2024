def parse(file):
    with open(file, "r") as file:
        numbers = file.read().split()

    return [int(n) for n in numbers]


if __name__ == "__main__":
    print(f"example: {parse('example1')}")
