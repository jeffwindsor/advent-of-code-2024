from collections import defaultdict
from re import findall
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .grid import Grid

# Input and Parsing Scenarios:
#
#    Single line of integers - as_ints()
#       - Example: "123\n456\n789" → parse each line as single integer
#    Column-based parsing - as_columns()
#       - Example: "3   4\n8   10" → parse aligned columns into separate lists
#    Line-by-line data - as_lines()
#       - Example: "line one\nline two\nline three" → list of string lines
#    Character grid - as_char_grid(), as_grid()
#       - Example: "XMAS\nMASX" → 2D array of characters
#    Numeric grid - as_int_grid()
#       - Example: "0123\n4567\n89.." → 2D array of digits (. becomes -1)
#    Two-part split - as_two_parts()
#       - Example: "section1\ndata\n\nsection2\ndata" → split on blank line into two Parser objects
#    Coordinate pairs - as_coord_pairs()
#       - Example: "6,1\n8,3\n12,5" → list of (x,y) tuples
#    Graph edges - as_graph_edges()
#       - Example: "kh-tc\ntc-wh\nwh-yn" → adjacency dictionary {node: set(neighbors)}
#    Dense single-line string - .content
#       - Example: "2333133121414131402" → raw string for character-by-character processing
#    Key-Value pairs - as_key_value_pairs()
#       - Example: "190: 10 19\n3267: 81 40 27" → parse colon-separated key and values
#    Pipe-separated ordering rules - as_pipe_rules()
#       - Example: "47|53\n97|13\n75|29" → ordering rules dictionary {key: [dependent_values]}
#    Comma-separated values per line - as_csv_lines()
#       - Example: "75,47,61,53,29\n97,61,53,29,13" → list of integer lists per line
#    Multi-pattern regex extractor - as_regex_groups()
#       - Example: "p=100,351 v=-10,25\np=50,100 v=5,-3" → extract regex capture groups from each line
#    Structured integers extractor - as_structured_ints()
#       - Example: "p=100,351 v=-10,25" → extract all integers from complex text: (100, 351, -10, 25)
#    Multi-section split - as_sections()
#       - Example: "sec1\n\nsec2\n\nsec3" → split on blank lines into N Parser objects (generalizes as_two_parts())


def extract_ints(text: str) -> list[int]:
    return list(map(int, findall(r"-?\d+", text)))


