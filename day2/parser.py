# Day 1 File Parser
def parse_line(line):
    # split line into integer list
    return list(map(int, line.strip().split(" ")))

def parse(file):
    with open(file, "r") as file:
        lines = file.readlines()

    return list(map(parse_line, lines))

if __name__ == "__main__":
    print(f"example: {parse('example')}")
