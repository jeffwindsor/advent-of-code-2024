"""
Tests for aoc.input parsers.

Run with: python -m pytest tests/test_input_parsers.py
Or simply: python tests/test_input_parsers.py
"""

import tempfile
import unittest
from pathlib import Path

from aoc import Input, extract_ints, extract_pattern, Coord




class TestPrimitives(unittest.TestCase):
    """Tests for composable primitive methods."""

    def test_parse_sections_default(self):
        """Test parse with section separator."""
        parser = Input.from_string("a\n\nb\n\nc")
        sections = parser.parse(parser._section_sep)

        self.assertEqual(sections, ['a', 'b', 'c'])
        self.assertIsInstance(sections, list)
        self.assertIsInstance(sections[0], str)

    def test_parse_sections_custom_separator(self):
        """Test parse with custom section separator."""
        parser = Input.from_string("a===b===c", section_sep="===")
        sections = parser.parse(parser._section_sep)

        self.assertEqual(sections, ['a', 'b', 'c'])

    def test_parse_sections_override_separator(self):
        """Test parse with method-level separator override."""
        parser = Input.from_string("a\n\nb|||c", section_sep="\n\n")
        sections = parser.parse("|||")

        self.assertEqual(sections, ['a\n\nb', 'c'])

    def test_parse_empty_separator_returns_char_array(self):
        """Test parse returns character array for empty separator."""
        parser = Input.from_string("abc")
        result = parser.parse("")

        self.assertEqual(result, ['a', 'b', 'c'])

    def test_parse_lines_default(self):
        """Test parse with line separator."""
        parser = Input.from_string("a\nb\nc")
        lines = parser.parse(parser._line_sep)

        self.assertEqual(lines, ['a', 'b', 'c'])

    def test_parse_lines_custom_separator(self):
        """Test parse with custom line separator."""
        parser = Input.from_string("a;b;c", line_sep=";")
        lines = parser.parse(parser._line_sep)

        self.assertEqual(lines, ['a', 'b', 'c'])

    def test_parse_lines_skip_empty(self):
        """Test parse skips empty lines."""
        parser = Input.from_string("a\n\nb\n  \nc")
        lines = parser.parse(parser._line_sep, skip_empty=True)

        self.assertEqual(lines, ['a', 'b', 'c'])

    def test_parse_lines_keep_empty(self):
        """Test parse keeps empty lines."""
        parser = Input.from_string("a\n\nb")
        lines = parser.parse(parser._line_sep, skip_empty=False)

        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[1], '')

    def test_parse_none_separator_returns_char_array(self):
        """Test parse returns character array for None separator."""
        parser = Input.from_string("hello")
        result = parser.parse(None)

        self.assertEqual(result, ['h', 'e', 'l', 'l', 'o'])

    def test_extract_ints_default(self):
        """Test extract_ints with default pattern."""
        result = extract_ints("x=10 y=-5 z=3")

        self.assertEqual(result, [10, -5, 3])
        self.assertIsInstance(result[0], int)

    def test_extract_ints_custom_pattern(self):
        """Test extract_ints with custom pattern."""
        result = extract_ints("values: 1.5, 2.7", pattern=r"\d+")

        self.assertEqual(result, [1, 5, 2, 7])

    def test_extract_ints_negative_numbers(self):
        """Test extract_ints handles negative numbers."""
        result = extract_ints("p=100,351 v=-10,25")

        self.assertEqual(result, [100, 351, -10, 25])

    def test_extract_ints_invalid_pattern(self):
        """Test extract_ints raises error for invalid regex."""
        with self.assertRaises(ValueError) as context:
            extract_ints("text", pattern="[invalid")

        self.assertIn("Invalid regex pattern", str(context.exception))

    def test_extract_pattern_simple(self):
        """Test extract_pattern with simple pattern."""
        result = extract_pattern("a1 b2 c3", r"[a-z]\d")

        self.assertEqual(result, ['a1', 'b2', 'c3'])

    def test_extract_pattern_floats(self):
        """Test extract_pattern for float numbers."""
        result = extract_pattern("x=1.5 y=-2.7", r"-?\d+\.\d+")

        self.assertEqual(result, ['1.5', '-2.7'])

    def test_extract_pattern_invalid_regex(self):
        """Test extract_pattern raises error for invalid regex."""
        with self.assertRaises(ValueError) as context:
            extract_pattern("text", r"[unclosed")

        self.assertIn("Invalid regex pattern", str(context.exception))


