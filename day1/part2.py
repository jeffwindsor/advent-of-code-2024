# Day 1, Part 2
from collections import Counter
from parser import parse

def similarity_score(dy, number):
    return number * dy[number]

def problem(file):
    xs, ys = parse(file)
    dy = Counter(ys)
    scores = list(map(lambda n: similarity_score(dy,n), xs))
    return sum(scores)


if __name__ == "__main__":
    print(f"example: {problem('example')}")
    print(f"answer: {problem('puzzle_input')}")
