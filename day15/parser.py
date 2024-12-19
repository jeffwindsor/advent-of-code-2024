#     Parse the Input:
#         Read the warehouse map and robot commands.
#         Store the map as a 2D grid of characters (#, ., O, @).
#         Concatenate the movement commands into a single string.


def parse_file(filepath):
    """
    Parse the warehouse map and movement commands.
    """
    with open(filepath, "r") as file:
        warehouse_map, move_lines = file.read().split("\n\n")

    return warehouse_map, "".join(move_lines.splitlines())


if __name__ == "__main__":
    print(f"example: {parse_file('example')}")