class TestCustomSeparators(unittest.TestCase):
    """Tests for custom separator configuration."""

    def test_parser_with_custom_line_separator(self):
        """Test Parser with custom line separator."""
        parser = Input.from_string("a;b;c", line_sep=";")
        lines = parser.parse(parser._line_sep)

        self.assertEqual(lines, ['a', 'b', 'c'])

    def test_parser_with_custom_section_separator(self):
        """Test Parser with custom section separator."""
        parser = Input.from_string("a===b===c", section_sep="===")
        sections = parser.parse(parser._section_sep)

        self.assertEqual(sections, ['a', 'b', 'c'])

    def test_parser_with_both_custom_separators(self):
        """Test Parser with both separators customized."""
        parser = Input.from_string("a;b===c;d", line_sep=";", section_sep="===")
        sections = parser.parse(parser._section_sep)

        self.assertEqual(len(sections), 2)

        # Parse first section lines
        section1 = Input.from_string(sections[0], line_sep=";")
        self.assertEqual(section1.parse(section1._line_sep), ['a', 'b'])

    def test_as_sections_preserves_separators(self):
        """Test as_sections() creates Parsers with same separators."""
        parser = Input.from_string("a;b===c;d", line_sep=";", section_sep="===")
        section_parsers = parser.as_sections()

        # Child parsers should inherit separator config
        self.assertEqual(section_parsers[0].parse(section_parsers[0]._line_sep), ['a', 'b'])
        self.assertEqual(section_parsers[1].parse(section_parsers[1]._line_sep), ['c', 'd'])


class TestComposition(unittest.TestCase):
    """Tests for composing primitives to create custom parsers."""

    def test_custom_multi_level_parsing(self):
        """Test composing primitives for multi-level parsing."""
        content = "1,2===3,4===5,6"
        parser = Input.from_string(content, section_sep="===")

        result = []
        for section_str in parser.parse(parser._section_sep):
            values = [int(v) for v in section_str.split(",")]
            result.append(values)

        self.assertEqual(result, [[1, 2], [3, 4], [5, 6]])

    def test_custom_conditional_parsing(self):
        """Test using primitives with conditional logic."""
        content = "coord: 10,20\nname: test\nvalues: 1.5,2.7"
        parser = Input.from_string(content)

        data = []
        for line in parser.parse(parser._line_sep):
            if line.startswith("coord:"):
                coords = extract_ints(line[6:])
                data.append(("coord", tuple(coords)))
            elif line.startswith("name:"):
                name = line[5:].strip()
                data.append(("name", name))
            elif line.startswith("values:"):
                values = [float(v) for v in line[7:].split(",")]
                data.append(("values", values))

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], ("coord", (10, 20)))
        self.assertEqual(data[1], ("name", "test"))
        self.assertEqual(data[2], ("values", [1.5, 2.7]))

    def test_extract_then_convert(self):
        """Test extracting patterns then converting."""
        # Extract float pattern
        float_str = extract_pattern("temperature: 72.5F", r"\d+\.\d+")[0]
        temp = float(float_str)

        # Extract int pattern
        int_str = extract_pattern("humidity: 45%", r"\d+")[0]
        humidity = int(int_str)

        self.assertEqual(temp, 72.5)
        self.assertEqual(humidity, 45)


