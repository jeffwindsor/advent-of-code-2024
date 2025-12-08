"""
Tests for aoc.input parsers.

Run with: python -m pytest tests/test_input_parsers.py
Or simply: python tests/test_input_parsers.py
"""

import tempfile
import unittest
from pathlib import Path

from aoc import Input, Parser


class TestCSVLinesParser(unittest.TestCase):
    """Tests for the as_csv_lines() parser method."""

    def test_default_comma_separated_integers(self):
        """Test parsing comma-separated integers (default behavior)."""
        parser = Parser("75,47,61,53,29\n97,61,53,29,13\n75,29,13")
        result = parser.as_csv_lines()

        expected = [[75, 47, 61, 53, 29], [97, 61, 53, 29, 13], [75, 29, 13]]
        self.assertEqual(result, expected)

        # Verify types
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], int)

    def test_custom_separator_semicolon(self):
        """Test parsing with custom separator (semicolon)."""
        parser = Parser("1;2;3\n4;5;6\n7;8;9")
        result = parser.as_csv_lines(separator=";")

        expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result, expected)

    def test_custom_separator_pipe(self):
        """Test parsing with pipe separator."""
        parser = Parser("10|20|30\n40|50|60")
        result = parser.as_csv_lines(separator="|")

        expected = [[10, 20, 30], [40, 50, 60]]
        self.assertEqual(result, expected)

    def test_string_converter(self):
        """Test parsing with string converter."""
        parser = Parser("a,b,c\nx,y,z\nfoo,bar,baz")
        result = parser.as_csv_lines(converter=str)

        expected = [['a', 'b', 'c'], ['x', 'y', 'z'], ['foo', 'bar', 'baz']]
        self.assertEqual(result, expected)

        # Verify all values are strings
        for row in result:
            for val in row:
                self.assertIsInstance(val, str)

    def test_float_converter(self):
        """Test parsing with float converter."""
        parser = Parser("1.5,2.7,3.9\n4.2,5.8,6.1")
        result = parser.as_csv_lines(converter=float)

        expected = [[1.5, 2.7, 3.9], [4.2, 5.8, 6.1]]
        self.assertEqual(result, expected)

        # Verify types
        self.assertIsInstance(result[0][0], float)

    def test_single_value_per_line(self):
        """Test parsing lines with single values."""
        parser = Parser("100\n200\n300")
        result = parser.as_csv_lines()

        expected = [[100], [200], [300]]
        self.assertEqual(result, expected)

    def test_empty_lines_skipped(self):
        """Test that empty lines are skipped (via as_lines behavior)."""
        parser = Parser("1,2,3\n\n4,5,6\n\n7,8,9")
        result = parser.as_csv_lines()

        expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result, expected)

    def test_whitespace_handling(self):
        """Test that leading/trailing whitespace is handled."""
        parser = Parser("  1,2,3  \n  4,5,6  ")
        result = parser.as_csv_lines()

        expected = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(result, expected)

    def test_variable_length_rows(self):
        """Test parsing rows with different numbers of values."""
        parser = Parser("1,2,3,4,5\n6,7\n8,9,10")
        result = parser.as_csv_lines()

        expected = [[1, 2, 3, 4, 5], [6, 7], [8, 9, 10]]
        self.assertEqual(result, expected)

    def test_with_input_class(self):
        """Test as_csv_lines() via Input class delegation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("10,20,30\n40,50,60")
            temp_path = f.name

        try:
            result = Input(temp_path).as_csv_lines()
            expected = [[10, 20, 30], [40, 50, 60]]
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()

    def test_day5_format(self):
        """Test with actual Day 5 puzzle data format (page updates)."""
        # Simulate Day 5 page updates section
        parser = Parser("75,47,61,53,29\n97,61,53,29,13\n75,29,13")
        result = parser.as_csv_lines()

        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 5)  # First update has 5 pages
        self.assertEqual(result[0][0], 75)

    def test_day18_format(self):
        """Test with actual Day 18 puzzle data format (coordinate pairs)."""
        # Simulate Day 18 coordinate format
        parser = Parser("5,4\n4,2\n4,5\n3,0\n2,1")
        result = parser.as_csv_lines()

        self.assertEqual(len(result), 5)
        self.assertEqual(len(result[0]), 2)  # Each coordinate has 2 values
        self.assertEqual(result[0], [5, 4])
        self.assertEqual(result[1], [4, 2])




class TestKeyValuePairsParser(unittest.TestCase):
    """Tests for the as_key_value_pairs() parser method."""

    def test_default_key_value_with_int_lists(self):
        """Test parsing key:value format with default behavior (int key, int list values)."""
        parser = Parser("190: 10 19\n3267: 81 40 27\n83: 17 5")
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
        parser = Parser("x = 1 2 3\ny = 4 5 6")
        result = parser.as_key_value_pairs(key_type=str, separator="=")

        expected = [('x', [1, 2, 3]), ('y', [4, 5, 6])]
        self.assertEqual(result, expected)

    def test_string_keys(self):
        """Test with string keys instead of integers."""
        parser = Parser("test: 10 20\nfoo: 30 40")
        result = parser.as_key_value_pairs(key_type=str)

        expected = [('test', [10, 20]), ('foo', [30, 40])]
        self.assertEqual(result, expected)
        self.assertIsInstance(result[0][0], str)

    def test_single_value_parser(self):
        """Test with custom value parser that returns single value."""
        parser = Parser("x: 42\ny: 99\nz: 123")
        result = parser.as_key_value_pairs(key_type=str, value_parser=int)

        expected = [('x', 42), ('y', 99), ('z', 123)]
        self.assertEqual(result, expected)
        self.assertIsInstance(result[0][1], int)  # Single int, not list

    def test_custom_value_parser(self):
        """Test with custom value parser (split on spaces)."""
        parser = Parser("test: hello world\nfoo: bar baz qux")
        result = parser.as_key_value_pairs(
            key_type=str,
            value_parser=str.split
        )

        expected = [('test', ['hello', 'world']), ('foo', ['bar', 'baz', 'qux'])]
        self.assertEqual(result, expected)
        self.assertIsInstance(result[0][1][0], str)

    def test_whitespace_handling(self):
        """Test that whitespace around separator is handled."""
        parser = Parser("  100:  5 10 15  \n  200:  20 25  ")
        result = parser.as_key_value_pairs()

        expected = [(100, [5, 10, 15]), (200, [20, 25])]
        self.assertEqual(result, expected)

    def test_variable_value_lengths(self):
        """Test keys with different numbers of values."""
        parser = Parser("1: 10\n2: 20 30\n3: 40 50 60 70")
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




class TestStructuredIntsParser(unittest.TestCase):
    """Tests for the as_structured_ints() parser method."""

    def test_position_velocity_format(self):
        """Test parsing position/velocity format with 4 ints per line."""
        parser = Parser("p=0,4 v=3,-3\np=6,3 v=-1,-3\np=10,3 v=-1,2")
        result = parser.as_structured_ints(4)

        expected = [(0, 4, 3, -3), (6, 3, -1, -3), (10, 3, -1, 2)]
        self.assertEqual(result, expected)

        # Verify types
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], int)

    def test_negative_numbers(self):
        """Test that negative numbers are extracted correctly."""
        parser = Parser("p=100,351 v=-10,25\np=-5,-10 v=20,-30")
        result = parser.as_structured_ints(4)

        expected = [(100, 351, -10, 25), (-5, -10, 20, -30)]
        self.assertEqual(result, expected)

    def test_coordinate_triplets(self):
        """Test parsing with 3 integers per line."""
        parser = Parser("x=10 y=20 id=1\nx=30 y=40 id=2\nx=50 y=60 id=3")
        result = parser.as_structured_ints(3)

        expected = [(10, 20, 1), (30, 40, 2), (50, 60, 3)]
        self.assertEqual(result, expected)

    def test_single_int_per_line(self):
        """Test parsing with 1 integer per line."""
        parser = Parser("value: 42\ncount: 99\ntotal: 123")
        result = parser.as_structured_ints(1)

        expected = [(42,), (99,), (123,)]
        self.assertEqual(result, expected)

    def test_validation_error_too_few_ints(self):
        """Test that ValueError is raised if line has too few integers."""
        parser = Parser("p=0,4 v=3")  # Only 3 ints, expecting 4
        with self.assertRaises(ValueError) as context:
            parser.as_structured_ints(4)

        self.assertIn("expected 4 integers, got 3", str(context.exception))
        self.assertIn("Line 1", str(context.exception))

    def test_validation_error_too_many_ints(self):
        """Test that ValueError is raised if line has too many integers."""
        parser = Parser("1 2 3 4 5")  # 5 ints, expecting 3
        with self.assertRaises(ValueError) as context:
            parser.as_structured_ints(3)

        self.assertIn("expected 3 integers, got 5", str(context.exception))

    def test_mixed_text_and_numbers(self):
        """Test extraction from lines with mixed text and numbers."""
        parser = Parser("robot at position (10, 20) moving velocity (-5, 3)")
        result = parser.as_structured_ints(4)

        expected = [(10, 20, -5, 3)]
        self.assertEqual(result, expected)

    def test_with_input_class(self):
        """Test as_structured_ints() via Input class delegation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("p=1,2 v=3,4\np=5,6 v=7,8")
            temp_path = f.name

        try:
            result = Input(temp_path).as_structured_ints(4)
            expected = [(1, 2, 3, 4), (5, 6, 7, 8)]
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()


