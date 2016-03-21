# Copyright (c) 2016, Matt Layman

from __future__ import print_function
import os
import string
import sys

from tap.directive import Directive
from tap.i18n import _
from tap.line import Result


class Tracker(object):

    def __init__(
            self, outdir=None, combined=False, streaming=False, stream=None,
            header=True):
        self.outdir = outdir

        # Combine all the test results into one file.
        self.combined = combined
        self.combined_line_number = 0
        # Test case ordering is important for the combined results
        # because of how numbers are assigned. The test cases
        # must be tracked in order so that reporting can sequence
        # the line numbers properly.
        self.combined_test_cases_seen = []

        # Stream output directly to a stream instead of file output.
        self.streaming = streaming
        self.stream = stream

        # Display the test case header unless told not to.
        self.header = header

        # Internal state for tracking each test case.
        self._test_cases = {}

        # Python versions 2 and 3 keep maketrans in different locations.
        if sys.version_info[0] < 3:
            self._sanitized_table = string.maketrans(' \\/\n', '----')
        else:  # pragma: no cover
            self._sanitized_table = str.maketrans(' \\/\n', '----')

    def _get_outdir(self):
        return self._outdir

    def _set_outdir(self, outdir):
        self._outdir = outdir
        if outdir and not os.path.exists(outdir):
            os.makedirs(outdir)

    outdir = property(_get_outdir, _set_outdir)

    def _track(self, class_name):
        """Keep track of which test cases have executed."""
        if self._test_cases.get(class_name) is None:
            if self.streaming and self.header:
                self._write_test_case_header(class_name, self.stream)

            self._test_cases[class_name] = []
            if self.combined:
                self.combined_test_cases_seen.append(class_name)

    def add_ok(self, class_name, description, directive=''):
        result = Result(
            ok=True, number=self._get_next_line_number(class_name),
            description=description)
        self._add_line(class_name, result)

    def add_not_ok(
            self, class_name, description, directive=None, diagnostics=None):
        result = Result(
            ok=False, number=self._get_next_line_number(class_name),
            description=description, diagnostics=diagnostics)
        self._add_line(class_name, result)

    def add_skip(self, class_name, description, reason):
        directive = 'SKIP {0}'.format(reason)
        result = Result(
            ok=True, number=self._get_next_line_number(class_name),
            description=description, directive=Directive(directive))
        self._add_line(class_name, result)

    def _add_line(self, class_name, result):
        self._track(class_name)
        if self.streaming:
            print(result, file=self.stream)
        self._test_cases[class_name].append(result)

    def _get_next_line_number(self, class_name):
        if self.combined or self.streaming:
            # This has an obvious side effect. Oh well.
            self.combined_line_number += 1
            return self.combined_line_number
        else:
            try:
                return len(self._test_cases[class_name]) + 1
            except KeyError:
                # A result is created before the call to _track so the test
                # case may not be tracked yet. In that case, the line is 1.
                return 1

    def generate_tap_reports(self):
        """Generate TAP reports.

        The results are either combined into a single output file or
        the output file name is generated from the test case.
        """
        if self.streaming:
            # The results already went to the stream, record the plan.
            print('1..{0}'.format(self.combined_line_number), file=self.stream)
            return

        if self.combined:
            combined_file = 'testresults.tap'
            if self.outdir:
                combined_file = os.path.join(self.outdir, combined_file)
            with open(combined_file, 'w') as out_file:
                for test_case in self.combined_test_cases_seen:
                    self.generate_tap_report(
                        test_case, self._test_cases[test_case], out_file)
                print(
                    '1..{0}'.format(self.combined_line_number), file=out_file)
        else:
            for test_case, tap_lines in self._test_cases.items():
                with open(self._get_tap_file_path(test_case), 'w') as out_file:
                    self.generate_tap_report(test_case, tap_lines, out_file)

    def generate_tap_report(self, test_case, tap_lines, out_file):
        self._write_test_case_header(test_case, out_file)

        for tap_line in tap_lines:
            print(tap_line, file=out_file)

        # For combined results, the plan is only output once after
        # all the test cases complete.
        if not self.combined:
            print('1..{0}'.format(len(tap_lines)), file=out_file)

    def _write_test_case_header(self, test_case, stream):
        print(_('# TAP results for {test_case}').format(
            test_case=test_case), file=stream)

    def _get_tap_file_path(self, test_case):
        """Get the TAP output file path for the test case."""
        sanitized_test_case = test_case.translate(self._sanitized_table)
        tap_file = sanitized_test_case + '.tap'
        if self.outdir:
            return os.path.join(self.outdir, tap_file)
        return tap_file