class TestCSVLinesInput(unittest.TestCase):
    """Tests for the as_delimited_lines() parser method."""

    def test_default_comma_separated_integers(self):
        """Test parsing comma-separated integers (default behavior)."""
        parser = Input.from_string("75,47,61,53,29\n97,61,53,29,13\n75,29,13")
        result = parser.as_delimited_lines()

        expected = [[75, 47, 61, 53, 29], [97, 61, 53, 29, 13], [75, 29, 13]]
        self.assertEqual(result, expected)

        # Verify types
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], int)

    def test_custom_separator_semicolon(self):
        """Test parsing with custom separator (semicolon)."""
        parser = Input.from_string("1;2;3\n4;5;6\n7;8;9")
        result = parser.as_delimited_lines(separator=";")

        expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result, expected)

    def test_custom_separator_pipe(self):
        """Test parsing with pipe separator."""
        parser = Input.from_string("10|20|30\n40|50|60")
        result = parser.as_delimited_lines(separator="|")

        expected = [[10, 20, 30], [40, 50, 60]]
        self.assertEqual(result, expected)

    def test_string_converter(self):
        """Test parsing with string converter."""
        parser = Input.from_string("a,b,c\nx,y,z\nfoo,bar,baz")
        result = parser.as_delimited_lines(converter=str)

        expected = [['a', 'b', 'c'], ['x', 'y', 'z'], ['foo', 'bar', 'baz']]
        self.assertEqual(result, expected)

        # Verify all values are strings
        for row in result:
            for val in row:
                self.assertIsInstance(val, str)

    def test_float_converter(self):
        """Test parsing with float converter."""
        parser = Input.from_string("1.5,2.7,3.9\n4.2,5.8,6.1")
        result = parser.as_delimited_lines(converter=float)

        expected = [[1.5, 2.7, 3.9], [4.2, 5.8, 6.1]]
        self.assertEqual(result, expected)

        # Verify types
        self.assertIsInstance(result[0][0], float)

    def test_single_value_per_line(self):
        """Test parsing lines with single values."""
        parser = Input.from_string("100\n200\n300")
        result = parser.as_delimited_lines()

        expected = [[100], [200], [300]]
        self.assertEqual(result, expected)

    def test_empty_lines_skipped(self):
        """Test that empty lines are skipped (via as_lines behavior)."""
        parser = Input.from_string("1,2,3\n\n4,5,6\n\n7,8,9")
        result = parser.as_delimited_lines()

        expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result, expected)

    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is handled."""
        parser = Input.from_string("  1,2,3  \n  4,5,6  ")
        result = parser.as_delimited_lines()

        expected = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(result, expected)

    def test_variable_length_rows(self):
        """Test parsing rows with different numbers of values."""
        parser = Input.from_string("1,2,3,4,5\n6,7\n8,9,10")
        result = parser.as_delimited_lines()

        expected = [[1, 2, 3, 4, 5], [6, 7], [8, 9, 10]]
        self.assertEqual(result, expected)

    def test_with_input_class(self):
        """Test as_delimited_lines() via Input class delegation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("10,20,30\n40,50,60")
            temp_path = f.name

        try:
            result = Input(temp_path).as_delimited_lines()
            expected = [[10, 20, 30], [40, 50, 60]]
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()

    def test_day5_format(self):
        """Test with actual Day 5 puzzle data format (page updates)."""
        # Simulate Day 5 page updates section
        parser = Input.from_string("75,47,61,53,29\n97,61,53,29,13\n75,29,13")
        result = parser.as_delimited_lines()

        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 5)  # First update has 5 pages
        self.assertEqual(result[0][0], 75)

    def test_day18_format(self):
        """Test with actual Day 18 puzzle data format (coordinate pairs)."""
        # Simulate Day 18 coordinate format
        parser = Input.from_string("5,4\n4,2\n4,5\n3,0\n2,1")
        result = parser.as_delimited_lines()

        self.assertEqual(len(result), 5)
        self.assertEqual(len(result[0]), 2)  # Each coordinate has 2 values
        self.assertEqual(result[0], [5, 4])
        self.assertEqual(result[1], [4, 2])




