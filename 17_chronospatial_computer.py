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
    # Test A values starting from 1 upward
    A = 1
    while True:
        output = run_program(program, A, reg_b, reg_c)
        # Convert output to a list of integers for comparison
        output_program = list(map(int, output.split(",")))
        if output_program == program:
            return A
        A += 1


if __name__ == "__main__":
    # print(f"p1.e1 (4,6,3,5,6,3,5,2,1,0): {run_program([0,1,5,4,3,0],729,0,0)}")
    # print(f"p1.pi (): {run_program([2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0],37283687,0,0)}")

    print(
        f"p2.e2 (117440): {find_lowest_a_for_self_replicating_program([0, 3, 5, 4, 3, 0],0,0)}"
    )
    print(
        f"p2.pi (): {find_lowest_a_for_self_replicating_program([2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0],0,0)}"
    )
