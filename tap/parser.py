# Copyright (c) 2018, Matt Layman and contributors

from io import StringIO
import itertools
import re
import sys

from tap.directive import Directive
from tap.i18n import _
from tap.line import Bail, Diagnostic, Plan, Result, Unknown, Version

try:
    from more_itertools import peekable
    import yaml  # noqa
    ENABLE_VERSION_13 = True
except ImportError:  # pragma: no cover
    ENABLE_VERSION_13 = False


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
    plan = re.compile(r"""
        ^1..(?P<expected>\d+) # Match the plan details.
        [^#]*                 # Consume any non-hash character to confirm only
                              # directives appear with the plan details.
        \#?                   # Optional directive marker.
        \s*                   # Optional whitespace.
        (?P<directive>.*)     # Optional directive text.
    """, re.VERBOSE)
    diagnostic = re.compile(r'^#')
    bail = re.compile(r"""
        ^Bail\ out!
        \s*            # Optional whitespace.
        (?P<reason>.*) # Optional reason.
    """, re.VERBOSE)
    version = re.compile(r'^TAP version (?P<version>\d+)$')

    yaml_block_start = re.compile(r'^(?P<indent>\s+)-')
    yaml_block_end = re.compile(r'^\s+\.\.\.')

    TAP_MINIMUM_DECLARED_VERSION = 13

    def __init__(self):
        self._try_peeking = False

    def parse_file(self, filename):
        """Parse a TAP file to an iterable of tap.line.Line objects.

        This is a generator method that will yield an object for each
        parsed line. The file given by `filename` is assumed to exist.
        """
        return self.parse(open(filename, 'r'))

    def parse_stdin(self):
        """Parse a TAP stream from standard input.

        Note: this has the side effect of closing the standard input
        filehandle after parsing.
        """
        return self.parse(sys.stdin)

    def parse_text(self, text):
        """Parse a string containing one or more lines of TAP output."""
        return self.parse(StringIO(text))

    def parse(self, fh):
        """Generate tap.line.Line objects, given a file-like object `fh`.

        `fh` may be any object that implements both the iterator and
        context management protocol (i.e. it can be used in both a
        "with" statement and a "for...in" statement.)

        Trailing whitespace and newline characters will be automatically
        stripped from the input lines.
        """
        with fh:
            try:
                first_line = next(fh)
            except StopIteration:
                return
            first_parsed = self.parse_line(first_line.rstrip())
            fh_new = itertools.chain([first_line], fh)
            if first_parsed.category == 'version' and \
                    first_parsed.version >= 13:
                if ENABLE_VERSION_13:
                    fh_new = peekable(itertools.chain([first_line], fh))
                    self._try_peeking = True
                else:  # pragma no cover
                    print("""
WARNING: Optional imports not found, TAP 13 output will be
    ignored. To parse yaml, see requirements in docs:
    https://tappy.readthedocs.io/en/latest/consumers.html#tap-version-13""")

            for line in fh_new:
                yield self.parse_line(line.rstrip(), fh_new)

    def parse_line(self, text, fh=None):
        """Parse a line into whatever TAP category it belongs."""
        match = self.ok.match(text)
        if match:
            return self._parse_result(True, match, fh)

        match = self.not_ok.match(text)
        if match:
            return self._parse_result(False, match, fh)

        if self.diagnostic.match(text):
            return Diagnostic(text)

        match = self.plan.match(text)
        if match:
            return self._parse_plan(match)

        match = self.bail.match(text)
        if match:
            return Bail(match.group('reason'))

        match = self.version.match(text)
        if match:
            return self._parse_version(match)

        return Unknown()

    def _parse_plan(self, match):
        """Parse a matching plan line."""
        expected_tests = int(match.group('expected'))
        directive = Directive(match.group('directive'))

        # Only SKIP directives are allowed in the plan.
        if directive.text and not directive.skip:
            return Unknown()

        return Plan(expected_tests, directive)

    def _parse_result(self, ok, match, fh=None):
        """Parse a matching result line into a result instance."""
        peek_match = None
        try:
            if fh is not None and self._try_peeking:
                peek_match = self.yaml_block_start.match(fh.peek())
        except StopIteration:
            pass
        if peek_match is None:
            return Result(
                ok,
                number=match.group('number'),
                description=match.group('description').strip(),
                directive=Directive(match.group('directive'))
            )
        indent = peek_match.group('indent')
        concat_yaml = self._extract_yaml_block(indent, fh)
        return Result(
            ok,
            number=match.group('number'),
            description=match.group('description').strip(),
            directive=Directive(match.group('directive')),
            raw_yaml_block=concat_yaml
        )

    def _extract_yaml_block(self, indent, fh):
        """Extract a raw yaml block from a file handler"""
        raw_yaml = []
        indent_match = re.compile(r'^{}'.format(indent))
        try:
            fh.next()
            while indent_match.match(fh.peek()):
                raw_yaml.append(fh.next().replace(indent, '', 1))
                # check for the end and stop adding yaml if encountered
                if self.yaml_block_end.match(fh.peek()):
                    fh.next()
                    break
        except StopIteration:
            pass
        return '\n'.join(raw_yaml)

    def _parse_version(self, match):
        version = int(match.group('version'))
        if version < self.TAP_MINIMUM_DECLARED_VERSION:
            raise ValueError(_('It is an error to explicitly specify '
                               'any version lower than 13.'))
        return Version(version)
