from parser import parse
import numpy as np
from math import isclose

tol = 0.00000000000001


def token_cost(a, b):
    # print(a, b, isclose(a, round(a)), isclose(b, round(b), rel_tol=0.000000000001))
    if isclose(a, round(a), rel_tol=tol) and isclose(b, round(b), rel_tol=tol):
        return round(a) * 3 + round(b)
    else:
        return 0


def solve_linear(m, prize_delta):
    buttons = np.array([[m[0], m[2]], [m[1], m[3]]])
    prize = np.array([m[4] + prize_delta, m[5] + prize_delta])
    return token_cost(*np.linalg.solve(buttons, prize))


def part1(file):
    inputs = parse(file)
    solutions = [solve_linear(input, 0) for input in inputs]
    # print(solutions)
    return sum(solutions)


def part2(file):
    inputs = parse(file)
    solutions = [solve_linear(input, 10000000000000) for input in inputs]
    # print(solutions)
    return sum(solutions)


if __name__ == "__main__":
    print(f"part 1 example (480): {part1('example')}")
    print(f"part 1 (37128): {part1('puzzle_input')}")
    print(f"part 2 example (875318608908): {part2('example')}")
    print(f"part 2 (74914228471331): {part2('puzzle_input')}")
