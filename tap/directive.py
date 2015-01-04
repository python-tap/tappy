# Copyright (c) 2015, Matt Layman

import re


class Directive(object):
    """A representation of a result line directive."""

    skip_pattern = re.compile(
        r"""^SKIP\S*
            (?P<whitespace>\s*) # Optional whitespace.
            (?P<reason>.*)      # Slurp up the rest.""",
        re.IGNORECASE | re.VERBOSE)
    todo_pattern = re.compile(
        r"""^TODO\b             # The directive name
            (?P<whitespace>\s*) # Immediately following must be whitespace.
            (?P<reason>.*)      # Slurp up the rest.""",
        re.IGNORECASE | re.VERBOSE)

    def __init__(self, text):
        """Initialize the directive by parsing the text.

        The text is assumed to be everything after a '#\s*' on a result line.
        """
        self._text = text
        self._skip = False
        self._todo = False
        self._reason = None

        match = self.skip_pattern.match(text)
        if match:
            self._skip = True
            self._reason = match.group('reason')

        match = self.todo_pattern.match(text)
        if match:
            if match.group('whitespace'):
                self._todo = True
            else:
                # Catch the case where the directive has no descriptive text.
                if match.group('reason') == '':
                    self._todo = True
            self._reason = match.group('reason')

    @property
    def text(self):
        """Get the entire text."""
        return self._text

    @property
    def skip(self):
        """Check if the directive is a SKIP type."""
        return self._skip

    @property
    def todo(self):
        """Check if the directive is a TODO type."""
        return self._todo

    @property
    def reason(self):
        """Get the reason for the directive."""
        return self._reason
