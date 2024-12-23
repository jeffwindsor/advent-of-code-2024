import os
import inspect

TITLE_COLOR = "\033[100m"
FALSE_COLOR = "\033[91m"
TRUE_COLOR = "\033[92m"
END_COLOR = "\033[0m"


def run(func, test_cases):
    filename = os.path.basename(inspect.stack()[1].filename)

    print(f"{TITLE_COLOR}{filename}: {func.__name__}{END_COLOR}")
    for tc in test_cases:
        # default any missing execute_test to True
        input, expected, execute_test = (tc + (True,))[:3]
        if execute_test:
            actual = func(input)
            result = expected == actual
            print(
                f"  {input}: {TRUE_COLOR if result else FALSE_COLOR}{result} ",
                end="",
            )
            if result:
                print(f"{actual}{END_COLOR}")
            else:
                print(f"{expected} != {actual}{END_COLOR}")
        else:
            print(f"  {FALSE_COLOR}{input} not run")
    print()
