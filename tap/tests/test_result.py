# Copyright (c) 2016, Matt Layman

import os
import unittest

from tap.runner import TAPTestResult
from tap.tracker import Tracker


class FakeTestCase(unittest.TestCase):

    def runTest(self):
        pass

    def __call__(self, result):
        pass


class TestTAPTestResult(unittest.TestCase):

    @classmethod
    def _make_one(cls):
        # Yep, the stream is not being closed.
        stream = open(os.devnull, 'w')
        result = TAPTestResult(stream, False, 0)
        result.tracker = Tracker()
        return result

    def test_adds_error(self):
        result = self._make_one()
        # Python 3 does some extra testing in unittest on exceptions so fake
        # the cause as if it were raised.
        ex = Exception()
        ex.__cause__ = None
        result.addError(FakeTestCase(), (None, ex, None))
        self.assertEqual(len(result.tracker._test_cases['FakeTestCase']), 1)

    def test_adds_failure(self):
        result = self._make_one()
        # Python 3 does some extra testing in unittest on exceptions so fake
        # the cause as if it were raised.
        ex = Exception()
        ex.__cause__ = None
        result.addFailure(FakeTestCase(), (None, ex, None))
        self.assertEqual(len(result.tracker._test_cases['FakeTestCase']), 1)

    def test_adds_success(self):
        result = self._make_one()
        result.addSuccess(FakeTestCase())
        self.assertEqual(len(result.tracker._test_cases['FakeTestCase']), 1)

    def test_adds_skip(self):
        result = self._make_one()
        try:
            result.addSkip(FakeTestCase(), 'a reason')
            self.assertEqual(
                len(result.tracker._test_cases['FakeTestCase']), 1)
        except AttributeError:
            self.assertTrue(True, 'Python 2.6 does not support skip.')

    def test_adds_expected_failure(self):
        result = self._make_one()
        try:
            result.addExpectedFailure(FakeTestCase(), (None, None, None))
            line = result.tracker._test_cases['FakeTestCase'][0]
            self.assertEqual(line.status, 'not ok')
            self.assertEqual(line.directive, '(expected failure)')
        except AttributeError:
            self.assertTrue(
                True, 'Python 2.6 does not support expected failure.')

    def test_adds_unexpected_success(self):
        result = self._make_one()
        try:
            result.addUnexpectedSuccess(FakeTestCase())
            line = result.tracker._test_cases['FakeTestCase'][0]
            self.assertEqual(line.status, 'ok')
            self.assertEqual(line.directive, '(unexpected success)')
        except AttributeError:
            self.assertTrue(
                True, 'Python 2.6 does not support unexpected success.')
