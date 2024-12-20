import os
import inspect

TITLE_COLOR = "\033[100m"
FALSE_COLOR = "\033[91m"
TRUE_COLOR = "\033[92m"
END_COLOR = "\033[0m"


def run(test_cases) -> None:
    print()
    print(f"{TITLE_COLOR}{os.path.basename(inspect.stack()[1].filename)}{END_COLOR}")
    for name, func, input_file, expected in test_cases:
        actual = func(input_file)
        result = expected == actual
        print(
            f"  {func.__name__} {input_file}: {TRUE_COLOR if result else FALSE_COLOR}[{result}] ",
            end="",
        )
        if result:
            print(f"{actual}{END_COLOR}")
        else:
            print(f"{expected} != {actual}{END_COLOR}")
    print()
