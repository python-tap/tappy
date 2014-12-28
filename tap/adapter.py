# Copyright (c) 2014, Matt Layman


class Adapter(object):
    """The adapter processes a TAP test line and updates a unittest result.

    It is an alternative to TestCase to collect TAP results.
    """

    def __init__(self, filename, line):
        self._filename = filename
        self._line = line

    def shortDescription(self):
        """Get the short description for verbeose results."""
        return self._line.description

    def __call__(self, result):
        """Update test result with the lines in the TAP file.

        Provide the interface that TestCase provides to a suite or runner.
        """
        # Each line counts as a test that needs to be "started."
        result.startTest(self)

        # TODO: Pass in a fake test case that has all the internal APIs.
        if self._line.skip:
            try:
                result.addSkip(None, self._line.directive.reason)
            except AttributeError:
                # Python 2.6 does not support skipping.
                result.addSuccess(None)
            return

        if self._line.todo:
            if self._line.ok:
                try:
                    result.addUnexpectedSuccess(None)
                except AttributeError:
                    # TODO: Set as addFailure with full directive text.
                    pass
            else:
                # TODO: make it work
                pass
            return

        if self._line.ok:
            result.addSuccess(None)
        else:
            # TODO: handle failure
            pass

    def __repr__(self):
        return '<file={filename}>'.format(filename=self._filename)
