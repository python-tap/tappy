# Copyright (c) 2014, Matt Layman

import tempfile
import unittest

from tap.adapter import Adapter


class TestAdapter(unittest.TestCase):
    """Tests for tap.adapter.Adapter"""

    def test_adapter_has_filename(self):
        """The adapter has a TAP filename."""
        tap_filename = 'fake.tap'
        adapter = Adapter(tap_filename)

        self.assertEqual(tap_filename, adapter._filename)

    def test_adapter_is_callable(self):
        """The adapter matches the call signature of a TestCase."""
        temp = tempfile.NamedTemporaryFile()
        adapter = Adapter(temp.name)
        results = None

        adapter(results)

        # No need to assert. If it was callable, the test passed.
