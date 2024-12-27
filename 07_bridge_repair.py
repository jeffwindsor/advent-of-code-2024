from itertools import product
from aoc import read_data_as_lines, run

PLUS = "+"
MULTIPLY = "*"
CONCATENATE = "||"


def parse_line(line):
    answer, parts = line.strip().split(":")
    parts = map(int, parts.split())
    return (int(answer), list(parts))


def parse(file):
    lines = read_data_as_lines(7, file)
    return [parse_line(line) for line in lines]


def evaluate_expression(nums, operators):
    result = nums[0]
    for i in range(len(operators)):
        if operators[i] == PLUS:
            result += nums[i + 1]
        elif operators[i] == MULTIPLY:
            result *= nums[i + 1]
        elif operators[i] == CONCATENATE:
            result = int(str(result) + str(nums[i + 1]))
    return result


def is_goal_possible(goal, nums, operators):
    n = len(nums)
    if n < 2:
        return nums[0] == goal

    # Test each operator combination
    for operators in product(operators, repeat=n - 1):
        if evaluate_expression(nums, operators) == goal:
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
    run(part1, [("example", 3749), ("puzzle_input", 1153997401072)])
    run(part2, [("example", 11387), ("puzzle_input", 97902809384118, False)])
