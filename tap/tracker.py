# Copyright (c) 2014, Matt Layman

from __future__ import print_function
from collections import namedtuple

TAPLine = namedtuple('TAPLine', ['status', 'description', 'directive'])


class Tracker(object):

    def __init__(self):
        self._test_cases = {}

    def _track(self, class_name):
        '''Keep track of which test cases have executed.'''
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
