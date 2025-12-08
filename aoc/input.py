from collections import defaultdict
from re import findall


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


__all__ = ["Input", "Parser", "extract_ints"]
