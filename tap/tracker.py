# Copyright (c) 2015, Matt Layman

from __future__ import print_function
import os

from tap.directive import Directive
from tap.line import Result


class Tracker(object):

    def __init__(self, outdir=None):
        self._test_cases = {}
        self.outdir = outdir

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
        return len(self._test_cases[class_name]) + 1

    def generate_tap_reports(self):
        for test_case, tap_lines in self._test_cases.items():
            self.generate_tap_report(test_case, tap_lines)

    def generate_tap_report(self, test_case, tap_lines):
        with open(self._get_tap_file_path(test_case), 'w') as f:
            print('# TAP results for {0}'.format(test_case), file=f)

            for tap_line in tap_lines:
                print(tap_line, file=f)

            print('1..{0}'.format(len(tap_lines)), file=f)

    def _get_tap_file_path(self, test_case):
        """Get the TAP output file path for the test case."""
        tap_file = test_case + '.tap'
        if self.outdir:
            return os.path.join(self.outdir, tap_file)
        return tap_file
