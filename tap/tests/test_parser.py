# Copyright (c) 2014, Matt Layman

import unittest

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
