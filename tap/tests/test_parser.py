# Copyright (c) 2016, Matt Layman

import inspect
import tempfile
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from tap.parser import Parser


class TestParser(unittest.TestCase):
    """Tests for tap.parser.Parser"""

    def test_finds_ok(self):
        """The parser extracts an ok line."""
        parser = Parser()

        line = parser.parse_line('ok - This is a passing test line.')

        self.assertEqual('test', line.category)
        self.assertTrue(line.ok)
        self.assertTrue(line.number is None)

    def test_finds_number(self):
        """The parser extracts a test number."""
        parser = Parser()

        line = parser.parse_line('ok 42 is the magic number.')

        self.assertEqual('test', line.category)
        self.assertEqual(42, line.number)

    def test_finds_description(self):
        parser = Parser()

        line = parser.parse_line('ok 42 A passing test.')

        self.assertEqual('test', line.category)
        self.assertEqual('A passing test.', line.description)

    def test_after_hash_is_not_description(self):
        parser = Parser()

        line = parser.parse_line('ok A description # Not part of description.')

        self.assertEqual('test', line.category)
        self.assertEqual('A description', line.description)

    def test_finds_todo(self):
        parser = Parser()

        line = parser.parse_line('ok A description # TODO Not done')

        self.assertEqual('test', line.category)
        self.assertTrue(line.todo)

    def test_finds_skip(self):
        parser = Parser()

        line = parser.parse_line('ok A description # SKIP for now')

        self.assertEqual('test', line.category)
        self.assertTrue(line.skip)

    def test_finds_not_ok(self):
        """The parser extracts a not ok line."""
        parser = Parser()

        line = parser.parse_line('not ok - This is a failing test line.')

        self.assertEqual('test', line.category)
        self.assertFalse(line.ok)
        self.assertTrue(line.number is None)

    def test_unrecognizable_line(self):
        """The parser returns an unrecognizable line."""
        parser = Parser()

        line = parser.parse_line('This is not a valid TAP line. # srsly')

        self.assertEqual('unknown', line.category)

    def test_diagnostic_line(self):
        """The parser extracts a diagnostic line."""
        text = '# An example diagnostic line'
        parser = Parser()

        line = parser.parse_line(text)

        self.assertEqual('diagnostic', line.category)
        self.assertEqual(text, line.text)

    def test_bail_out_line(self):
        """The parser extracts a bail out line."""
        parser = Parser()

        line = parser.parse_line('Bail out! This is the reason to bail.')

        self.assertEqual('bail', line.category)
        self.assertEqual('This is the reason to bail.', line.reason)

    def test_finds_version(self):
        """The parser extracts a version line."""
        parser = Parser()

        line = parser.parse_line('TAP version 13')

        self.assertEqual('version', line.category)
        self.assertEqual(13, line.version)

    def test_errors_on_old_version(self):
        """The TAP spec dictates that anything less than 13 is an error."""
        parser = Parser()

        self.assertRaises(ValueError, parser.parse_line, 'TAP version 12')

    def test_finds_plan(self):
        """The parser extracts a plan line."""
        parser = Parser()

        line = parser.parse_line('1..42')

        self.assertEqual('plan', line.category)
        self.assertEqual(42, line.expected_tests)

    def test_finds_plan_with_skip(self):
        """The parser extracts a plan line containing a SKIP."""
        parser = Parser()

        line = parser.parse_line('1..42 # Skipping this test file.')

        self.assertEqual('plan', line.category)
        self.assertTrue(line.skip)

    def test_ignores_plan_with_any_non_skip_directive(self):
        """The parser only recognizes SKIP directives in plans."""
        parser = Parser()

        line = parser.parse_line('1..42 # TODO will not work.')

        self.assertEqual('unknown', line.category)

    def test_parses_file(self):
        sample = inspect.cleandoc(
            """1..2
            ok 1 A passing test
            not ok 2 A failing test""")
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(sample.encode('utf-8'))
        temp.close()
        parser = Parser()
        lines = []

        for line in parser.parse_file(temp.name):
            lines.append(line)

        self.assertEqual(3, len(lines))
        self.assertEqual('plan', lines[0].category)
        self.assertEqual('test', lines[1].category)
        self.assertTrue(lines[1].ok)
        self.assertEqual('test', lines[2].category)
        self.assertFalse(lines[2].ok)

    @mock.patch('tap.parser.sys')
    def test_parses_stdin(self, mock_sys):
        def stdin_data():
            yield '1..2\n'
            yield 'ok 1 A passing test\n'
            yield 'not ok 2 A failing test\n'
        mock_stdin = mock.PropertyMock()
        mock_stdin.side_effect = stdin_data
        type(mock_sys).stdin = mock_stdin
        parser = Parser()
        lines = []

        for line in parser.parse_stdin():
            lines.append(line)

        self.assertEqual(3, len(lines))
        self.assertEqual('plan', lines[0].category)
        self.assertEqual('test', lines[1].category)
        self.assertTrue(lines[1].ok)
        self.assertEqual('test', lines[2].category)
        self.assertFalse(lines[2].ok)
