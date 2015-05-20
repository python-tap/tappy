# Copyright (c) 2015, Matt Layman

import os
from unittest import TextTestRunner
import sys

# Older versions of Python have the result under a different name.
try:
    from unittest import TextTestResult
except ImportError:
    from unittest import _TextTestResult as TextTestResult
try:
    from unittest.runner import _WritelnDecorator
except ImportError:  # Python 2.6 has a different package structure.
    from unittest import _WritelnDecorator

from tap.i18n import _
from tap.tracker import Tracker


class TAPTestResult(TextTestResult):

    FORMAT = None

    def __init__(self, stream, descriptions, verbosity):
        super(TAPTestResult, self).__init__(stream, descriptions, verbosity)

    def stopTestRun(self):
        """Once the test run is complete, generate each of the TAP files."""
        super(TAPTestResult, self).stopTestRun()
        self.tracker.generate_tap_reports()

    def addError(self, test, err):
        super(TAPTestResult, self).addError(test, err)
        self.tracker.add_not_ok(self._cls_name(test), self._description(test))

    def addFailure(self, test, err):
        super(TAPTestResult, self).addFailure(test, err)
        self.tracker.add_not_ok(self._cls_name(test), self._description(test))

    def addSuccess(self, test):
        super(TAPTestResult, self).addSuccess(test)
        self.tracker.add_ok(self._cls_name(test), self._description(test))

    def addSkip(self, test, reason):
        super(TAPTestResult, self).addSkip(test, reason)
        self.tracker.add_skip(
            self._cls_name(test), self._description(test), reason)

    def addExpectedFailure(self, test, err):
        super(TAPTestResult, self).addExpectedFailure(test, err)
        self.tracker.add_not_ok(self._cls_name(test), self._description(test),
                                _('(expected failure)'))

    def addUnexpectedSuccess(self, test):
        super(TAPTestResult, self).addUnexpectedSuccess(test)
        self.tracker.add_ok(self._cls_name(test), self._description(test),
                            _('(unexpected success)'))

    def _cls_name(self, test):
        return test.__class__.__name__

    def _description(self, test):
        if self.FORMAT:
            try:
                return self.FORMAT.format(
                    method_name=str(test),
                    short_description=test.shortDescription() or '')
            except KeyError:
                sys.exit(_(
                    'Bad format string: {format}\n'
                    'Replacement options are: {{short_description}} and '
                    '{{method_name}}').format(format=self.FORMAT))

        return test.shortDescription() or str(test)


# Module level state stinks, but this is the only way to keep compatibility
# with Python 2.6. The best place for the tracker is as an instance variable
# on the runner, but __init__ is so different that it is not easy to create
# a runner that satisfies every supported Python version.
_tracker = Tracker()


class TAPTestRunner(TextTestRunner):
    """A test runner that will behave exactly like TextTestRunner and will
    additionally generate TAP files for each test case"""

    resultclass = TAPTestResult

    def set_stream(self, streaming):
        """Set the streaming boolean option to stream TAP directly to stdout.

        The test runner default output will be suppressed in favor of TAP.
        """
        self.stream = _WritelnDecorator(open(os.devnull, 'w'))
        _tracker.streaming = streaming
        _tracker.stream = sys.stdout

    def _makeResult(self):
        result = self.resultclass(
            self.stream, self.descriptions, self.verbosity)
        result.tracker = _tracker
        return result

    @classmethod
    def set_outdir(cls, outdir):
        """Set the output directory so that TAP files are written to the
        specified outdir location.
        """
        # Blame the lack of unittest extensibility for this hacky method.
        _tracker.outdir = outdir

    @classmethod
    def set_combined(cls, combined):
        """Set the tracker to use a single output file."""
        _tracker.combined = combined

    @classmethod
    def set_format(cls, fmt):
        """Set the format of each test line.

        The format string can use:
        * {method_name}: The test method name
        * {short_description}: The test's docstring short description
        """
        TAPTestResult.FORMAT = fmt