class TestStructuredIntsIntegration(unittest.TestCase):
    """Integration tests for structured ints parsing scenarios."""

    def test_structured_ints_position_velocity(self):
        """Integration test: Extract position/velocity format (4 ints per line)."""
        result = Input("tests/data/test_structured_ints_position_velocity").as_structured_ints(4)

        # Verify we got valid data
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], tuple)

        # Each tuple should have exactly 4 integers
        for tup in result:
            self.assertEqual(len(tup), 4)
            for val in tup:
                self.assertIsInstance(val, int)

        # Verify expected data (from Day 14 example)
        self.assertEqual(result[0], (0, 4, 3, -3))
        self.assertEqual(result[1], (6, 3, -1, -3))




class TestSectionsParser(unittest.TestCase):
    """Tests for the as_sections() parser method."""

    def test_two_sections(self):
        """Test splitting input into two sections."""
        parser = Parser("section1\ndata\n\nsection2\nmore")
        sections = parser.as_sections()

        self.assertEqual(len(sections), 2)
        self.assertIsInstance(sections[0], Parser)
        self.assertEqual(sections[0].content, "section1\ndata")
        self.assertEqual(sections[1].content, "section2\nmore")

    def test_three_sections(self):
        """Test splitting input into three sections."""
        parser = Parser("sec1\n\nsec2\n\nsec3")
        sections = parser.as_sections()

        self.assertEqual(len(sections), 3)
        contents = [s.content for s in sections]
        self.assertEqual(contents, ['sec1', 'sec2', 'sec3'])

    def test_four_sections(self):
        """Test splitting input into four sections."""
        parser = Parser("a\n\nb\n\nc\n\nd")
        sections = parser.as_sections()

        self.assertEqual(len(sections), 4)

    def test_single_section(self):
        """Test input with no blank lines (single section)."""
        parser = Parser("line1\nline2\nline3")
        sections = parser.as_sections()

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].content, "line1\nline2\nline3")

    def test_whitespace_stripping(self):
        """Test that whitespace is stripped by default."""
        parser = Parser("  section1  \n\n  section2  ")
        sections = parser.as_sections()

        self.assertEqual(sections[0].content, "section1")
        self.assertEqual(sections[1].content, "section2")

    def test_whitespace_preservation(self):
        """Test whitespace preservation when strip=False."""
        parser = Parser("  section1  \n\n  section2  ")
        sections = parser.as_sections(strip=False)

        self.assertEqual(sections[0].content, "  section1  ")
        self.assertEqual(sections[1].content, "  section2  ")

    def test_sections_are_parsers(self):
        """Test that each section is a Parser with full functionality."""
        parser = Parser("1,2,3\n4,5,6\n\n7,8,9")
        sections = parser.as_sections()

        # First section can be parsed as CSV
        csv_data = sections[0].as_csv_lines()
        self.assertEqual(csv_data, [[1, 2, 3], [4, 5, 6]])

        # Second section can also be parsed
        csv_data2 = sections[1].as_csv_lines()
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
            self.assertIsInstance(section, Parser)

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




