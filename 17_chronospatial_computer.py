from aoc import run, TestCase


def run_program(program, reg_a, reg_b, reg_c):
    # Initialize registers and instruction pointer
    A, B, C = reg_a, reg_b, reg_c
    instruction_pointer = 0
    output = []

    # Helper function to get combo operand value
    def get_combo_value(operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        else:
            raise ValueError("Invalid combo operand")

    # Run the program
    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = (
            program[instruction_pointer + 1]
            if instruction_pointer + 1 < len(program)
            else 0
        )

        if opcode == 0:  # adv
            divisor = 2 ** get_combo_value(operand)
            A //= divisor

        elif opcode == 1:  # bxl
            B ^= operand

        elif opcode == 2:  # bst
            B = get_combo_value(operand) % 8

        elif opcode == 3:  # jnz
            if A != 0:
                instruction_pointer = operand
                continue  # Skip the normal instruction pointer increment

        elif opcode == 4:  # bxc
            B ^= C

        elif opcode == 5:  # out
            output.append(get_combo_value(operand) % 8)

        elif opcode == 6:  # bdv
            divisor = 2 ** get_combo_value(operand)
            B = A // divisor

        elif opcode == 7:  # cdv
            divisor = 2 ** get_combo_value(operand)
            C = A // divisor

        else:
            raise ValueError(f"Invalid opcode: {opcode}")

        # Move to the next instruction
        instruction_pointer += 2

    return ",".join(map(str, output))


def find_lowest_a_for_self_replicating_program(program, reg_b, reg_c):
    """
    Find the lowest value of A that makes the program output itself.

    Key insight: The program processes A in chunks (typically dividing by 8 each iteration).
    We work backwards from the desired output, building A one "digit" at a time.

    For each position in the output (from right to left), we try all possible 3-bit
    values and check if they produce the correct output suffix.
    """

    def search(pos, current_a):
        """
        Recursively search for A values.
        pos: current position in the program (working backwards from len-1 to 0)
        current_a: the A value built so far
        """
        # Base case: if we've processed all positions, check if A produces the full program
        if pos < 0:
            output = run_program(program, current_a, reg_b, reg_c)
            output_list = list(map(int, output.split(","))) if output else []
            return current_a if output_list == program else None

        # Try each possible 3-bit value (0-7) for the next chunk
        # We shift by 3 to make room for the next 3 bits
        for digit in range(8):
            # Build the test value by shifting current_a and adding the digit
            test_a = (current_a << 3) | digit

            # Run the program and check if it matches the suffix we need
            output = run_program(program, test_a, reg_b, reg_c)
            output_list = list(map(int, output.split(","))) if output else []

            # Check if the output matches the expected suffix
            # We need output to match program[pos:]
            expected_suffix = program[pos:]
            if output_list == expected_suffix:
                # Recursively try to build the rest
                result = search(pos - 1, test_a)
                if result is not None:
                    return result

        return None

    # Start from the last position and work backwards
    result = search(len(program) - 1, 0)
    return result if result is not None else -1


def part1_test(test_name):
    """Test wrapper for part 1"""
    test_data = {
        "example1": ([0, 1, 5, 4, 3, 0], 729, 0, 0),
        "puzzle": ([2, 4, 1, 3, 7, 5, 4, 1, 1, 3, 0, 3, 5, 5, 3, 0], 37283687, 0, 0),
    }
    program, reg_a, reg_b, reg_c = test_data[test_name]
    return run_program(program, reg_a, reg_b, reg_c)


def part2_test(test_name):
    """Test wrapper for part 2"""
    test_data = {
        "example": ([0, 3, 5, 4, 3, 0], 0, 0),
        "puzzle": ([2, 4, 1, 3, 7, 5, 4, 1, 1, 3, 0, 3, 5, 5, 3, 0], 0, 0),
    }
    program, reg_b, reg_c = test_data[test_name]
    return find_lowest_a_for_self_replicating_program(program, reg_b, reg_c)


if __name__ == "__main__":
    run(
        part1_test,
        [
            TestCase("example1", "4,6,3,5,6,3,5,2,1,0"),
            TestCase("puzzle", "1,5,3,0,2,5,2,5,3"),
        ],
    )
    run(
        part2_test,
        [
            TestCase("example", 117440),
            TestCase("puzzle", 108107566389757),
        ],
    )
