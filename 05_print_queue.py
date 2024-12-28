from aoc import read_data, run
from collections import defaultdict
from functools import cmp_to_key


def parse(file):
    # read file contents
    file_contents = read_data(5, file)

    # Splitting the file contents into two sections
    sections = file_contents.strip().split("\n\n")

    # Section 1: Parsing page ordering rules into a dictionary
    page_ordering_rules = defaultdict(list)

    for line in sections[0].splitlines():
        key, value = map(int, line.strip().split("|"))
        page_ordering_rules[key].append(value)

    # Section 2: Parsing page updates into a list of lists
    page_updates = [
        list(map(int, line.strip().split(","))) for line in sections[1].splitlines()
    ]

    return page_ordering_rules, page_updates


def middle_numbers(xss):
    return [xs[len(xs) // 2] for xs in xss]


def is_ordered(rules, pages):
    # using previous page comparison so can safely skip first page in list
    for i, p in enumerate(pages, start=1):
        # skip if no rules exists for current page
        if p not in rules:
            next
        # if any pages are in the intersection of previous pages and rules,
        # the list is unordered
        if set(pages[:i]) & set(rules[p]):
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
                return 1  # y must be before x
            else:
                return -1
        elif y in rules:
            if x in rules[y]:
                return -1  # x must be before y
            else:
                return 1
        else:
            raise Exception(f"not sure how to compare {x} to {y}")

    reordered_pss = [
        sorted(ps, key=cmp_to_key(rules_comparer))
        for ps in pss
        if not is_ordered(rules, ps)
    ]
    # print("RE", reordered_pss)
    return sum(middle_numbers(reordered_pss))


if __name__ == "__main__":
    run(part1, [("example", 143), ("puzzle_input", 7198)])
    run(part2, [("example", 123), ("puzzle_input", 4230)])
