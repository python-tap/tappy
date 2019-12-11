# Copyright (c) 2019, Matt Layman and contributors

import contextlib
import os
import unittest
import unittest.case

from tap.i18n import _
from tap.runner import TAPTestResult
from tap.tests import TestCase
from tap.tracker import Tracker


class FakeTestCase(unittest.TestCase):
    def runTest(self):
        pass

    @contextlib.contextmanager
    def subTest(self, *args, **kwargs):
        try:
            self._subtest = unittest.case._SubTest(self, object(), {})
            yield
        finally:
            self._subtest = None

    def __call__(self, result):
        pass


class TestTAPTestResult(TestCase):
    @classmethod
    def _make_one(cls):
        # Yep, the stream is not being closed.
        stream = open(os.devnull, "w")
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
        self.assertEqual(len(result.tracker._test_cases["FakeTestCase"]), 1)

    def test_adds_failure(self):
        result = self._make_one()
        # Python 3 does some extra testing in unittest on exceptions so fake
        # the cause as if it were raised.
        ex = Exception()
        ex.__cause__ = None
        result.addFailure(FakeTestCase(), (None, ex, None))
        self.assertEqual(len(result.tracker._test_cases["FakeTestCase"]), 1)

    def test_adds_success(self):
        result = self._make_one()
        result.addSuccess(FakeTestCase())
        self.assertEqual(len(result.tracker._test_cases["FakeTestCase"]), 1)

    def test_adds_skip(self):
        result = self._make_one()
        result.addSkip(FakeTestCase(), "a reason")
        self.assertEqual(len(result.tracker._test_cases["FakeTestCase"]), 1)

    def test_adds_expected_failure(self):
        exc = self.factory.make_exc()
        result = self._make_one()
        result.addExpectedFailure(FakeTestCase(), exc)
        line = result.tracker._test_cases["FakeTestCase"][0]
        self.assertFalse(line.ok)
        self.assertEqual(line.directive.text, "TODO {}".format(_("(expected failure)")))

    def test_adds_unexpected_success(self):
        result = self._make_one()
        result.addUnexpectedSuccess(FakeTestCase())
        line = result.tracker._test_cases["FakeTestCase"][0]
        self.assertTrue(line.ok)
        self.assertEqual(
            line.directive.text, "TODO {}".format(_("(unexpected success)"))
        )

    def test_adds_subtest_success(self):
        """Test that the runner handles subtest success results."""
        result = self._make_one()
        test = FakeTestCase()
        with test.subTest():
            result.addSubTest(test, test._subtest, None)
        line = result.tracker._test_cases["FakeTestCase"][0]
        self.assertTrue(line.ok)

    def test_adds_subtest_failure(self):
        """Test that the runner handles subtest failure results."""
        result = self._make_one()
        # Python 3 does some extra testing in unittest on exceptions so fake
        # the cause as if it were raised.
        ex = Exception()
        ex.__cause__ = None
        test = FakeTestCase()
        with test.subTest():
            result.addSubTest(test, test._subtest, (ex.__class__, ex, None))
        line = result.tracker._test_cases["FakeTestCase"][0]
        self.assertFalse(line.ok)
