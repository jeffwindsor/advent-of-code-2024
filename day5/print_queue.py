from parser import parse

def is_ordered(rules, pages):
    # using previous page comparison so can safely skip first page in list
    for i,p in enumerate(pages, start=1):
        # skip if no rules exists for current page
        if p not in rules: next
        # if any pages are in the intersection of previous pages and rules, the list is unordered
        if list(set(pages[:i]) & set(rules[p])): return False

    return True


def part1(file):
    rules, page_lists = parse(file)
    ordered_lists = [ps for ps in page_lists if is_ordered(rules, ps)]
    middle_numbers = [ps[len(ps) // 2] for ps in ordered_lists]
    return sum(middle_numbers)

def part2(file):
    pass

if __name__ == "__main__":
    print(f"part 1 example should be 143: {part1('example1')}")
    print(f"part 1: {part1('puzzle_input')}")
    # print(f"part 2 example should be _: {part2('example2')}")
    # print(f"part 2: {part2('puzzle_input')}")
