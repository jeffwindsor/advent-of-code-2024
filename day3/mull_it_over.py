from parser import parse
from re import findall

def mul(match):
    return int(match[0]) * int(match[1])

def score(multiplies):
    return sum( map(mul, multiplies) )

def apply_do_and_dont(matches):
    include = True
    for match in matches:
        if match == "don't()":
            include = False
        elif match == "do()":
            include = True
        elif include:
            yield tuple(findall(r'\d+', match))


def part1(file):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    # find all returns tuple of (x,y)
    multiplies = findall(pattern, parse(file))
    return score(multiplies)

def part2(file):
    pattern = r"(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don't\(\))"
    # flatten since findall returns a tuple per match ('mul(x,y)','do()', "don't()")
    instructions = [m[0] or m[1] or m[2] for m in findall(pattern, parse(file))]
    multiplies = apply_do_and_dont(instructions)
    return score(multiplies)

if __name__ == "__main__":
    print(f"part 1 example should be 161: {part1('example')}")
    print(f"part 1: {part1('puzzle_input')}")
    print(f"part 2 example should be 48: {part2('example2')}")
    print(f"part 2: {part2('puzzle_input')}")