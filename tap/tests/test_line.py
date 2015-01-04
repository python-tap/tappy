# Copyright (c) 2015, Matt Layman

import unittest

from tap.line import Line, Result


class TestLine(unittest.TestCase):
    """Tests for tap.line.Line"""

    def test_line_requires_category(self):
        line = Line()

        def check_category():
            line.category

        self.assertRaises(NotImplementedError, check_category)


class TestResult(unittest.TestCase):
    """Tests for tap.line.Result"""

    def test_category(self):
        result = Result(True)
        self.assertEqual('test', result.category)

    def test_ok(self):
        result = Result(True)
        self.assertTrue(result.ok)