class Parser:
    def __init__(self, content: str):
        self._content = content

    @property
    def content(self) -> str:
        return self._content

    def as_lines(self, skip_empty: bool = True) -> list[str]:
        lines = self.content.splitlines()
        if skip_empty:
            return [stripped for line in lines if (stripped := line.strip())]
        return lines

    def as_ints(self) -> list[int]:
        return [int(line) for line in self.as_lines()]

    def as_char_grid(self) -> list[list[str]]:
        return [list(line) for line in self.as_lines()]

    def as_int_grid(self, empty_value: int = -1) -> list[list[int]]:
        return [
            [int(char) if char.isdigit() else empty_value for char in line]
            for line in self.as_lines()
        ]

    def as_grid(self) -> "Grid":
        """
        Parse input as a Grid instance for coordinate-based access.

        Returns:
            Grid instance wrapping character grid
        """
        from .grid import Grid

        return Grid(self.as_char_grid())

    def as_columns(
        self, separator: str | None = None, converter: type = int
    ) -> list[tuple]:
        lines = self.as_lines()
        rows = [list(map(converter, line.split(separator))) for line in lines]
        return list(zip(*rows))

    def as_coord_pairs(self, separator: str = ",") -> list[tuple[int, int]]:
        return [
            (int(x), int(y))
            for x, y in (line.split(separator) for line in self.as_lines())
        ]

    def as_graph_edges(
        self, separator: str = "-", directed: bool = False
    ) -> dict[str, set[str]]:
        graph = defaultdict(set)
        lines = self.as_lines()

        for line in lines:
            node1, node2 = line.split(separator)
            graph[node1].add(node2)
            if not directed:
                graph[node2].add(node1)

        return dict(graph)

    def as_csv_lines(self, separator: str = ",", converter: type = int) -> list[list]:
        """
        Parse each line as comma-separated values.

        Args:
            separator: Delimiter between values (default: ",")
            converter: Type function to apply to each value (default: int)

        Returns:
            List of lists, one per line with converted values

        Examples:
            Default usage (comma-separated integers):
            >>> parser = Parser("75,47,61\\n97,61,53\\n75,29")
            >>> parser.as_csv_lines()
            [[75, 47, 61], [97, 61, 53], [75, 29]]

            Custom separator:
            >>> parser = Parser("1;2;3\\n4;5;6")
            >>> parser.as_csv_lines(separator=";")
            [[1, 2, 3], [4, 5, 6]]

            String values:
            >>> parser = Parser("a,b,c\\nx,y,z")
            >>> parser.as_csv_lines(converter=str)
            [['a', 'b', 'c'], ['x', 'y', 'z']]

            Float values:
            >>> parser = Parser("1.5,2.7\\n3.2,4.8")
            >>> parser.as_csv_lines(converter=float)
            [[1.5, 2.7], [3.2, 4.8]]
        """
        return [list(map(converter, line.split(separator))) for line in self.as_lines()]

    def as_key_value_pairs(
        self,
        key_type: type = int,
        value_parser=None,
        separator: str = ":",
    ) -> list[tuple]:
        """
        Parse lines with "key: value" format.

        Args:
            key_type: Type function for key (default: int)
            value_parser: Function to parse value side (default: extract_ints)
            separator: Delimiter between key and value (default: ":")

        Returns:
            List of tuples: [(key, parsed_value), ...]

        Examples:
            Default usage (key as int, values as list of ints):
            >>> parser = Parser("190: 10 19\\n3267: 81 40 27")
            >>> parser.as_key_value_pairs()
            [(190, [10, 19]), (3267, [81, 40, 27])]

            Custom value parser:
            >>> parser = Parser("test: hello world\\nfoo: bar baz")
            >>> parser.as_key_value_pairs(key_type=str, value_parser=str.split)
            [('test', ['hello', 'world']), ('foo', ['bar', 'baz'])]

            Single value per key:
            >>> parser = Parser("x: 42\\ny: 99")
            >>> parser.as_key_value_pairs(value_parser=int)
            [('x', 42), ('y', 99)]
        """
        if value_parser is None:
            value_parser = extract_ints

        result = []
        for line in self.as_lines():
            key_str, value_str = line.split(separator, 1)
            key = key_type(key_str.strip())
            value = value_parser(value_str.strip())
            result.append((key, value))

        return result

    def as_structured_ints(self, ints_per_line: int) -> list[tuple[int, ...]]:
        """
        Extract all integers from each line using extract_ints().

        Args:
            ints_per_line: Expected number of integers per line (for validation)

        Returns:
            List of tuples, one per line with extracted integers

        Raises:
            ValueError: If any line doesn't have exactly ints_per_line integers

        Examples:
            Position/velocity format:
            >>> parser = Parser("p=0,4 v=3,-3\\np=6,3 v=-1,-3")
            >>> parser.as_structured_ints(4)
            [(0, 4, 3, -3), (6, 3, -1, -3)]

            Coordinates with metadata:
            >>> parser = Parser("x=10 y=20 id=1\\nx=30 y=40 id=2")
            >>> parser.as_structured_ints(3)
            [(10, 20, 1), (30, 40, 2)]

            Negative numbers supported:
            >>> parser = Parser("p=100,351 v=-10,25")
            >>> parser.as_structured_ints(4)
            [(100, 351, -10, 25)]
        """
        result = []
        for line_num, line in enumerate(self.as_lines(), 1):
            ints = extract_ints(line)
            if len(ints) != ints_per_line:
                raise ValueError(
                    f"Line {line_num}: expected {ints_per_line} integers, got {len(ints)}: {line}"
                )
            result.append(tuple(ints))

        return result

    def as_sections(self, strip: bool = True) -> list["Parser"]:
        """
        Split input into multiple sections separated by blank lines.

        Args:
            strip: Whether to strip whitespace from each section (default: True)

        Returns:
            List of Parser instances, one for each section

        Examples:
            Two sections:
            >>> parser = Parser("section1\\ndata\\n\\nsection2\\nmore")
            >>> sections = parser.as_sections()
            >>> len(sections)
            2

            Three sections:
            >>> parser = Parser("sec1\\n\\nsec2\\n\\nsec3")
            >>> sections = parser.as_sections()
            >>> [s.content for s in sections]
            ['sec1', 'sec2', 'sec3']

            With whitespace preservation:
            >>> parser = Parser("  a  \\n\\n  b  ")
            >>> sections = parser.as_sections(strip=False)
            >>> sections[0].content
            '  a  '
        """
        parts = self.content.split("\n\n")
        return [Parser(s.strip() if strip else s) for s in parts]

    def as_pipe_rules(self, separator: str = "|") -> dict[int, list[int]]:
        """
        Parse ordering/dependency rules in "X|Y" format.

        Args:
            separator: Delimiter between rule parts (default: "|")

        Returns:
            Dictionary mapping each key to list of dependent values

        Examples:
            Ordering rules:
            >>> parser = Parser("47|53\\n97|13\\n97|61")
            >>> parser.as_pipe_rules()
            {47: [53], 97: [13, 61]}

            Custom separator:
            >>> parser = Parser("A->B\\nA->C\\nB->D")
            >>> parser.as_pipe_rules(separator="->")
            {'A': ['B', 'C'], 'B': ['D']}

            All rules in dict form:
            >>> parser = Parser("1|2\\n1|3\\n2|4")
            >>> rules = parser.as_pipe_rules()
            >>> rules[1]
            [2, 3]
        """
        rules = defaultdict(list)
        for line in self.as_lines():
            key, value = line.split(separator)
            # Try to convert to int, fall back to string
            try:
                key = int(key.strip())
                value = int(value.strip())
            except ValueError:
                key = key.strip()
                value = value.strip()
            rules[key].append(value)

        return dict(rules)

    def as_regex_groups(self, pattern: str) -> list[tuple]:
        """
        Extract regex capture groups from each line.

        Args:
            pattern: Regular expression pattern with capture groups

        Returns:
            List of tuples containing captured groups from each line

        Examples:
            Position/velocity with named structure:
            >>> parser = Parser("p=0,4 v=3,-3\\np=6,3 v=-1,-3")
            >>> parser.as_regex_groups(r"p=(-?\\d+),(-?\\d+) v=(-?\\d+),(-?\\d+)")
            [('0', '4', '3', '-3'), ('6', '3', '-1', '-3')]

            Extract words:
            >>> parser = Parser("name: Alice age: 25\\nname: Bob age: 30")
            >>> parser.as_regex_groups(r"name: (\\w+) age: (\\d+)")
            [('Alice', '25'), ('Bob', '30')]

            Multiple patterns per line:
            >>> parser = Parser("move 3 from 1 to 2\\nmove 5 from 3 to 1")
            >>> parser.as_regex_groups(r"move (\\d+) from (\\d+) to (\\d+)")
            [('3', '1', '2'), ('5', '3', '1')]
        """
        from re import search

        result = []
        for line in self.as_lines():
            match = search(pattern, line)
            if match:
                result.append(match.groups())

        return result


