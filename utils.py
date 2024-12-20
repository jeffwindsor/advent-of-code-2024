def read_data(day, file):
    with open(f"./data/{day:02}_{file}", "r") as file:
        lines = file.read()
    return lines


def read_data_as_lines(day, file):
    return read_data(day, file).splitlines(False)


def run(test_cases) -> None:
    for name, func, input_file, expected in test_cases:
        actual = func(input_file)
        print(f"{name}: [{expected == actual}] {expected} == {actual}")
