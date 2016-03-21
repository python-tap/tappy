# Copyright (c) 2016, Matt Layman


class Line(object):
    """Base type for TAP data.

    TAP is a line based protocol. Thus, the most primitive type is a line.
    """
    @property
    def category(self):
        raise NotImplementedError


class Result(Line):
    """Information about an individual test line."""

    def __init__(
            self, ok, number=None, description='', directive=None,
            diagnostics=None):
        self._ok = ok
        if number:
            self._number = int(number)
        else:
            # The number may be an empty string so explicitly set to None.
            self._number = None
        self._description = description
        self.directive = directive
        self.diagnostics = diagnostics

    @property
    def category(self):
        """:returns: ``test``"""
        return 'test'

    @property
    def ok(self):
        """Get the ok status.

        :rtype: bool
        """
        return self._ok

    @property
    def number(self):
        """Get the test number.

        :rtype: int
        """
        return self._number

    @property
    def description(self):
        """Get the description."""
        return self._description

    @property
    def skip(self):
        """Check if this test was skipped.

        :rtype: bool
        """
        return self.directive.skip

    @property
    def todo(self):
        """Check if this test was a TODO.

        :rtype: bool
        """
        return self.directive.todo

    def __str__(self):
        is_not = ''
        if not self.ok:
            is_not = 'not '
        directive = ''
        if self.directive is not None:
            directive = ' # {0}'.format(self.directive.text)
        diagnostics = ''
        if self.diagnostics is not None:
            diagnostics = '\n' + self.diagnostics.rstrip()
        return "{0}ok {1} - {2}{3}{4}".format(
            is_not, self.number, self.description, directive, diagnostics)


class Plan(Line):
    """A plan line to indicate how many tests to expect."""

    def __init__(self, expected_tests, directive=None):
        self._expected_tests = expected_tests
        self.directive = directive

    @property
    def category(self):
        """:returns: ``plan``"""
        return 'plan'

    @property
    def expected_tests(self):
        """Get the number of expected tests.

        :rtype: int
        """
        return self._expected_tests

    @property
    def skip(self):
        """Check if this plan should skip the file.

        :rtype: bool
        """
        return self.directive.skip


class Diagnostic(Line):
    """A diagnostic line (i.e. anything starting with a hash)."""

    def __init__(self, text):
        self._text = text

    @property
    def category(self):
        """:returns: ``diagnostic``"""
        return 'diagnostic'

    @property
    def text(self):
        """Get the text."""
        return self._text


class Bail(Line):
    """A bail out line (i.e. anything starting with 'Bail out!')."""

    def __init__(self, reason):
        self._reason = reason

    @property
    def category(self):
        """:returns: ``bail``"""
        return 'bail'

    @property
    def reason(self):
        """Get the reason."""
        return self._reason


class Version(Line):
    """A version line (i.e. of the form 'TAP version 13')."""

    def __init__(self, version):
        self._version = version

    @property
    def category(self):
        """:returns: ``version``"""
        return 'version'

    @property
    def version(self):
        """Get the version number.

        :rtype: int
        """
        return self._version


class Unknown(Line):
    """A line that represents something that is not a known TAP line.

    This exists for the purpose of a Null Object pattern.
    """
    @property
    def category(self):
        """:returns: ``unknown``"""
        return 'unknown'
