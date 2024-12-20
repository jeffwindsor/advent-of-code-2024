def parse_input(file_path: str):
    with open(file_path, "r") as file:
        lines = file.readlines()

    patterns = lines[0].strip()
    designs = [line.strip() for line in lines[2:]]
    return patterns, designs


def count_possible_designs(towel_patterns, desired_designs):
    # Parse towel patterns
    towel_patterns = towel_patterns.split(", ")

    # Initialize counter for feasible designs
    possible_count = 0

    # Check each desired design
    for design in desired_designs:
        # print(design)
        n = len(design)
        dp = [False] * (n + 1)
        dp[0] = True  # Base case: empty string can always be constructed

        # Fill dp array
        for i in range(1, n + 1):
            for pattern in towel_patterns:
                # Check if the pattern fits the current position
                if i >= len(pattern) and design[i - len(pattern) : i] == pattern:
                    dp[i] = dp[i] or dp[i - len(pattern)]

        # If the full design is feasible, increment the counter
        if dp[n]:
            # print("  YES")
            possible_count += 1

    return possible_count


def part1(filepath):
    return count_possible_designs(*parse_input(filepath))
    # return parse_input(filepath)


if __name__ == "__main__":
    # print(f"p1.e (6): {part1('example')}")
    print(f"p1.pi (): {part1('puzzle_input')}")
