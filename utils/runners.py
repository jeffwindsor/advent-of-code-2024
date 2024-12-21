import os
import inspect

TITLE_COLOR = "\033[100m"
FALSE_COLOR = "\033[91m"
TRUE_COLOR = "\033[92m"
END_COLOR = "\033[0m"


def run(func, test_cases):
    filename = os.path.basename(inspect.stack()[1].filename)

    print(f"{TITLE_COLOR}{filename}: {func.__name__}{END_COLOR}")
    for input_file, expected in test_cases:
        actual = func(input_file)
        result = expected == actual
        print(
            f"  {input_file}: {TRUE_COLOR if result else FALSE_COLOR}{result} ",
            end="",
        )
        if result:
            print(f"{actual}{END_COLOR}")
        else:
            print(f"{expected} != {actual}{END_COLOR}")
    print()
