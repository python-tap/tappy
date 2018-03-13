# Copyright (c) 2018, Matt Layman and contributors

import unittest

from tap.directive import Directive
from tap.line import Line, Result


class TestLine(unittest.TestCase):
    """Tests for tap.line.Line"""

    def test_line_requires_category(self):
        line = Line()
        with self.assertRaises(NotImplementedError):
            line.category


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
            'ok 42 passing', str(result))

    def test_str_not_ok(self):
        result = Result(False, 43, 'failing')
        self.assertEqual(
            'not ok 43 failing', str(result))

    def test_str_directive(self):
        directive = Directive('SKIP a reason')
        result = Result(True, 44, 'passing', directive)
        self.assertEqual(
            'ok 44 passing # SKIP a reason', str(result))

    def test_str_diagnostics(self):
        result = Result(False, 43, 'failing', diagnostics='# more info')
        self.assertEqual(
            'not ok 43 failing\n# more info', str(result))
