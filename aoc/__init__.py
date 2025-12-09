"""
Advent of Code 2024 Utilities

Organized into modules but accessible from top level for convenience:
- coord: Coordinate class and utilities
- grid: Matrix/grid operations
- graph: Graph algorithms (BFS, DFS, Dijkstra, max clique)
- input: Data reading and parsing (Input and Parser classes)
- math: Number/math utilities
- testing: Test framework

Import styles supported:
    # Simple (recommended for puzzles)
    from aoc import Coord, bfs, Input, run, TestCase

    # Explicit (optional for clarity)
    from aoc.coord import Coord
    from aoc.graph import bfs
    from aoc.input import Input, Parser
    from aoc.testing import run, TestCase
"""

# Re-export everything for backward compatibility
from .coord import *
from .grid import *
from .graph import *
from .input import *
from .math import *
from .testing import *

# Explicit __all__ for clarity
__all__ = [
    # From coord
    "Coord",
    "filter_coords_in_bounds",
    # From grid
    "Grid",
    # From graph
    "bfs",
    "dfs",
    "bfs_grid_path",
    "dfs_grid_path",
    "dijkstra",
    "find_max_clique",
    # From input
    "Input",
    "Parser",
    "extract_ints",
    "extract_pattern",
    # From math
    "count_continuous_segments",
    "count_digits",
    # From testing
    "TestCase",
    "run",
]
