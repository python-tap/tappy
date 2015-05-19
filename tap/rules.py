# Copyright (c) 2015, Matt Layman

from tap.adapter import Adapter
from tap.directive import Directive
from tap.i18n import _
from tap.line import Result


class Rules(object):

    def __init__(self, filename, suite):
        self._filename = filename
        self._suite = suite
        self._lines_seen = {'plan': [], 'test': 0, 'version': []}

    def check(self, final_line_count):
        """Check the status of all provided data and update the suite."""
        if self._lines_seen['version']:
            self._process_version_lines()
        self._process_plan_lines(final_line_count)

    def _process_version_lines(self):
        """Process version line rules."""
        if len(self._lines_seen['version']) > 1:
            self._add_error(_('Multiple version lines appeared.'))
        elif self._lines_seen['version'][0] != 1:
            self._add_error(_('The version must be on the first line.'))

    def _process_plan_lines(self, final_line_count):
        """Process plan line rules."""
        if not self._lines_seen['plan']:
            self._add_error(_('Missing a plan.'))
            return

        if len(self._lines_seen['plan']) > 1:
            self._add_error(_('Only one plan line is permitted per file.'))
            return

        plan, at_line = self._lines_seen['plan'][0]
        if not self._plan_on_valid_line(at_line, final_line_count):
            self._add_error(
                _('A plan must appear at the beginning or end of the file.'))
            return

        if plan.expected_tests != self._lines_seen['test']:
            self._add_error(_(
                'Expected {expected_count} tests '
                'but only {seen_count} ran.').format(
                    expected_count=plan.expected_tests,
                    seen_count=self._lines_seen['test']))

    def _plan_on_valid_line(self, at_line, final_line_count):
        """Check if a plan is on a valid line."""
        # Put the common cases first.
        if at_line == 1 or at_line == final_line_count:
            return True

        # The plan may only appear on line 2 if the version is at line 1.
        after_version = (
            self._lines_seen['version'] and
            self._lines_seen['version'][0] == 1 and
            at_line == 2)
        if after_version:
            return True

        return False

    def handle_bail(self, bail):
        """Handle a bail line."""
        self._add_error(_('Bailed: {reason}').format(reason=bail.reason))

    def handle_file_does_not_exist(self):
        """Handle a test file that does not exist."""
        self._add_error(_('{filename} does not exist.').format(
            filename=self._filename))

    def handle_skipping_plan(self, skip_plan):
        """Handle a plan that contains a SKIP directive."""
        skip_line = Result(
            True, None, skip_plan.directive.text, Directive('SKIP'))
        self._suite.addTest(Adapter(self._filename, skip_line))

    def saw_plan(self, plan, at_line):
        """Record when a plan line was seen."""
        self._lines_seen['plan'].append((plan, at_line))

    def saw_test(self):
        """Record when a test line was seen."""
        self._lines_seen['test'] += 1

    def saw_version_at(self, line_counter):
        """Record when a version line was seen."""
        self._lines_seen['version'].append(line_counter)

    def _add_error(self, message):
        """Add an error test to the suite."""
        error_line = Result(False, None, message, Directive(''))
        self._suite.addTest(Adapter(self._filename, error_line))