class Input:
    def __init__(self, data_file: str):
        self._data_file = data_file
        self._parser: Parser | None = None

    @property
    def parser(self) -> Parser:
        if self._parser is None:
            with open(self._data_file, "r") as f:
                self._parser = Parser(f.read().strip())
        return self._parser

    @property
    def content(self) -> str:
        return self.parser.content

    def as_lines(self, skip_empty: bool = True) -> list[str]:
        return self.parser.as_lines(skip_empty)

    def as_ints(self) -> list[int]:
        return self.parser.as_ints()

    def as_two_parts(self, strip: bool = True) -> tuple["Parser", "Parser"]:
        parts = [Parser(s.strip() if strip else s) for s in self.content.split("\n\n")]
        return (parts[0], parts[1])

    def as_char_grid(self) -> list[list[str]]:
        return self.parser.as_char_grid()

    def as_int_grid(self, empty_value: int = -1) -> list[list[int]]:
        return self.parser.as_int_grid(empty_value)

    def as_grid(self) -> "Grid":
        """
        Parse input as a Grid instance for coordinate-based access.

        Returns:
            Grid instance wrapping character grid
        """
        return self.parser.as_grid()

    def as_columns(
        self, separator: str | None = None, converter: type = int
    ) -> list[tuple]:
        return self.parser.as_columns(separator, converter)

    def as_coord_pairs(self, separator: str = ",") -> list[tuple[int, int]]:
        return self.parser.as_coord_pairs(separator)

    def as_graph_edges(
        self, separator: str = "-", directed: bool = False
    ) -> dict[str, set[str]]:
        return self.parser.as_graph_edges(separator, directed)

    def as_csv_lines(self, separator: str = ",", converter: type = int) -> list[list]:
        return self.parser.as_csv_lines(separator, converter)

    def as_key_value_pairs(
        self,
        key_type: type = int,
        value_parser=None,
        separator: str = ":",
    ) -> list[tuple]:
        return self.parser.as_key_value_pairs(key_type, value_parser, separator)

    def as_structured_ints(self, ints_per_line: int) -> list[tuple[int, ...]]:
        return self.parser.as_structured_ints(ints_per_line)

    def as_sections(self, strip: bool = True) -> list["Parser"]:
        return self.parser.as_sections(strip)

    def as_pipe_rules(self, separator: str = "|") -> dict[int, list[int]]:
        return self.parser.as_pipe_rules(separator)

    def as_regex_groups(self, pattern: str) -> list[tuple]:
        return self.parser.as_regex_groups(pattern)


__all__ = ["Input", "Parser", "extract_ints"]
