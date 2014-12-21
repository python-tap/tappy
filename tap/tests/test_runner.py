# Copyright (c) 2014, Matt Layman

import tempfile
import unittest

from tap import TAPTestRunner
from tap.runner import TAPTestResult


class TestTAPTestRunner(unittest.TestCase):

    def test_has_tap_test_result(self):
        runner = TAPTestRunner()
        self.assertEqual(runner.resultclass, TAPTestResult)

    def test_runner_uses_outdir(self):
        """Test that the test runner sets the TAPTestResult OUTDIR so that TAP
        files will be written to that location.

        Setting class attributes to get the right behavior is a dirty hack, but
        the unittest classes aren't very extensible.
        """
        # Save the previous outdir in case **this** execution was using it.
        previous_outdir = TAPTestResult
        outdir = tempfile.mkdtemp()

        TAPTestRunner.set_outdir(outdir)

        self.assertEqual(outdir, TAPTestResult.OUTDIR)

        TAPTestResult.OUTDIR = previous_outdir
