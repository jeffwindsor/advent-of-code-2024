from parser import parse
from functools import cmp_to_key


def middle_numbers(xss):
    return [xs[len(xs) // 2] for xs in xss]


def intersection(a, b):
    return list(set(a) & set(b))


def is_ordered(rules, pages):
    # using previous page comparison so can safely skip first page in list
    for i, p in enumerate(pages, start=1):
        # skip if no rules exists for current page
        if p not in rules:
            next
        # if any pages are in the intersection of previous pages and rules,
        # the list is unordered
        if intersection(pages[:i], rules[p]):
            return False

    return True


def part1(file):
    rules, pss = parse(file)
    ordered_pss = [ps for ps in pss if is_ordered(rules, ps)]
    return sum(middle_numbers(ordered_pss))


def part2(file):
    rules, pss = parse(file)

    def rules_comparer(x, y):
        if x == y:
            return 0  # they are equal
        elif x in rules:
            if y in rules[x]:
                return 1    # y must be before x
            else:
                return -1
        elif y in rules:
            if x in rules[y]:
                return -1   # x must be before y
            else:
                return 1
        else:
            raise Exception(f"not sure how to compare {x} to {y}")

    reordered_pss = [sorted(ps, key=cmp_to_key(rules_comparer))
                     for ps in pss if not is_ordered(rules, ps)]
    # print("RE", reordered_pss)
    return sum(middle_numbers(reordered_pss))


if __name__ == "__main__":
    print(f"part 1 example should be 143: {part1('example')}")
    print(f"part 1: {part1('puzzle_input')}")
    print(f"part 2 example should be 123: {part2('example')}")
    print(f"part 2: {part2('puzzle_input')}")
