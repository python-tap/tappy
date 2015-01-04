# Copyright (c) 2014, Matt Layman

import unittest

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
