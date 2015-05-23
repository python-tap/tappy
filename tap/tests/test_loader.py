# Copyright (c) 2015, Matt Layman

import inspect
import os
import tempfile

from tap.i18n import _
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

        # The bail line counts as a failed test.
        self.assertEqual(3, len(suite._tests))

    def test_file_does_not_exist(self):
        """The loader records a failure when a file does not exist."""
        loader = Loader()

        suite = loader.load_suite_from_file('phony.tap')

        self.assertEqual(1, len(suite._tests))
        self.assertEqual(
            _('{filename} does not exist.').format(filename='phony.tap'),
            suite._tests[0]._line.description)

    def test_handles_directory(self):
        directory = tempfile.mkdtemp()
        sub_directory = os.path.join(directory, 'sub')
        os.mkdir(sub_directory)
        with open(os.path.join(directory, 'a_file.tap'), 'w') as f:
            f.write('ok A passing test')
        with open(os.path.join(sub_directory, 'another_file.tap'), 'w') as f:
            f.write('not ok A failing test')
        loader = Loader()

        suite = loader.load([directory])

        self.assertEqual(2, len(suite._tests))

    def test_errors_with_multiple_version_lines(self):
        sample = inspect.cleandoc(
            """TAP version 13
            TAP version 13
            1..0
            """)
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(sample.encode('utf-8'))
        temp.close()
        loader = Loader()

        suite = loader.load_suite_from_file(temp.name)

        self.assertEqual(1, len(suite._tests))
        self.assertEqual(
            _('Multiple version lines appeared.'),
            suite._tests[0]._line.description)

    def test_errors_with_version_not_on_first_line(self):
        sample = inspect.cleandoc(
            """# Something that doesn't belong.
            TAP version 13
            1..0
            """)
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(sample.encode('utf-8'))
        temp.close()
        loader = Loader()

        suite = loader.load_suite_from_file(temp.name)

        self.assertEqual(1, len(suite._tests))
        self.assertEqual(
            _('The version must be on the first line.'),
            suite._tests[0]._line.description)

    def test_skip_plan_aborts_loading(self):
        sample = inspect.cleandoc(
            """1..0 # Skipping this test file.
            ok This should not get processed.
            """)
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(sample.encode('utf-8'))
        temp.close()
        loader = Loader()

        suite = loader.load_suite_from_file(temp.name)

        self.assertEqual(1, len(suite._tests))
        self.assertEqual(
            'Skipping this test file.', suite._tests[0]._line.description)
