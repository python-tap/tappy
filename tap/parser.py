# Copyright (c) 2014, Matt Layman

import re

from tap.directive import Directive
from tap.line import Bail, Diagnostic, Result, Unknown


class Parser(object):
    """A parser for TAP files and lines."""

    # ok and not ok share most of the same characteristics.
    result_base = r"""
        \s*                    # Optional whitespace.
        (?P<number>\d*)        # Optional test number.
        \s*                    # Optional whitespace.
        (?P<description>[^#]*) # Optional description before #.
        \#?                    # Optional directive marker.
        \s*                    # Optional whitespace.
        (?P<directive>.*)      # Optional directive text.
    """
    ok = re.compile(r'^ok' + result_base, re.VERBOSE)
    not_ok = re.compile(r'^not\ ok' + result_base, re.VERBOSE)
    diagnostic = re.compile(r'^#')
    bail = re.compile(r"""
        ^Bail\ out!
        \s*            # Optional whitespace.
        (?P<reason>.*) # Optional reason.
    """, re.VERBOSE)

    def parse_line(self, text):
        """Parse a line into whatever TAP category it belongs."""
        match = self.ok.match(text)
        if match:
            return self.parse_result(True, match)

        match = self.not_ok.match(text)
        if match:
            return self.parse_result(False, match)

        if self.diagnostic.match(text):
            return Diagnostic(text)

        match = self.bail.match(text)
        if match:
            return Bail(match.group('reason'))

        # TODO: Integrate with all the other line types.
        return Unknown()

    def parse_result(self, ok, match):
        """Parse a matching result line into a result instance."""
        return Result(
            ok, match.group('number'), match.group('description').strip(),
            Directive(match.group('directive')))
