def split_and_map(func, split_on, lines):
    return [list(map(func, line.split(split_on))) for line in lines]


def read_data(day, file):
    with open(f"./data/{day}_{file}", "r") as file:
        lines = file.read()
    return lines


def read_data_as_lines(day, file):
    return read_data(day, file).splitlines(False)
