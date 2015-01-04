# Copyright (c) 2014, Matt Layman

from tap.adapter import Adapter
from tap.directive import Directive
from tap.line import Result


class Rules(object):

    def __init__(self, filename, suite):
        self._filename = filename
        self._suite = suite
        self._lines_seen = {'plan': [], 'version': []}

    def check(self):
        """Check the status of all provided data and update the suite."""
        if self._lines_seen['version']:
            self._process_version_lines()

    def _process_version_lines(self):
        """Process version line rules."""
        if len(self._lines_seen['version']) > 1:
            self._add_error('Multiple version lines appeared.')
        elif self._lines_seen['version'][0] != 1:
            self._add_error('The version must be on the first line.')

    def handle_file_does_not_exist(self):
        """Handle a test file that does not exist."""
        self._add_error('{0} does not exist.'.format(self._filename))

    def handle_skipping_plan(self, skip_plan):
        """Handle a plan that contains a SKIP directive."""
        skip_line = Result(
            True, None, skip_plan.directive.text, Directive('SKIP'))
        self._suite.addTest(Adapter(self._filename, skip_line))

    def saw_version_at(self, line_counter):
        """Record when a version line was seen."""
        self._lines_seen['version'].append(line_counter)

    def _add_error(self, message):
        """Add an error test to the suite."""
        error_line = Result(False, None, message, Directive(''))
        self._suite.addTest(Adapter(self._filename, error_line))
