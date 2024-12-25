from utils.runners import run
from utils.files import read_data_as_lines
from scripts.pads_for_21 import DIRECTION_PAD, NUMBER_PAD
from itertools import product

#
#     SHIP
#  ||======================================================================================||
#  || ME      || -40                || RADIATION         || DEPRESSURIZED    || ????       ||
#  || dpad-40 || robot-40 -> dpad-r || robot-r -> dpad-d ||robot-d -> npad-h ||historian   ||
#  ||======================================================================================||
#
#  start at [A] on d-pad
#  start at [A] on n-pad
#
#  d-pad [A] = robot move forward, pushing n-pad button
#  n-pad [A] = activate TODO
#


def generate_combinations(list_of_lists):
    # Generate all combinations respecting the order of the sublists
    combinations = product(*list_of_lists)
    # Ensure strings are concatenated properly
    return ["".join(combination) for combination in combinations]


def find_shortest(strings):
    if not strings:
        return []
    min_length = min(len(s) for s in strings)
    return [s for s in strings if len(s) == min_length]


def flatten(nested_list):
    # Check if the input is a list of lists
    if not isinstance(nested_list, list) or not all(
        isinstance(sublist, list) for sublist in nested_list
    ):
        return nested_list

    return sum(nested_list, [])


def robot_moves(pad, button_pushes):
    options = []
    current_button = "A"
    for push_button in button_pushes:
        # append movements from button to button then A for press
        paths = pad[(current_button, push_button)]
        options.append(paths)
        current_button = push_button
    # print("  options", options)
    results = generate_combinations(options)
    return list(results)


def shortest_robot_moves(pad, sequences):
    return find_shortest(flatten([robot_moves(pad, s) for s in sequences]))


def part1(file):
    result = []
    for button_seq in read_data_as_lines(21, file):
        # print("  button_seqs", [button_seq])
        d_seqs = shortest_robot_moves(NUMBER_PAD, [button_seq])
        # print("  d_seqs", d_seqs)
        r_seqs = shortest_robot_moves(DIRECTION_PAD, d_seqs)
        # print("  r_seqs", r_seqs)
        fourty_seqs = shortest_robot_moves(DIRECTION_PAD, r_seqs)
        # print("  40_seqs", fourty_seqs)

        button_seq_as_num = int(button_seq[:-1])
        shortest_seq_length = len(fourty_seqs[0])
        # print(button_seq_as_num, shortest_seq_length)
        result.append(button_seq_as_num * shortest_seq_length)

    # print("  result", result)
    return sum(result)


#      number pad           direction pad
#     +---+---+---+            +---+---+
#     | 7 | 8 | 9 |            | ^ | A |
#     +---+---+---+        +---+---+---+
#     | 4 | 5 | 6 |        | < | v | > |
#     +---+---+---+        +---+---+---+
#     | 1 | 2 | 3 |
#     +---+---+---+
#         | 0 | A |
#         +---+---+

if __name__ == "__main__":
    # print(generate_combinations([["<"], ["^"], ["^^>", "^>^", ">^^"], ["vvv"]]))
    run(
        part1,
        [
            ("pre_example", 1972),
            # ("pre_example2", 2660),
            ("example", 126384),
            ("puzzle_input", 278748),
        ],
    )
