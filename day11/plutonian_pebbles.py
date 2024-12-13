from parser import parse


def change_stone(stone):
    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    if stone == 0:
        return 1
    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
    # The left half of the digits are engraved on the new left stone, and the right half of the digits are
    # engraved on the new right stone. (The new numbers don't keep extra leading zeroes:
    # 1000 would become stones 10 and 0.)
    sl = len(str(stone))
    if sl % 2 == 0:
        i = sl // 2
        ss = str(stone)
        return [int(ss[:i]), int(ss[i:])]
    # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number
    # multiplied by 2024 is engraved on the new stone.
    return stone * 2024


def blink(stones):
    result = []
    for stone in stones:
        changed = change_stone(stone)
        if isinstance(changed, list):
            result.extend(changed)
        else:
            result.append(changed)
    return result


def part1(file, blinks):
    stones = parse(file)
    # print(f"Original: {stones}")
    for b in range(blinks):
        stones = blink(stones)
        # print(f"[{b}]: {stones}")

    return len(stones)


def part2(file, blinks):
    pass


# =============================================================================
if __name__ == "__main__":
    print(f"1:example1 (7): {part1('example1',1)}")
    print(f"1:example2 (22): {part1('example2',6)}")
    print(f"1:example2 (55312): {part1('example2', 25)}")
    print(f"part 1 (222461): {part1('puzzle_input', 25)}")
    print(f"part 2 : {part2('puzzle_input', 75)}")

    # print(f"2:example_6 (3): {part2('example_6')}")
    # print(f"2:example_7 (13): {part1('example_7')}")
    # print(f"2:example_8 (121): {part1('example_8')}")
    # print(f"2:example_9 (81): {part1('example_9')}")
    # print(f"2:example (): {part1('puzzle_input')}")
