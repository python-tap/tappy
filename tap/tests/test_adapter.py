# Copyright (c) 2014, Matt Layman

import sys

import mock

from tap.adapter import Adapter
from tap.tests import TestCase


class TestAdapter(TestCase):
    """Tests for tap.adapter.Adapter"""

    def test_adapter_has_filename(self):
        """The adapter has a TAP filename."""
        tap_filename = 'fake.tap'
        adapter = Adapter(tap_filename)

        self.assertEqual(tap_filename, adapter._filename)

    def test_handles_ok_test_line(self):
        """Add a success for an ok test line."""
        adapter = Adapter(None)
        result = mock.Mock()
        ok_line = self.factory.make_ok()

        adapter.handle_test(ok_line, result)

        self.assertTrue(result.addSuccess.called)

    def test_handles_skip_test_line(self):
        """Add a skip when a test line contains a skip directive."""
        # Don't test on Python 2.6.
        if sys.version_info[0] == 2 and sys.version_info[1] == 6:
            return

        adapter = Adapter(None)
        result = self.factory.make_test_result()
        skip_line = self.factory.make_ok(
            directive_text='SKIP This is the reason.')

        adapter.handle_test(skip_line, result)

        self.assertEqual(1, len(result.skipped))
        self.assertEqual('This is the reason.', result.skipped[0][1])

    def test_handles_ok_todo_test_line(self):
        """Add an unexpected success for an ok todo test line."""
        # Don't test on Python 2.6.
        if sys.version_info[0] == 2 and sys.version_info[1] == 6:
            return

        adapter = Adapter(None)
        result = self.factory.make_test_result()
        todo_line = self.factory.make_ok(
            directive_text='TODO An incomplete test')

        adapter.handle_test(todo_line, result)

        self.assertEqual(1, len(result.unexpectedSuccesses))
