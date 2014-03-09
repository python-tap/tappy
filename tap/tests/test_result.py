# Copyright (c) 2014, Matt Layman

import os
import unittest

from tap.runner import TAPTestResult


class FakeTestCase(unittest.TestCase):
    '''A fake test case'''

    def runTest(self):
        pass


class TestTAPTestResult(unittest.TestCase):

    @classmethod
    def _make_one(cls):
        # Yep, the stream is not being closed.
        stream = open(os.devnull, 'w')
        result = TAPTestResult(stream, False, 0)
        result._test_cases['FakeTestCase'] = []
        return result

    def test_has_test_cases(self):
        stream = open(os.devnull, 'w')
        result = TAPTestResult(stream, False, 0)
        self.assertEqual(result._test_cases, {})

    def test_tracks_test_case(self):
        '''Test that a new test case is tracked when first encountered.'''
        stream = open(os.devnull, 'w')
        result = TAPTestResult(stream, False, 0)
        result.startTest(FakeTestCase())
        self.assertEqual(result._test_cases.get('FakeTestCase'), [])

    def test_adds_error(self):
        result = self._make_one()
        result.addError(FakeTestCase(), (None, None, None))
        line = result._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'not ok')
        self.assertTrue('runTest (' in line.description)
        self.assertEqual(line.directive, '')

    def test_adds_failure(self):
        result = self._make_one()
        result.addFailure(FakeTestCase(), (None, None, None))
        line = result._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'not ok')
        self.assertTrue('runTest (' in line.description)
        self.assertEqual(line.directive, '')

    def test_adds_success(self):
        result = self._make_one()
        result.addSuccess(FakeTestCase())
        line = result._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'ok')
        self.assertTrue('runTest (' in line.description)
        self.assertEqual(line.directive, '')

    def test_adds_skip(self):
        result = self._make_one()
        result.addSkip(FakeTestCase(), 'a reason')
        line = result._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'ok')
        self.assertTrue('runTest (' in line.description)
        self.assertEqual(line.directive, '# SKIP a reason')

    def test_adds_expected_failure(self):
        result = self._make_one()
        result.addExpectedFailure(FakeTestCase(), (None, None, None))
        line = result._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'not ok')
        self.assertTrue('runTest (' in line.description)
        self.assertEqual(line.directive, '(expected failure)')

    def test_adds_unexpected_success(self):
        result = self._make_one()
        result.addUnexpectedSuccess(FakeTestCase())
        line = result._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'ok')
        self.assertTrue('runTest (' in line.description)
        self.assertEqual(line.directive, '(unexpected success)')
