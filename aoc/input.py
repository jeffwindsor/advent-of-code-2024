from collections import defaultdict
from re import findall


class Input:
    def __init__(self, data_file: str):
        self._data_file = data_file
        self._content: str | None = None

    @property
    def content(self) -> str:
        if self._content is None:
            with open(self._data_file, "r") as f:
                self._content = f.read().strip()
        return self._content

    def as_lines(self, skip_empty: bool = True) -> list[str]:
        lines = self.content.splitlines()
        if skip_empty:
            return [stripped for line in lines if (stripped := line.strip())]
        return lines

    def as_ints(self) -> list[int]:
        return [int(line) for line in self.as_lines()]

    def as_sections(self, strip: bool = True) -> list[str]:
        sections = self.content.split("\n\n")
        return [section.strip() for section in sections] if strip else sections

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
        return [(int(x), int(y)) for x, y in (line.split(separator) for line in self.as_lines())]

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

    @staticmethod
    def extract_ints(text: str) -> list[int]:
        return list(map(int, findall(r"-?\d+", text)))


__all__ = ["Input"]
