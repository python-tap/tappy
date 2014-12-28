# Copyright (c) 2014, Matt Layman

import os
import unittest

from tap.adapter import Adapter
from tap.directive import Directive
from tap.line import Result
from tap.parser import Parser


class Loader(object):
    """Load TAP lines into unittest-able objects."""

    ignored_lines = set(['diagnostic', 'unknown', 'version'])

    def __init__(self):
        self._parser = Parser()

    def load(self, files):
        """Load any files found into a suite."""
        # TODO: Handle directories
        suite = unittest.TestSuite()
        for filename in files:
            suite.addTest(self.load_suite_from_file(filename))
        return suite

    def load_suite_from_file(self, filename):
        """Load a test suite with test lines from the provided TAP file."""
        suite = unittest.TestSuite()

        if not os.path.exists(filename):
            error_line = Result(
                False, 1, '{0} does not exist.'.format(filename),
                Directive(''))
            suite.addTest(Adapter(filename, error_line))
            return suite

        for line in self._parser.parse_file(filename):
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
        return suite
