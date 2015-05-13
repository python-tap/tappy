# Copyright (c) 2015, Matt Layman

import unittest

from tap.directive import Directive
from tap.line import Line, Result


class TestLine(unittest.TestCase):
    """Tests for tap.line.Line"""

    def test_line_requires_category(self):
        line = Line()
        self.assertRaises(NotImplementedError, lambda: line.category)


class TestResult(unittest.TestCase):
    """Tests for tap.line.Result"""

    def test_category(self):
        result = Result(True)
        self.assertEqual('test', result.category)

    def test_ok(self):
        result = Result(True)
        self.assertTrue(result.ok)

    def test_str_ok(self):
        result = Result(True, 42, 'passing')
        self.assertEqual(
            'ok 42 - passing', str(result))

    def test_str_not_ok(self):
        result = Result(False, 43, 'failing')
        self.assertEqual(
            'not ok 43 - failing', str(result))

    def test_str_directive(self):
        directive = Directive('SKIP a reason')
        result = Result(True, 44, 'passing', directive)
        self.assertEqual(
            'ok 44 - passing # SKIP a reason', str(result))