class TestKeyValuePairsInput(unittest.TestCase):
    """Tests for the as_key_value_pairs() parser method."""

    def test_default_key_value_with_int_lists(self):
        """Test parsing key:value format with default behavior (int key, int list values)."""
        parser = Input.from_string("190: 10 19\n3267: 81 40 27\n83: 17 5")
        result = parser.as_key_value_pairs()

        expected = [(190, [10, 19]), (3267, [81, 40, 27]), (83, [17, 5])]
        self.assertEqual(result, expected)

        # Verify types
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], int)  # Key
        self.assertIsInstance(result[0][1], list)  # Value list

    def test_custom_separator(self):
        """Test with custom separator (equals sign)."""
        parser = Input.from_string("x = 1 2 3\ny = 4 5 6")
        result = parser.as_key_value_pairs(key_converter=str, separator="=")

        expected = [('x', [1, 2, 3]), ('y', [4, 5, 6])]
        self.assertEqual(result, expected)

    def test_string_keys(self):
        """Test with string keys instead of integers."""
        parser = Input.from_string("test: 10 20\nfoo: 30 40")
        result = parser.as_key_value_pairs(key_converter=str)

        expected = [('test', [10, 20]), ('foo', [30, 40])]
        self.assertEqual(result, expected)
        self.assertIsInstance(result[0][0], str)

    def test_single_value_parser(self):
        """Test with custom value parser that returns single value."""
        parser = Input.from_string("x: 42\ny: 99\nz: 123")
        result = parser.as_key_value_pairs(key_converter=str, value_parser=int)

        expected = [('x', 42), ('y', 99), ('z', 123)]
        self.assertEqual(result, expected)
        self.assertIsInstance(result[0][1], int)  # Single int, not list

    def test_custom_value_parser(self):
        """Test with custom value parser (split on spaces)."""
        parser = Input.from_string("test: hello world\nfoo: bar baz qux")
        result = parser.as_key_value_pairs(
            key_converter=str,
            value_parser=str.split
        )

        expected = [('test', ['hello', 'world']), ('foo', ['bar', 'baz', 'qux'])]
        self.assertEqual(result, expected)
        self.assertIsInstance(result[0][1][0], str)

    def test_whitespace_handling(self):
        """Test that whitespace around separator is handled."""
        parser = Input.from_string("  100:  5 10 15  \n  200:  20 25  ")
        result = parser.as_key_value_pairs()

        expected = [(100, [5, 10, 15]), (200, [20, 25])]
        self.assertEqual(result, expected)

    def test_variable_value_lengths(self):
        """Test keys with different numbers of values."""
        parser = Input.from_string("1: 10\n2: 20 30\n3: 40 50 60 70")
        result = parser.as_key_value_pairs()

        expected = [(1, [10]), (2, [20, 30]), (3, [40, 50, 60, 70])]
        self.assertEqual(result, expected)

    def test_with_input_class(self):
        """Test as_key_value_pairs() via Input class delegation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("100: 1 2 3\n200: 4 5 6")
            temp_path = f.name

        try:
            result = Input(temp_path).as_key_value_pairs()
            expected = [(100, [1, 2, 3]), (200, [4, 5, 6])]
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()


class TestKeyValuePairsIntegration(unittest.TestCase):
    """Integration tests for key-value pairs parsing scenarios."""

    def test_key_value_pairs_with_lists(self):
        """Integration test: Key-value pairs with multiple integer values per key."""
        result = Input("tests/data/test_key_value_pairs_with_lists").as_key_value_pairs()

        # Verify we got valid data
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], tuple)

        # Each tuple should have (int_key, list_of_ints)
        for key, values in result:
            self.assertIsInstance(key, int)
            self.assertIsInstance(values, list)
            for val in values:
                self.assertIsInstance(val, int)

        # Verify expected data (from Day 7 example)
        self.assertEqual(result[0], (190, [10, 19]))
        self.assertEqual(result[1], (3267, [81, 40, 27]))


class TestSectionsInput(unittest.TestCase):
    """Tests for the as_sections() parser method."""

    def test_two_sections(self):
        """Test splitting input into two sections."""
        parser = Input.from_string("section1\ndata\n\nsection2\nmore")
        sections = parser.as_sections()

        self.assertEqual(len(sections), 2)
        self.assertIsInstance(sections[0], Input)
        self.assertEqual(sections[0].content, "section1\ndata")
        self.assertEqual(sections[1].content, "section2\nmore")

    def test_three_sections(self):
        """Test splitting input into three sections."""
        parser = Input.from_string("sec1\n\nsec2\n\nsec3")
        sections = parser.as_sections()

        self.assertEqual(len(sections), 3)
        contents = [s.content for s in sections]
        self.assertEqual(contents, ['sec1', 'sec2', 'sec3'])

    def test_four_sections(self):
        """Test splitting input into four sections."""
        parser = Input.from_string("a\n\nb\n\nc\n\nd")
        sections = parser.as_sections()

        self.assertEqual(len(sections), 4)

    def test_single_section(self):
        """Test input with no blank lines (single section)."""
        parser = Input.from_string("line1\nline2\nline3")
        sections = parser.as_sections()

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].content, "line1\nline2\nline3")

    def test_whitespace_stripping(self):
        """Test that whitespace is stripped by default."""
        parser = Input.from_string("  section1  \n\n  section2  ")
        sections = parser.as_sections()

        self.assertEqual(sections[0].content, "section1")
        self.assertEqual(sections[1].content, "section2")

    def test_whitespace_preservation(self):
        """Test whitespace preservation when strip=False."""
        parser = Input.from_string("  section1  \n\n  section2  ")
        sections = parser.as_sections(strip=False)

        self.assertEqual(sections[0].content, "  section1  ")
        self.assertEqual(sections[1].content, "  section2  ")

    def test_sections_are_parsers(self):
        """Test that each section is a Parser with full functionality."""
        parser = Input.from_string("1,2,3\n4,5,6\n\n7,8,9")
        sections = parser.as_sections()

        # First section can be parsed as CSV
        csv_data = sections[0].as_delimited_lines()
        self.assertEqual(csv_data, [[1, 2, 3], [4, 5, 6]])

        # Second section can also be parsed
        csv_data2 = sections[1].as_delimited_lines()
        self.assertEqual(csv_data2, [[7, 8, 9]])

    def test_with_input_class(self):
        """Test as_sections() via Input class delegation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("part1\n\npart2\n\npart3")
            temp_path = f.name

        try:
            sections = Input(temp_path).as_sections()
            self.assertEqual(len(sections), 3)
            self.assertEqual(sections[0].content, "part1")
        finally:
            Path(temp_path).unlink()


