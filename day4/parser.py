# return lines without returns
def parse(file):
    with open(file, "r") as file:
        return [line.strip() for line in file]

if __name__ == "__main__":
    print(f"example: {parse('example')}")
