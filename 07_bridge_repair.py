from parser import parse
from itertools import product

PLUS = '+'
MULTIPLY = '*'
CONCATENATE = '||'

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
    for operators in product(operators, repeat=n-1):
        if evaluate_expression(nums, operators) == goal:
            return True

    return False

def answer(file, operators):
    success_numbers = [goal for goal, nums in parse(file)
                       if is_goal_possible(goal, nums, operators)]
    # print(success_numbers)
    return sum(success_numbers)


def part1(file):
    return answer(file, [PLUS, MULTIPLY])


def part2(file):
    return answer(file, [PLUS, MULTIPLY, CONCATENATE])


if __name__ == "__main__":
    print(f"part 1 example should be 3749: {part1('example')}")
    print(f"part 1 should be 5095: {part1('puzzle_input')}")
    print(f"part 2 example should be 11387: {part2('example')}")
    print(f"part 2: {part2('puzzle_input')}")
