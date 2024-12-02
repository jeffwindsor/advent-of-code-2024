# Day 1 File Parser
def parse_line(line):
    return list(map(int, line.strip().split("   ")))

def parse(file):
    with open(file, "r") as file:
        lines = file.readlines()

    return list(zip(*map(parse_line, lines)))

if __name__ == "__main__":
    print(f"example: {parse('example')}")