class TestPipeRulesParser(unittest.TestCase):
    """Tests for the as_pipe_rules() parser method."""

    def test_basic_ordering_rules(self):
        """Test parsing basic pipe-separated ordering rules."""
        parser = Parser("47|53\n97|13\n97|61")
        result = parser.as_pipe_rules()

        expected = {47: [53], 97: [13, 61]}
        self.assertEqual(result, expected)

        # Verify types
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result[47], list)
        self.assertIsInstance(result[47][0], int)

    def test_multiple_dependencies(self):
        """Test keys with multiple dependent values."""
        parser = Parser("1|2\n1|3\n1|4\n2|5\n2|6")
        result = parser.as_pipe_rules()

        expected = {1: [2, 3, 4], 2: [5, 6]}
        self.assertEqual(result, expected)

    def test_single_dependency_each(self):
        """Test each key having single dependency."""
        parser = Parser("10|20\n30|40\n50|60")
        result = parser.as_pipe_rules()

        expected = {10: [20], 30: [40], 50: [60]}
        self.assertEqual(result, expected)

    def test_custom_separator_arrow(self):
        """Test with custom separator (arrow)."""
        parser = Parser("A->B\nA->C\nB->D")
        result = parser.as_pipe_rules(separator="->")

        expected = {'A': ['B', 'C'], 'B': ['D']}
        self.assertEqual(result, expected)
        self.assertIsInstance(result['A'][0], str)

    def test_custom_separator_colon(self):
        """Test with colon separator."""
        parser = Parser("1:2\n1:3\n2:4")
        result = parser.as_pipe_rules(separator=":")

        expected = {1: [2, 3], 2: [4]}
        self.assertEqual(result, expected)

    def test_whitespace_handling(self):
        """Test that whitespace around values is handled."""
        parser = Parser("  1  |  2  \n  3  |  4  ")
        result = parser.as_pipe_rules()

        expected = {1: [2], 3: [4]}
        self.assertEqual(result, expected)

    def test_preserves_order(self):
        """Test that dependencies preserve insertion order."""
        parser = Parser("1|5\n1|3\n1|9\n1|1")
        result = parser.as_pipe_rules()

        # Should maintain order: 5, 3, 9, 1
        self.assertEqual(result[1], [5, 3, 9, 1])

    def test_with_input_class(self):
        """Test as_pipe_rules() via Input class delegation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("10|20\n10|30\n20|40")
            temp_path = f.name

        try:
            result = Input(temp_path).as_pipe_rules()
            expected = {10: [20, 30], 20: [40]}
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()


class TestPipeRulesIntegration(unittest.TestCase):
    """Integration tests for pipe rules parsing scenarios."""

    def test_pipe_rules_ordering(self):
        """Integration test: Pipe-separated ordering rules (page dependencies)."""
        result = Input("tests/data/test_pipe_rules_ordering").as_pipe_rules()

        # Verify we got valid data
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)

        # All keys and values should be integers
        for key, values in result.items():
            self.assertIsInstance(key, int)
            self.assertIsInstance(values, list)
            for val in values:
                self.assertIsInstance(val, int)

        # Verify expected data (from Day 5 example)
        self.assertIn(47, result)
        self.assertEqual(result[47], [53])
        self.assertIn(97, result)
        self.assertIn(13, result[97])




class TestRegexGroupsParser(unittest.TestCase):
    """Tests for the as_regex_groups() parser method."""

    def test_position_velocity_pattern(self):
        """Test extracting position/velocity with regex groups."""
        parser = Parser("p=0,4 v=3,-3\np=6,3 v=-1,-3")
        result = parser.as_regex_groups(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

        expected = [('0', '4', '3', '-3'), ('6', '3', '-1', '-3')]
        self.assertEqual(result, expected)

        # Verify types
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], str)  # Groups are strings

    def test_named_fields_extraction(self):
        """Test extracting named fields."""
        parser = Parser("name: Alice age: 25\nname: Bob age: 30")
        result = parser.as_regex_groups(r"name: (\w+) age: (\d+)")

        expected = [('Alice', '25'), ('Bob', '30')]
        self.assertEqual(result, expected)

    def test_command_parsing(self):
        """Test parsing command-style input."""
        parser = Parser("move 3 from 1 to 2\nmove 5 from 3 to 1")
        result = parser.as_regex_groups(r"move (\d+) from (\d+) to (\d+)")

        expected = [('3', '1', '2'), ('5', '3', '1')]
        self.assertEqual(result, expected)

    def test_single_group(self):
        """Test pattern with single capture group."""
        parser = Parser("value: 42\nvalue: 99\nvalue: 123")
        result = parser.as_regex_groups(r"value: (\d+)")

        expected = [('42',), ('99',), ('123',)]
        self.assertEqual(result, expected)

    def test_no_matches_skipped(self):
        """Test that lines without matches are skipped."""
        parser = Parser("match: 1\nnot a match\nmatch: 2")
        result = parser.as_regex_groups(r"match: (\d+)")

        expected = [('1',), ('2',)]
        self.assertEqual(result, expected)

    def test_complex_pattern(self):
        """Test complex pattern with multiple group types."""
        parser = Parser("id=10 name=test value=3.14\nid=20 name=prod value=2.71")
        result = parser.as_regex_groups(r"id=(\d+) name=(\w+) value=([\d.]+)")

        expected = [('10', 'test', '3.14'), ('20', 'prod', '2.71')]
        self.assertEqual(result, expected)

    def test_negative_numbers(self):
        """Test pattern capturing negative numbers."""
        parser = Parser("x=-5 y=10\nx=3 y=-7")
        result = parser.as_regex_groups(r"x=(-?\d+) y=(-?\d+)")

        expected = [('-5', '10'), ('3', '-7')]
        self.assertEqual(result, expected)

    def test_with_input_class(self):
        """Test as_regex_groups() via Input class delegation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("a=1 b=2\na=3 b=4")
            temp_path = f.name

        try:
            result = Input(temp_path).as_regex_groups(r"a=(\d+) b=(\d+)")
            expected = [('1', '2'), ('3', '4')]
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()


class TestRegexGroupsIntegration(unittest.TestCase):
    """Integration tests for regex groups parsing scenarios."""

    def test_regex_groups_position_velocity(self):
        """Integration test: Extract position/velocity using regex capture groups."""
        pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
        result = Input("tests/data/test_regex_groups_position_velocity").as_regex_groups(pattern)

        # Verify we got valid data
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], tuple)

        # Each tuple should have exactly 4 captured groups (strings)
        for tup in result:
            self.assertEqual(len(tup), 4)
            for val in tup:
                self.assertIsInstance(val, str)

        # Verify expected data (from Day 14 example)
        self.assertEqual(result[0], ('0', '4', '3', '-3'))
        self.assertEqual(result[1], ('6', '3', '-1', '-3'))


class TestCSVLinesIntegration(unittest.TestCase):
    """Integration tests for CSV line parsing scenarios."""

    def test_csv_multi_values_per_line(self):
        """Integration test: Multiple comma-separated values per line (variable length)."""
        section1, section2 = Input("tests/data/test_csv_multi_values_per_line").as_two_parts()
        page_updates = section2.as_csv_lines()

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
        coords = Input("tests/data/test_csv_pairs_per_line").as_csv_lines()

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
