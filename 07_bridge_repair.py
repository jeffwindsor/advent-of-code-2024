from aoc import Input, run, TestCase, count_digits

PLUS = "+"
MULTIPLY = "*"
CONCATENATE = "||"


def parse_line(line):
    answer, parts = line.strip().split(":")
    parts = map(int, parts.split())
    return (int(answer), list(parts))


def parse(data_file):
    lines = Input(data_file).as_lines()
    return [parse_line(line) for line in lines]


def is_goal_possible(goal, nums, available_operators, result=None, index=0):
    """
    Recursively check if goal is achievable with given numbers and operators.
    Uses pruning to skip impossible branches early.
    """
    # Base case: initialize with first number
    if result is None:
        if len(nums) < 2:
            return nums[0] == goal
        return is_goal_possible(goal, nums, available_operators, nums[0], 1)

    # Base case: all numbers processed
    if index >= len(nums):
        return result == goal

    # Early pruning: if result exceeds goal and concatenation isn't available,
    # remaining operations (+, *) can only increase or maintain the value
    if result > goal and CONCATENATE not in available_operators:
        return False

    next_num = nums[index]

    # Try each available operator
    for op in available_operators:
        if op == PLUS:
            new_result = result + next_num
        elif op == MULTIPLY:
            new_result = result * next_num
        elif op == CONCATENATE:
            # Use math instead of string concatenation for performance
            digits = count_digits(next_num)
            new_result = result * (10 ** digits) + next_num
        else:
            continue

        # Recurse with the new result - return True immediately on first success
        if is_goal_possible(goal, nums, available_operators, new_result, index + 1):
            return True

    return False


def answer(file, operators):
    success_numbers = [
        goal for goal, nums in parse(file) if is_goal_possible(goal, nums, operators)
    ]
    # print(success_numbers)
    return sum(success_numbers)


def part1(file):
    return answer(file, [PLUS, MULTIPLY])


def part2(file):
    return answer(file, [PLUS, MULTIPLY, CONCATENATE])


if __name__ == "__main__":
    run(part1, [
        TestCase("./data/07_example", 3749),
        TestCase("./data/07_puzzle_input", 1153997401072),
    ])
    run(part2, [
        TestCase("./data/07_example", 11387),
        TestCase("./data/07_puzzle_input", 97902809384118),
    ])
