EMPTY = -1
def parse_value(value):
    if value.isdigit():
        return int(value)
    else:
        return EMPTY

def parse(file):
    with open(file, "r") as file:
        lines = file.readlines()

    return [list(map(parse_value, line.strip())) for line in lines]


if __name__ == "__main__":
    print(f"example1: {parse('example1')}")
