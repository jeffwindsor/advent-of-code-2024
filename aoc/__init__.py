"""
Advent of Code 2024 Utilities

Organized into modules but accessible from top level for convenience:
- coord: Coordinate class and utilities
- grid: Matrix/grid operations
- graph: Graph algorithms (BFS, DFS, Dijkstra, max clique)
- data: Data reading and parsing
- math: Number/math utilities
- testing: Test framework

Import styles supported:
    # Simple (recommended for puzzles)
    from aoc import Coord, bfs, read_data_as_lines, run, TestCase

    # Explicit (optional for clarity)
    from aoc.coord import Coord
    from aoc.graph import bfs
    from aoc.data import read_data_as_lines
    from aoc.testing import run, TestCase
"""

# Re-export everything for backward compatibility
from .coord import *
from .grid import *
from .graph import *
from .data import *
from .math import *
from .testing import *

# Explicit __all__ for clarity
__all__ = [
    # From coord
    "Coord",
    "filter_coords_in_bounds",
    # From grid
    "Grid",
    "grid_size",
    "grid_max_bounds",
    "grid_contains_coord",
    "grid_get",
    "grid_set",
    "find_first",
    "find_all",
    "grid_coords",
    "search_in_direction",
    "group_by_value",
    "create_visited_grid",
    "create_grid",
    # From graph
    "bfs",
    "dfs",
    "dfs_grid_path",
    "dijkstra",
    "find_max_clique",
    # From data
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
    # From math
    "count_continuous_segments",
    "count_digits",
    # From testing
    "TestCase",
    "run",
]
