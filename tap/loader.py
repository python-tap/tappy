# Copyright (c) 2015, Matt Layman

import os
import unittest

from tap.adapter import Adapter
from tap.parser import Parser
from tap.rules import Rules


class Loader(object):
    """Load TAP lines into unittest-able objects."""

    ignored_lines = set(['diagnostic', 'unknown'])

    def __init__(self):
        self._parser = Parser()

    def load(self, files):
        """Load any files found into a suite.

        Any directories are walked and their files are added as TAP files.

        :returns: A ``unittest.TestSuite`` instance
        """
        suite = unittest.TestSuite()
        for filepath in files:
            if os.path.isdir(filepath):
                self._find_tests_in_directory(filepath, suite)
            else:
                suite.addTest(self.load_suite_from_file(filepath))
        return suite

    def load_suite_from_file(self, filename):
        """Load a test suite with test lines from the provided TAP file.

        :returns: A ``unittest.TestSuite`` instance
        """
        suite = unittest.TestSuite()
        rules = Rules(filename, suite)

        if not os.path.exists(filename):
            rules.handle_file_does_not_exist()
            return suite

        line_counter = 0
        for line in self._parser.parse_file(filename):
            line_counter += 1

            if line.category in self.ignored_lines:
                continue

            if line.category == 'test':
                suite.addTest(Adapter(filename, line))
                rules.saw_test()
            elif line.category == 'plan':
                if line.skip:
                    rules.handle_skipping_plan(line)
                    return suite
                rules.saw_plan(line, line_counter)
            elif line.category == 'bail':
                rules.handle_bail(line)
                return suite
            elif line.category == 'version':
                rules.saw_version_at(line_counter)

        rules.check(line_counter)
        return suite

    def _find_tests_in_directory(self, directory, suite):
        """Find test files in the directory and add them to the suite."""
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                suite.addTest(self.load_suite_from_file(filepath))