class TestSectionsIntegration(unittest.TestCase):
    """Integration tests for multi-section parsing scenarios."""

    def test_sections_three_parts(self):
        """Integration test: Split input into three distinct sections."""
        sections = Input("tests/data/test_sections_three_parts").as_sections()

        # Verify we got exactly 3 sections
        self.assertEqual(len(sections), 3)

        # All sections should be Parser instances
        for section in sections:
            self.assertIsInstance(section, Input)

        # First section should have header and 2 data lines
        lines1 = sections[0].as_lines()
        self.assertEqual(len(lines1), 3)
        self.assertIn("Section 1", lines1[0])

        # Second section
        lines2 = sections[1].as_lines()
        self.assertEqual(len(lines2), 3)
        self.assertIn("Section 2", lines2[0])

        # Third section
        lines3 = sections[2].as_lines()
        self.assertEqual(len(lines3), 3)
        self.assertIn("Section 3", lines3[0])


class TestGridMethods(unittest.TestCase):
    """Tests for grid-related parsing methods."""

    def test_as_grid_basic(self):
        """Test as_grid with simple input."""
        from aoc import Coord, Grid
        parser = Input.from_string("ABC\nDEF\nGHI")
        result = parser.as_grid()

        self.assertIsInstance(result, Grid)
        self.assertEqual(result.size.height, 3)
        self.assertEqual(result.size.width, 3)
        self.assertEqual(result[Coord(0, 0)], 'A')
        self.assertEqual(result[Coord(1, 1)], 'E')
        self.assertEqual(result[Coord(2, 2)], 'I')

    def test_as_grid_variable_width(self):
        """Test as_grid with variable line lengths."""
        from aoc import Grid
        parser = Input.from_string("AB\nDEF\nG")
        result = parser.as_grid()

        self.assertIsInstance(result, Grid)
        self.assertEqual(result.size.height, 3)

    def test_as_grid_single_line(self):
        """Test as_grid with single line."""
        from aoc import Coord, Grid
        parser = Input.from_string("HELLO")
        result = parser.as_grid()

        self.assertIsInstance(result, Grid)
        self.assertEqual(result.size.height, 1)
        self.assertEqual(result[Coord(0, 0)], 'H')
        self.assertEqual(result[Coord(0, 4)], 'O')

    def test_as_int_grid_basic(self):
        """Test as_int_grid with digit characters."""
        from aoc import Coord, Grid
        parser = Input.from_string("012\n345\n678")
        result = parser.as_int_grid()

        self.assertIsInstance(result, Grid)
        self.assertEqual(result.size.height, 3)
        self.assertEqual(result.size.width, 3)
        self.assertEqual(result[Coord(0, 0)], 0)
        self.assertEqual(result[Coord(1, 1)], 4)
        self.assertEqual(result[Coord(2, 2)], 8)

    def test_as_int_grid_with_non_digits(self):
        """Test as_int_grid with non-digit characters using default empty_value."""
        from aoc import Coord, Grid
        parser = Input.from_string("0.2\n3.5\n6.8")
        result = parser.as_int_grid()

        self.assertIsInstance(result, Grid)
        self.assertEqual(result[Coord(0, 0)], 0)
        self.assertEqual(result[Coord(0, 1)], -1)  # default empty_value
        self.assertEqual(result[Coord(0, 2)], 2)

    def test_as_int_grid_custom_empty_value(self):
        """Test as_int_grid with custom empty_value."""
        from aoc import Coord, Grid
        parser = Input.from_string("1.3\n4.6")
        result = parser.as_int_grid(empty_value=0)

        self.assertEqual(result[Coord(0, 1)], 0)  # custom empty_value

    def test_as_int_grid_single_line(self):
        """Test as_int_grid with single line."""
        from aoc import Coord, Grid
        parser = Input.from_string("12345")
        result = parser.as_int_grid()

        self.assertIsInstance(result, Grid)
        self.assertEqual(result.size.height, 1)
        self.assertEqual(result[Coord(0, 0)], 1)
        self.assertEqual(result[Coord(0, 4)], 5)


