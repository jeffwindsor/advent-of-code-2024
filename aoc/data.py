"""Data reading and parsing utilities."""

from typing import Any


def read_data(data_file: str) -> str:
    """Read puzzle input file and return contents as string."""
    try:
        with open(f"./data/{data_file}", "r") as f:
            return f.read().strip()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}")
    except IOError as e:
        raise IOError(f"Error reading file: {e}")


def read_data_as_lines(data_file: str, strip_whitespace: bool = True) -> list[str]:
    """Read puzzle input file and return as list of lines."""
    lines = read_data(data_file).splitlines()
    return (
        [line.strip() for line in lines if line.strip()] if strip_whitespace else lines
    )


def read_data_as_ints(data_file: str) -> list[int]:
    """
    Read puzzle input file and return as list of integers (one per line).

    Args:
        data_file: Path to input file

    Returns:
        List of integers parsed from each line

    Example:
        Input file:
            123
            456
            789
        Returns: [123, 456, 789]
    """
    lines = read_data_as_lines(data_file)
    return [int(line) for line in lines]


def read_data_as_char_grid(data_file: str) -> list[list[str]]:
    """
    Read puzzle input file and return as 2D character grid.

    Returns:
        list[list[str]] where each inner list is a row of characters
    """
    return [list(line) for line in read_data_as_lines(data_file)]


def read_data_as_int_grid(data_file: str, empty_value: int = -1) -> list[list[int]]:
    """
    Read puzzle input file and return as 2D integer grid.

    Args:
        data_file: Path to input file
        empty_value: Value to use for non-digit characters (default: -1)

    Returns:
        list[list[int]] where each inner list is a row of integers
    """
    return [
        [int(char) if char.isdigit() else empty_value for char in line]
        for line in read_data_as_lines(data_file)
    ]


def read_data_as_coord_pairs(data_file: str, separator: str = ",") -> list[tuple[int, int]]:
    """
    Read file and parse lines of coordinate pairs into list of tuples.

    Args:
        data_file: Path to input file
        separator: Character separating coordinates (default: ',')

    Returns:
        List of (x, y) coordinate tuples

    Example:
        Input file with lines like "3,4" returns [(3, 4), ...]
    """
    return [
        tuple(map(int, line.split(separator)))
        for line in read_data_as_lines(data_file)
    ]


def read_data_as_graph_edges(
    data_file: str,
    separator: str = "-",
    directed: bool = False
) -> dict[str, set[str]]:
    """
    Read file with edge list and return adjacency graph representation.

    Args:
        data_file: Path to input file with edges (e.g., "a-b")
        separator: Character separating nodes (default: '-')
        directed: If False, adds edges in both directions (default: False)

    Returns:
        Dictionary mapping each node to its set of neighbors

    Example:
        Input file:
            a-b
            b-c
        Returns: {'a': {'b'}, 'b': {'a', 'c'}, 'c': {'b'}}
    """
    from collections import defaultdict

    graph = defaultdict(set)
    lines = read_data_as_lines(data_file)

    for line in lines:
        node1, node2 = line.split(separator)
        graph[node1].add(node2)
        if not directed:
            graph[node2].add(node1)

    return graph


def read_data_as_sections(data_file: str, strip: bool = True) -> list[str]:
    """
    Read file and split by blank lines into sections.

    Args:
        data_file: Path to input file
        strip: Whether to strip whitespace from sections (default: True)

    Returns:
        List of section strings (split by blank lines)

    Example:
        Input file:
            section 1 line 1
            section 1 line 2

            section 2 line 1
        Returns: ['section 1 line 1\\nsection 1 line 2', 'section 2 line 1']
    """
    content = read_data(data_file)
    sections = content.split("\n\n")
    return [section.strip() for section in sections] if strip else sections


def extract_ints(text: str) -> list[int]:
    """
    Extract all integers (including negative) from text using regex.

    Args:
        text: String to extract integers from

    Returns:
        List of integers found in the text

    Example:
        >>> extract_ints("p=3,4 v=-2,5")
        [3, 4, -2, 5]
    """
    from re import findall
    return list(map(int, findall(r"-?\d+", text)))


def read_data_as_columns(
    data_file: str,
    separator: str | None = None,
    converter: type = int
) -> list[list]:
    """
    Read file with whitespace/delimiter-separated columns and transpose.

    Args:
        data_file: Path to input file
        separator: Column separator (None = whitespace, default)
        converter: Type to convert values to (default: int)

    Returns:
        List of columns (transposed from rows)

    Example:
        Input file:
            1  4
            2  5
            3  6
        Returns: [[1, 2, 3], [4, 5, 6]]
    """
    lines = read_data_as_lines(data_file)
    rows = [list(map(converter, line.split(separator))) for line in lines]
    return list(zip(*rows))  # Transpose


__all__ = [
    "read_data",
    "read_data_as_lines",
    "read_data_as_ints",
    "read_data_as_char_grid",
    "read_data_as_int_grid",
    "read_data_as_coord_pairs",
    "read_data_as_graph_edges",
    "read_data_as_sections",
    "read_data_as_columns",
    "extract_ints",
]
