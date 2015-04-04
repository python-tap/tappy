# Copyright (c) 2015, Matt Layman

import sys

try:
    from unittest import mock
except ImportError:
    import mock

from tap.adapter import Adapter
from tap.tests import TestCase


class TestAdapter(TestCase):
    """Tests for tap.adapter.Adapter"""

    def test_adapter_has_filename(self):
        """The adapter has a TAP filename."""
        tap_filename = 'fake.tap'
        adapter = Adapter(tap_filename, None)

        self.assertEqual(tap_filename, adapter._filename)

    def test_handles_ok_test_line(self):
        """Add a success for an ok test line."""
        ok_line = self.factory.make_ok()
        adapter = Adapter('fake.tap', ok_line)
        result = mock.Mock()

        adapter(result)

        self.assertTrue(result.addSuccess.called)

    def test_handles_skip_test_line(self):
        """Add a skip when a test line contains a skip directive."""
        # Don't test on Python 2.6.
        if sys.version_info[0] == 2 and sys.version_info[1] == 6:
            return

        skip_line = self.factory.make_ok(
            directive_text='SKIP This is the reason.')
        adapter = Adapter('fake.tap', skip_line)
        result = self.factory.make_test_result()

        adapter(result)

        self.assertEqual(1, len(result.skipped))
        self.assertEqual('This is the reason.', result.skipped[0][1])

    def test_handles_ok_todo_test_line(self):
        """Add an unexpected success for an ok todo test line."""
        # Don't test on Python 2.6.
        if sys.version_info[0] == 2 and sys.version_info[1] == 6:
            return

        todo_line = self.factory.make_ok(
            directive_text='TODO An incomplete test')
        adapter = Adapter('fake.tap', todo_line)
        result = self.factory.make_test_result()

        adapter(result)

        self.assertEqual(1, len(result.unexpectedSuccesses))

    def test_handles_not_ok_todo_test_line(self):
        """Add an expected failure for a not ok todo test line."""
        # Don't test on Python 2.6.
        if sys.version_info[0] == 2 and sys.version_info[1] == 6:
            return

        todo_line = self.factory.make_not_ok(
            directive_text='TODO An incomplete test')
        adapter = Adapter('fake.tap', todo_line)
        result = self.factory.make_test_result()

        adapter(result)

        self.assertEqual(1, len(result.expectedFailures))
