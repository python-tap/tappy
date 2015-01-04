# Copyright (c) 2014, Matt Layman

import os
import unittest

from tap.adapter import Adapter
from tap.directive import Directive
from tap.line import Result
from tap.parser import Parser


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

        if not os.path.exists(filename):
            self._add_error(
                filename, '{0} does not exist.'.format(filename), suite)
            return suite

        # Keep track of how many times plan and version lines are seen.
        lines_seen = {'plan': [], 'version': []}
        lines_counter = 0

        for line in self._parser.parse_file(filename):
            lines_counter += 1

            if line.category in self.ignored_lines:
                continue

            if line.category == 'test':
                suite.addTest(Adapter(filename, line))
            elif line.category == 'plan':
                # TODO: Deal with the plan specific logic.
                pass
            elif line.category == 'bail':
                # TODO: Abort further processing of the test case.
                pass
            elif line.category == 'version':
                lines_seen['version'].append(lines_counter)

        if lines_seen['version']:
            self._process_version_lines(lines_seen['version'], filename, suite)
        return suite

    def _add_error(self, filename, message, suite):
        """Add an error test to the suite."""
        error_line = Result(False, None, message, Directive(''))
        suite.addTest(Adapter(filename, error_line))

    def _find_tests_in_directory(self, directory, suite):
        """Find test files in the directory and add them to the suite."""
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                suite.addTest(self.load_suite_from_file(filepath))

    def _process_version_lines(self, version_lines, filename, suite):
        """Process version line rules."""
        if len(version_lines) > 1:
            self._add_error(
                filename, 'Multiple version lines appeared.', suite)
        elif version_lines[0] != 1:
            self._add_error(
                filename, 'The version must be on the first line.', suite)
