# Copyright (c) 2014, Matt Layman

from unittest import TextTestRunner

# Older versions of Python have the result under a different name.
try:
    from unittest import TextTestResult
except ImportError:
    from unittest import _TextTestResult as TextTestResult

from tap.tracker import Tracker


class TAPTestResult(TextTestResult):

    # This attribute will store the user's desired output directory.
    OUTDIR = None

    def __init__(self, stream, descriptions, verbosity):
        super(TAPTestResult, self).__init__(stream, descriptions, verbosity)
        self.tracker = Tracker(outdir=self.OUTDIR)

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
                                '(expected failure)')

    def addUnexpectedSuccess(self, test):
        super(TAPTestResult, self).addUnexpectedSuccess(test)
        self.tracker.add_ok(self._cls_name(test), self._description(test),
                            '(unexpected success)')

    def _cls_name(self, test):
        return test.__class__.__name__

    def _description(self, test):
        return test.shortDescription() or str(test)


class TAPTestRunner(TextTestRunner):
    """A test runner that will behave exactly like TextTestRunner and will
    additionally generate TAP files for each test case"""

    resultclass = TAPTestResult

    @classmethod
    def set_outdir(cls, outdir):
        """Set the output directory so that TAP files are written to the
        specified outdir location.
        """
        # Blame the lack of unittest extensibility for this hacky method.
        TAPTestResult.OUTDIR = outdir
