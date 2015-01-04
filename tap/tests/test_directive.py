# Copyright (c) 2015, Matt Layman

import unittest

from tap.directive import Directive


class TestDirective(unittest.TestCase):
    """Tests for tap.directive.Directive"""

    def test_finds_todo(self):
        text = 'ToDo This is something to do.'
        directive = Directive(text)

        self.assertTrue(directive.todo)

    def test_finds_simplest_todo(self):
        text = 'TODO'
        directive = Directive(text)

        self.assertTrue(directive.todo)

    def test_todo_has_boundary(self):
        """TAP spec indicates TODO directives must be on a boundary."""
        text = 'TODO: Not a TODO directive because of an immediate colon.'
        directive = Directive(text)

        self.assertFalse(directive.todo)

    def test_finds_skip(self):
        text = 'Skipping This is something to skip.'
        directive = Directive(text)

        self.assertTrue(directive.skip)

    def test_finds_simplest_skip(self):
        text = 'SKIP'
        directive = Directive(text)

        self.assertTrue(directive.skip)

    def test_skip_at_beginning(self):
        """Only match SKIP directives at the beginning."""
        text = 'This is not something to skip.'
        directive = Directive(text)

        self.assertFalse(directive.skip)
