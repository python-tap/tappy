# Copyright (c) 2016, Matt Layman


class Adapter(object):
    """The adapter processes a TAP test line and updates a unittest result.

    It is an alternative to TestCase to collect TAP results.
    """
    failureException = AssertionError

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
        result.startTest(self)

        if self._line.skip:
            try:
                result.addSkip(None, self._line.directive.reason)
            except AttributeError:
                # Python 2.6 does not support skipping.
                result.addSuccess(self)
            return

        if self._line.todo:
            if self._line.ok:
                try:
                    result.addUnexpectedSuccess(self)
                except AttributeError:
                    # Python 2.6 does not support unexpected success.
                    self.addFailure(result)
            else:
                try:
                    result.addExpectedFailure(
                        self, (Exception, Exception(), None))
                except AttributeError:
                    # Python 2.6 does not support expected failures.
                    result.addSuccess(self)
            return

        if self._line.ok:
            result.addSuccess(self)
        else:
            self.addFailure(result)

    def addFailure(self, result):
        """Add a failure to the result."""
        result.addFailure(self, (Exception, Exception(), None))
        # Since TAP will not provide assertion data, clean up the assertion
        # section so it is not so spaced out.
        test, err = result.failures[-1]
        result.failures[-1] = (test, '')

    def __repr__(self):
        return '<file={filename}>'.format(filename=self._filename)
