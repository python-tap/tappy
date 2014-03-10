# Copyright (c) 2014, Matt Layman

import os
import unittest

from tap.runner import TAPTestResult


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
        return result

    def test_has_tracker(self):
        result = self._make_one()
        self.assertTrue(result.tracker is not None)

    def test_adds_error(self):
        result = self._make_one()
        result.addError(FakeTestCase(), (None, None, None))
        self.assertEqual(len(result.tracker._test_cases['FakeTestCase']), 1)

    def test_adds_failure(self):
        result = self._make_one()
        result.addFailure(FakeTestCase(), (None, None, None))
        self.assertEqual(len(result.tracker._test_cases['FakeTestCase']), 1)

    def test_adds_success(self):
        result = self._make_one()
        result.addSuccess(FakeTestCase())
        self.assertEqual(len(result.tracker._test_cases['FakeTestCase']), 1)

    def test_adds_skip(self):
        result = self._make_one()
        result.addSkip(FakeTestCase(), 'a reason')
        self.assertEqual(len(result.tracker._test_cases['FakeTestCase']), 1)

    def test_adds_expected_failure(self):
        result = self._make_one()
        result.addExpectedFailure(FakeTestCase(), (None, None, None))
        line = result.tracker._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'not ok')
        self.assertEqual(line.directive, '(expected failure)')

    def test_adds_unexpected_success(self):
        result = self._make_one()
        result.addUnexpectedSuccess(FakeTestCase())
        line = result.tracker._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'ok')
        self.assertEqual(line.directive, '(unexpected success)')
