# Copyright (c) 2014, Matt Layman

from __future__ import print_function
from collections import namedtuple
import os

TAPLine = namedtuple('TAPLine', ['status', 'description', 'directive'])


class Tracker(object):

    def __init__(self, outdir=None):
        self._test_cases = {}
        self.outdir = outdir
        if outdir and not os.path.exists(outdir):
            os.makedirs(outdir)

    def _track(self, class_name):
        """Keep track of which test cases have executed."""
        if self._test_cases.get(class_name) is None:
            self._test_cases[class_name] = []

    def add_ok(self, class_name, description, directive=''):
        self._track(class_name)
        self._test_cases[class_name].append(
            TAPLine('ok', description, directive))

    def add_not_ok(self, class_name, description, directive=''):
        self._track(class_name)
        self._test_cases[class_name].append(
            TAPLine('not ok', description, directive))

    def add_skip(self, class_name, description, reason):
        directive = '# SKIP {0}'.format(reason)
        self.add_ok(class_name, description, directive)

    def generate_tap_reports(self):
        for test_case, tap_lines in self._test_cases.items():
            self.generate_tap_report(test_case, tap_lines)

    def generate_tap_report(self, test_case, tap_lines):
        with open(self._get_tap_file_path(test_case), 'w') as f:
            print('# TAP results for {0}'.format(test_case), file=f)

            for line_count, tap_line in enumerate(tap_lines, start=1):
                result = ' '.join([
                    tap_line.status,
                    str(line_count),
                    '-',
                    tap_line.description,
                    tap_line.directive,
                ])
                print(result, file=f)

            print('1..{0}'.format(len(tap_lines)), file=f)

    def _get_tap_file_path(self, test_case):
        """Get the TAP output file path for the test case."""
        tap_file = test_case + '.tap'
        if self.outdir:
            return os.path.join(self.outdir, tap_file)
        return tap_file
