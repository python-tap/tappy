# Copyright (c) 2014, Matt Layman

import inspect
import tempfile

from tap.loader import Loader
from tap.tests import TestCase


class TestLoader(TestCase):
    """Tests for tap.loader.Loader"""

    def test_handles_file(self):
        """The loader handles a file."""
        sample = inspect.cleandoc(
            """TAP version 13
            1..2
            # This is a diagnostic.
            ok 1 A passing test
            not ok 2 A failing test
            This is an unknown line.
            Bail out! This test would abort.
            """)
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(sample.encode('utf-8'))
        temp.close()
        loader = Loader()

        suite = loader.load_suite_from_file(temp.name)

        self.assertEqual(2, len(suite._tests))

    def test_file_does_not_exist(self):
        """The loader records a failure when a file does not exist."""
        loader = Loader()

        suite = loader.load_suite_from_file('phony.tap')

        self.assertEqual(1, len(suite._tests))
        self.assertEqual(
            'phony.tap does not exist.', suite._tests[0]._line.description)
