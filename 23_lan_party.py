from aoc import read_data_as_graph_edges, find_max_clique, run, TestCase

# frozenset - immutable set that is hashable, used to avoid duplicates

CHIEFS_COMPUTER_PREFIX = "t"
NETWORK_SIZE = 3


def find_all_networks(graph):
    """
    Find all sets of three interconnected computers (triangles in graph).
    """
    networks = set()

    for a in graph:
        for b in graph[a]:
            for c in graph[b]:
                if c in graph[a]:
                    # Triangle Found
                    network = frozenset([a, b, c])
                    if len(network) == NETWORK_SIZE:  # Ensure 3 distinct nodes
                        networks.add(network)

    return networks


def contains_chiefs_computer(network):
    return any(computer.startswith(CHIEFS_COMPUTER_PREFIX) for computer in network)


def count_chiefs_networks(data_file):
    graph = read_data_as_graph_edges(data_file)
    networks = find_all_networks(graph)
    count = sum(contains_chiefs_computer(network) for network in networks)
    return count


def find_largest_clique(data_file):
    """
    Find the largest fully-connected group of computers and return the password.
    Returns computers sorted alphabetically, joined with commas.
    """
    graph = read_data_as_graph_edges(data_file)
    largest_clique = find_max_clique(graph)
    password = ",".join(sorted(largest_clique))
    return password


if __name__ == "__main__":
    run(
        count_chiefs_networks,
        [
            TestCase("23_example_01", 7),
            TestCase("23_puzzle_input", 1218),
        ],
    )

    run(
        find_largest_clique,
        [
            TestCase("23_example_01", "co,de,ka,ta"),
            TestCase("23_puzzle_input", "ah,ap,ek,fj,fr,jt,ka,ln,me,mp,qa,ql,zg"),
        ],
    )
