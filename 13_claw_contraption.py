import numpy as np
from math import isclose
from aoc import read_data, run, TestCase
from re import findall


def as_integers(xs):
    return list(map(int, xs))


def split_list(xs, n):
    return [as_integers(xs[i : i + n]) for i in range(0, len(xs), n)]


def parse(data_file):
    text = read_data(data_file)
    return split_list(findall(r"[XY][+=](\d+)", text), 6)


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
    # print(f"example: {parse('example')}")
    run(part1, [
        TestCase("13_example", 480),
        TestCase("13_puzzle_input", 37128),
    ])
    run(part2, [
        TestCase("13_example", 875318608908),
        TestCase("13_puzzle_input", 74914228471331),
    ])
