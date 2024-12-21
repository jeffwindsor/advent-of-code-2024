def parse_into_char_coords(lines, empty_char):
    result = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line.strip()):
            if char == empty_char:
                continue
            if char not in result:
                result[char] = []
            result[char].append((row, col))
    return result
