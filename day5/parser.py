from collections import defaultdict

def parse(file):
    # read file contents
    with open(file, "r") as file:
        file_contents = file.read()

    # Splitting the file contents into two sections
    sections = file_contents.strip().split("\n\n")

    # Section 1: Parsing page ordering rules into a dictionary
    page_ordering_rules = defaultdict(list)
    for line in sections[0].splitlines():
        key, value = map(int, line.strip().split('|'))
        page_ordering_rules[key].append(value)

    # Section 2: Parsing page updates into a list of lists
    page_updates = [list(map(int, line.strip().split(','))) for line in sections[1].splitlines()]

    return page_ordering_rules, page_updates


def pprint(file):
    print(f"File: {file}")
    page_ordering_rules, page_updates = parse(file)

    print("Page Ordering Rules (Dictionary):")
    for key, values in page_ordering_rules.items():
        print(f"{key}: {values}")

    print("\nPage Updates (List of Lists):")
    for update in page_updates:
        print(update)


if __name__ == "__main__":
    pprint('example1')
    #pprint('puzzle_input')

