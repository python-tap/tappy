# Copyright (c) 2014, Matt Layman

from __future__ import print_function
from collections import namedtuple
import unittest
import sys

TAPLine = namedtuple('TAPLine', ['status', 'description', 'directive'])


class TAPTestResult(unittest.TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super(TAPTestResult, self).__init__(stream, descriptions, verbosity)
        # The test cases dictionary tracks all the TAP lines to write out.
        self._test_cases = {}

    def startTest(self, test):
        '''Add the test class to tracing if it has not been seen yet.'''
        super(TAPTestResult, self).startTest(test)
        cls_name = test.__class__.__name__
        if self._test_cases.get(cls_name) is None:
            self._test_cases[cls_name] = []

    def stopTestRun(self):
        '''Once the test run is complete, generate each of the TAP files.'''
        super(TAPTestResult, self).stopTestRun()
        for test_case, tap_lines in self._test_cases.items():
            with open(test_case + '.tap', 'w') as f:
                print('# TAP results for {0}'.format(test_case), file=f)

                for line_count, tap_line in enumerate(tap_lines, start=1):
                    print(' '.join([
                        tap_line.status,
                        str(line_count),
                        '-',
                        tap_line.description,
                        tap_line.directive,
                    ]), file=f)

                print('1..{0}'.format(len(tap_lines)), file=f)

    def addError(self, test, err):
        # TAP does not distinguish between errors and failures.
        super(TAPTestResult, self).addError(test, err)
        self._add_line(test, 'not ok', '')

    def addFailure(self, test, err):
        # TAP does not distinguish between errors and failures.
        super(TAPTestResult, self).addFailure(test, err)
        self._add_line(test, 'not ok', '')

    def addSuccess(self, test):
        super(TAPTestResult, self).addSuccess(test)
        self._add_line(test, 'ok', '')

    def addSkip(self, test, reason):
        super(TAPTestResult, self).addSkip(test, reason)
        self._add_line(test, 'ok', '# SKIP {0}'.format(reason))

    def addExpectedFailure(self, test, err):
        super(TAPTestResult, self).addExpectedFailure(test, err)
        self._add_line(test, 'not ok', '(expected failure)')

    def addUnexpectedSuccess(self, test):
        super(TAPTestResult, self).addUnexpectedSuccess(test)
        self._add_line(test, 'ok', '(unexpected success)')

    def _add_line(self, test, status, directive):
        description = test.shortDescription() or str(test)
        self._test_cases[test.__class__.__name__].append(
            TAPLine(status, description, directive))


class TAPTestRunner(unittest.TextTestRunner):
    '''A test runner that will behave exactly like TextTestRunner and will
    additionally generate TAP files for each test case'''

    resultclass = TAPTestResult
