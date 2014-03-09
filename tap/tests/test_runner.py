# Copyright (c) 2014, Matt Layman

import unittest

from tap import TAPTestRunner
from tap.runner import TAPTestResult


class TestTAPTestRunner(unittest.TestCase):

    def test_has_tap_test_result(self):
        runner = TAPTestRunner()
        self.assertEqual(runner.resultclass, TAPTestResult)
