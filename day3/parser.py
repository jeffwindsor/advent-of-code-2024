def parse(file):
    with open(file, "r") as file:
        return file.read()

if __name__ == "__main__":
    print(f"example: {parse('example')}")
