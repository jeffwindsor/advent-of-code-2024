def parse_line(line):
    answer, parts = line.strip().split(":")
    parts = map(int, parts.split())
    return (int(answer), list(parts))

def parse(file):
    # read file contents
    with open(file, "r") as file:
        lines = file.readlines()

    return [parse_line(line) for line in lines]

if __name__ == "__main__":
    print(parse('example'))
