# Copyright (c) 2015, Matt Layman

from __future__ import print_function
import os

from tap.directive import Directive
from tap.line import Result


class Tracker(object):

    def __init__(self, outdir=None, combined=False):
        self._test_cases = {}
        self.outdir = outdir
        # Combine all the test results into one file.
        self.combined = combined
        self.combined_line_number = 0
        # Test case ordering is important for the combined results
        # because of how numbers are assigned. The test cases
        # must be tracked in order so that reporting can sequence
        # the line numbers properly.
        self.combined_test_cases_seen = []

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
            self._test_cases[class_name] = []
            if self.combined:
                self.combined_test_cases_seen.append(class_name)

    def add_ok(self, class_name, description, directive=''):
        self._track(class_name)
        self._test_cases[class_name].append(
            Result(
                ok=True, number=self._get_next_line_number(class_name),
                description=description))

    def add_not_ok(self, class_name, description, directive=''):
        self._track(class_name)
        self._test_cases[class_name].append(
            Result(
                ok=False, number=self._get_next_line_number(class_name),
                description=description))

    def add_skip(self, class_name, description, reason):
        self._track(class_name)
        directive = 'SKIP {0}'.format(reason)
        self._test_cases[class_name].append(
            Result(
                ok=True, number=self._get_next_line_number(class_name),
                description=description, directive=Directive(directive)))

    def _get_next_line_number(self, class_name):
        if self.combined:
            # This has an obvious side effect. Oh well.
            self.combined_line_number += 1
            return self.combined_line_number
        else:
            return len(self._test_cases[class_name]) + 1

    def generate_tap_reports(self):
        """Generate TAP reports.

        The results are either combined into a single output file or
        the output file name is generated from the test case.
        """
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
        print('# TAP results for {0}'.format(test_case), file=out_file)

        for tap_line in tap_lines:
            print(tap_line, file=out_file)

        # For combined results, the plan is only output once after
        # all the test cases complete.
        if not self.combined:
            print('1..{0}'.format(len(tap_lines)), file=out_file)

    def _get_tap_file_path(self, test_case):
        """Get the TAP output file path for the test case."""
        tap_file = test_case + '.tap'
        if self.outdir:
            return os.path.join(self.outdir, tap_file)
        return tap_file