class TestColumnsMethods(unittest.TestCase):
    """Tests for as_columns parsing method."""

    def test_as_columns_basic(self):
        """Test as_columns with default whitespace separator."""
        parser = Input.from_string("1 2 3\n4 5 6\n7 8 9")
        result = parser.as_columns()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)  # 3 columns
        self.assertEqual(result[0], (1, 4, 7))  # First column
        self.assertEqual(result[1], (2, 5, 8))  # Second column
        self.assertEqual(result[2], (3, 6, 9))  # Third column

    def test_as_columns_custom_separator(self):
        """Test as_columns with custom separator."""
        parser = Input.from_string("1,2,3\n4,5,6")
        result = parser.as_columns(separator=",")

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (1, 4))
        self.assertEqual(result[1], (2, 5))
        self.assertEqual(result[2], (3, 6))

    def test_as_columns_two_columns(self):
        """Test as_columns with two columns (common AOC pattern)."""
        parser = Input.from_string("3   4\n8   10\n5   9")
        result = parser.as_columns(separator="   ")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (3, 8, 5))
        self.assertEqual(result[1], (4, 10, 9))

    def test_as_columns_single_column(self):
        """Test as_columns with single column."""
        parser = Input.from_string("1\n2\n3")
        result = parser.as_columns()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (1, 2, 3))


