# Copyright (c) 2016, Matt Layman

import unittest

from tap.i18n import _
from tap.rules import Rules
from tap.tests import TestCase


class TestRules(TestCase):
    """Tests for tap.rules.Rules"""

    def _make_one(self):
        self.suite = unittest.TestSuite()
        return Rules('foobar.tap', self.suite)

    def test_handles_skipping_plan(self):
        skip_plan = self.factory.make_plan(directive_text='Skip on Mondays.')
        rules = self._make_one()

        rules.handle_skipping_plan(skip_plan)

        self.assertEqual(1, len(self.suite._tests))
        self.assertEqual(
            'Skip on Mondays.', self.suite._tests[0]._line.description)

    def test_tracks_plan_line(self):
        plan = self.factory.make_plan()
        rules = self._make_one()

        rules.saw_plan(plan, 28)

        self.assertEqual(rules._lines_seen['plan'][0][0], plan)
        self.assertEqual(rules._lines_seen['plan'][0][1], 28)

    def test_errors_plan_not_at_end(self):
        plan = self.factory.make_plan()
        rules = self._make_one()
        rules.saw_plan(plan, 41)

        rules.check(42)

        self.assertEqual(
            _('A plan must appear at the beginning or end of the file.'),
            self.suite._tests[0]._line.description)

    def test_requires_plan(self):
        rules = self._make_one()

        rules.check(42)

        self.assertEqual(
            _('Missing a plan.'), self.suite._tests[0]._line.description)

    def test_only_one_plan(self):
        plan = self.factory.make_plan()
        rules = self._make_one()
        rules.saw_plan(plan, 41)
        rules.saw_plan(plan, 42)

        rules.check(42)

        self.assertEqual(
            _('Only one plan line is permitted per file.'),
            self.suite._tests[0]._line.description)

    def test_plan_line_two(self):
        """A plan may appear on line 2 when line 1 is a version line."""
        rules = self._make_one()
        rules.saw_version_at(1)

        valid = rules._plan_on_valid_line(at_line=2, final_line_count=42)

        self.assertTrue(valid)

    def test_errors_when_expected_tests_differs_from_actual(self):
        plan = self.factory.make_plan(expected_tests=42)
        rules = self._make_one()
        rules.saw_plan(plan, 1)
        rules.saw_test()

        rules.check(2)

        self.assertEqual(
            _('Expected {expected_count} tests but only '
              '{seen_count} ran.').format(expected_count=42, seen_count=1),
            self.suite._tests[0]._line.description)

    def test_errors_on_bail(self):
        bail = self.factory.make_bail(reason='Missing something important.')
        rules = self._make_one()

        rules.handle_bail(bail)

        self.assertEqual(1, len(self.suite._tests))
        self.assertEqual(
            _('Bailed: {reason}').format(
                reason='Missing something important.'),
            self.suite._tests[0]._line.description)
