# Copyright (c) 2014, Matt Layman

import re

from tap.directive import Directive
from tap.line import Bail, Diagnostic, Result, Unknown, Version


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
    version = re.compile(r'^TAP version (?P<version>\d+)$')

    TAP_MINIMUM_DECLARED_VERSION = 13

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

        match = self.version.match(text)
        if match:
            return self.parse_version(match)

        # TODO: Integrate with all the other line types.
        return Unknown()

    def parse_result(self, ok, match):
        """Parse a matching result line into a result instance."""
        return Result(
            ok, match.group('number'), match.group('description').strip(),
            Directive(match.group('directive')))

    def parse_version(self, match):
        version = int(match.group('version'))
        if version < self.TAP_MINIMUM_DECLARED_VERSION:
            raise ValueError('It is an error to explicitly specify '
                             'any version lower than 13.')
        return Version(version)

# TODO: Introduce a Rules class that will track and enforce critical state
# during parsing of a TAP file (e.g., position of the plan line).