class TestCoordPairsMethods(unittest.TestCase):
    """Tests for as_coord_pairs parsing method."""

    def test_as_coords_basic(self):
        """Test as_coords with comma-separated pairs."""
        parser = Input.from_string("5,4\n4,2\n3,1")
        result = parser.as_coords()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], Coord(5, 4))
        self.assertEqual(result[1], Coord(4, 2))
        self.assertEqual(result[2], Coord(3, 1))

    def test_as_coords_custom_separator(self):
        """Test as_coords with custom separator."""
        parser = Input.from_string("10:20\n30:40")
        result = parser.as_coords(separator=":")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], Coord(10, 20))
        self.assertEqual(result[1], Coord(30, 40))

    def test_as_coords_negative_values(self):
        """Test as_coords with negative coordinates."""
        parser = Input.from_string("-5,10\n20,-30")
        result = parser.as_coords()

        self.assertEqual(result[0], Coord(-5, 10))
        self.assertEqual(result[1], Coord(20, -30))

    def test_as_coords_single_pair(self):
        """Test as_coords with single coordinate pair."""
        parser = Input.from_string("100,200")
        result = parser.as_coords()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], Coord(100, 200))


class TestGraphEdgesMethods(unittest.TestCase):
    """Tests for as_graph_edges parsing method."""

    def test_as_adjacency_list_bidirectional_default(self):
        """Test as_adjacency_list with default bidirectional edges."""
        parser = Input.from_string("a-b\nc-d")
        result = parser.as_adjacency_list()

        self.assertIsInstance(result, dict)
        # Bidirectional: both directions should exist
        self.assertIn('b', result['a'])
        self.assertIn('a', result['b'])
        self.assertIn('d', result['c'])
        self.assertIn('c', result['d'])

    def test_as_adjacency_list_directional(self):
        """Test as_adjacency_list with directional edges."""
        parser = Input.from_string("a-b\nc-d")
        result = parser.as_adjacency_list(directed=True)

        self.assertIsInstance(result, dict)
        # Directional: only one direction
        self.assertIn('b', result['a'])
        self.assertNotIn('a', result.get('b', set()))

    def test_as_adjacency_list_custom_separator(self):
        """Test as_adjacency_list with custom separator."""
        parser = Input.from_string("a:b\nc:d")
        result = parser.as_adjacency_list(separator=":")

        self.assertIn('b', result['a'])
        self.assertIn('a', result['b'])

    def test_as_adjacency_list_multiple_connections(self):
        """Test as_adjacency_list with multiple connections to same node."""
        parser = Input.from_string("a-b\na-c\na-d")
        result = parser.as_adjacency_list()

        self.assertEqual(len(result['a']), 3)
        self.assertIn('b', result['a'])
        self.assertIn('c', result['a'])
        self.assertIn('d', result['a'])


class TestCSVLinesIntegration(unittest.TestCase):
    """Integration tests for CSV line parsing scenarios."""

    def test_csv_multi_values_per_line(self):
        """Integration test: Multiple comma-separated values per line (variable length)."""
        section1, section2 = Input("tests/data/test_csv_multi_values_per_line").as_sections()
        page_updates = section2.as_delimited_lines()

        # Verify we got valid data
        self.assertIsInstance(page_updates, list)
        self.assertGreater(len(page_updates), 0)
        self.assertIsInstance(page_updates[0], list)

        # Verify all values are integers
        for row in page_updates:
            for val in row:
                self.assertIsInstance(val, int)

        # Verify expected data
        self.assertEqual(len(page_updates), 6)  # 6 lists with varying lengths
        self.assertEqual(page_updates[0], [75, 47, 61, 53, 29])  # 5 values
        self.assertEqual(len(page_updates[1]), 5)  # Variable length rows

    def test_csv_pairs_per_line(self):
        """Integration test: Comma-separated pairs per line (fixed 2 values)."""
        coords = Input("tests/data/test_csv_pairs_per_line").as_delimited_lines()

        # Verify we got valid coordinate pairs
        self.assertIsInstance(coords, list)
        self.assertGreater(len(coords), 0)

        # Each line should have exactly 2 values (coordinate pairs)
        for coord in coords:
            self.assertEqual(len(coord), 2)
            self.assertIsInstance(coord[0], int)
            self.assertIsInstance(coord[1], int)

        # Verify expected data
        self.assertEqual(len(coords), 25)  # 25 coordinate pairs
        self.assertEqual(coords[0], [5, 4])
        self.assertEqual(coords[1], [4, 2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
