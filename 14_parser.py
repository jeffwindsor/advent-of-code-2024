import re


def parse_line(line):
    px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
    return ((px, py), (vx, vy))


def parse_file(filepath):
    with open(filepath, "r") as file:
        return [parse_line(line) for line in file]


if __name__ == "__main__":
    print(f"example: {parse_file('example')}")
