# Day 1, Part 1
# Sort, Zip. Map ABS(a - b), Sum 
from parser import parse 

def distance(ps):
    return abs(ps[0] - ps[1])

def problem(file):
    first, second = parse(file)
    data = zip(sorted(first), sorted(second))
    return sum(map(distance, data))

if __name__ == "__main__":
    print(f"example: {problem('example') == 11}")
    print(f"answer: {problem('puzzle_input')}")
