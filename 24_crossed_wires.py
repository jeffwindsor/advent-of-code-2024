from aoc import Input, run, TestCase

# Gate operation constants
OP_AND = "AND"
OP_OR = "OR"
OP_XOR = "XOR"


def parse_data(data_file):
    """Parse initial wire values and gate connections."""
    section1, section2 = Input(data_file).as_two_parts()

    # Parse initial wire values from first section
    wire_values = {}
    for line in section1.as_lines():
        wire, value = line.split(': ')
        wire_values[wire] = int(value)

    # Parse gate connections from second section
    gates = []
    for line in section2.as_lines():
        parts = line.split(' -> ')
        output = parts[1]
        input_parts = parts[0].split()
        input1 = input_parts[0]
        operation = input_parts[1]
        input2 = input_parts[2]
        gates.append((input1, operation, input2, output))

    return wire_values, gates

def simulate_gates(wire_values, gates):
    """Simulate gate operations until all outputs are determined."""
    # Keep track of which gates haven't been processed yet
    remaining_gates = gates.copy()

    while remaining_gates:
        processed = []
        for i, (input1, operation, input2, output) in enumerate(remaining_gates):
            # Check if both inputs are available
            if input1 in wire_values and input2 in wire_values:
                val1 = wire_values[input1]
                val2 = wire_values[input2]

                # Compute output based on operation
                if operation == OP_AND:
                    result = val1 & val2
                elif operation == OP_OR:
                    result = val1 | val2
                elif operation == OP_XOR:
                    result = val1 ^ val2

                wire_values[output] = result
                processed.append(i)

        # Remove processed gates (in reverse order to maintain indices)
        for i in reversed(processed):
            remaining_gates.pop(i)

    return wire_values

def get_z_output(wire_values):
    """Extract and combine all z wire values into a decimal number.

    Returns:
        int: Decimal number formed by z wires (z00 is least significant bit)
    """
    # Get all z wires and sort them
    z_wires = sorted([wire for wire in wire_values if wire.startswith('z')])

    # Build binary number (z00 is least significant bit)
    binary_str = ''.join(str(wire_values[wire]) for wire in reversed(z_wires))

    return int(binary_str, 2)

def decode_wire_output(data_file):
    """Simulate the gate system and decode the output number.

    The system uses AND, OR, and XOR gates to process wire values.
    All z-prefixed wires combine to form the final output number.

    Returns:
        int: The decimal number produced by the gate system
    """
    wire_values, gates = parse_data(data_file)
    wire_values = simulate_gates(wire_values, gates)
    return get_z_output(wire_values)

def find_swapped_wires(data_file):
    """Find the wires involved in swapped gate outputs.

    The circuit should implement a binary adder (x + y = z).
    Four pairs of gate outputs have been swapped.

    Returns:
        str: Comma-separated sorted list of 8 swapped wire names
    """
    _, gates = parse_data(data_file)

    # Build maps for circuit analysis
    wire_to_gate = {}
    for gate in gates:
        input1, op, input2, output = gate
        wire_to_gate[output] = (input1, op, input2)

    # Find bit width
    z_wires = sorted([w for w in wire_to_gate.keys() if w.startswith('z')])
    num_bits = len(z_wires)

    wrong_wires = set()

    def find_gate_output(in1, in2, op):
        """Find output wire of gate with given inputs and operation."""
        for gate in gates:
            g_in1, g_op, g_in2, g_out = gate
            if g_op == op and {g_in1, g_in2} == {in1, in2}:
                return g_out
        return None

    # Rule 1: All z outputs except the last must come from XOR gates
    for i in range(num_bits - 1):
        z_wire = f"z{i:02d}"
        if z_wire in wire_to_gate:
            _, op, _ = wire_to_gate[z_wire]
            if op != OP_XOR:
                wrong_wires.add(z_wire)

    # Rule 2: XOR gates not involving x,y inputs must output to z
    for gate in gates:
        in1, op, in2, out = gate
        if op == OP_XOR:
            # Check if this XOR takes x,y inputs
            if not ((in1.startswith('x') and in2.startswith('y')) or
                   (in1.startswith('y') and in2.startswith('x'))):
                # This is an internal XOR (sum gate), must output to z
                if not out.startswith('z'):
                    wrong_wires.add(out)

    # Rule 3: XOR gates with x,y inputs (except x00,y00) must feed into another XOR
    for gate in gates:
        in1, op, in2, out = gate
        if op == OP_XOR:
            if ((in1.startswith('x') and in2.startswith('y')) or
                (in1.startswith('y') and in2.startswith('x'))):
                # Skip x00, y00 which goes directly to z00
                if in1 in ['x00', 'y00'] or in2 in ['x00', 'y00']:
                    continue
                # This half-sum must feed into another XOR
                feeds_xor = False
                for other_gate in gates:
                    o_in1, o_op, o_in2, o_out = other_gate
                    if o_op == OP_XOR and (o_in1 == out or o_in2 == out):
                        feeds_xor = True
                        break
                if not feeds_xor:
                    wrong_wires.add(out)

    # Rule 4: AND gates (except x00 AND y00) must feed into OR gates
    for gate in gates:
        in1, op, in2, out = gate
        if op == OP_AND:
            # Skip x00 AND y00 which is the initial carry
            if (in1 in ['x00', 'y00'] and in2 in ['x00', 'y00']):
                continue
            # This AND must feed into an OR
            feeds_or = False
            for other_gate in gates:
                o_in1, o_op, o_in2, o_out = other_gate
                if o_op == OP_OR and (o_in1 == out or o_in2 == out):
                    feeds_or = True
                    break
            if not feeds_or:
                wrong_wires.add(out)

    return ','.join(sorted(wrong_wires))

if __name__ == "__main__":
    run(
        decode_wire_output,
        [
            TestCase("./data/24_example_01", 4),
            TestCase("./data/24_example_02", 2024),
            TestCase("./data/24_puzzle_input", 52038112429798),
        ],
    )

    run(
        find_swapped_wires,
        [
            # Note: Part 2 example is a simple AND circuit, not an adder,
            # so adder-specific detection rules don't apply to it
            TestCase("./data/24_puzzle_input", "cph,jqn,kwb,qkf,tgr,z12,z16,z24"),
        ],
    )
