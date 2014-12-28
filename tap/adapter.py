# Copyright (c) 2014, Matt Layman

from tap.parser import Parser


class Adapter(object):
    """The adapter parses a TAP file and updates a unittest result.

    It is an alternative to TestCase to collect TAP results.
    """

    ignored_lines = set(['diagnostic', 'unknown', 'version'])

    def __init__(self, filename):
        self._filename = filename
        self._parser = Parser()

    def shortDescription(self):
        """Get the short description for verbeose results."""
        # TODO: Make the adapter work on one line and return its description.
        return 'Adapter instance'

    def __call__(self, result):
        """Update test result with the lines in the TAP file.

        Provide the interface that TestCase provides to a suite or runner.
        """
        # TODO: Check if the file exists. Add error and abort if it doesn't.
        for line in self._parser.parse_file(self._filename):

            if line.category in self.ignored_lines:
                continue

            handler = getattr(self, 'handle_' + line.category)
            handler(line, result)

    def handle_test(self, line, result):
        # Each line counts as a test that needs to be "started."
        result.startTest(self)

        # TODO: Pass in a fake test case that has all the internal APIs.
        """Handle a test result line."""
        if line.skip:
            try:
                result.addSkip(None, line.directive.reason)
            except AttributeError:
                # Python 2.6 does not support skipping.
                result.addSuccess(None)
            return

        if line.todo:
            if line.ok:
                try:
                    result.addUnexpectedSuccess(None)
                except AttributeError:
                    # TODO: Set as addFailure with full directive text.
                    pass
            else:
                # TODO: make it work
                pass
            return

        if line.ok:
            result.addSuccess(None)
        else:
            # TODO: handle failure
            pass

    def handle_plan(self, line, result):
        """Handle a plan line."""
        # TODO: Deal with the plan specific logic.

    def handle_bail(self, line, result):
        """Handle a plan line."""
        # TODO: Abort further processing of the test case.

    def __repr__(self):
        return '<file={filename}>'.format(filename=self._filename)
