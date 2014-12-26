# Copyright (c) 2014, Matt Layman

from tap.parser import Parser


class Adapter(object):
    """The adapter parses a TAP file and updates unittest's results.

    It is an alternative to TestCase to collect TAP results.
    """

    def __init__(self, filename):
        self._filename = filename
        self._parser = Parser()

    def __call__(self, results):
        """Update test results with the lines in the TAP file.

        Provide the interface that TestCase provides to a suite or runner.
        """
        # TODO: Check if the file exists. Add error and abort if it doesn't.
        for line in self._parser.parse_file(self._filename):
            # TODO: Inspect line category and update results.
            pass
