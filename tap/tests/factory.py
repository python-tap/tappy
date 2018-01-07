# Copyright (c) 2018, Matt Layman and contributors

import sys
import tempfile
from unittest.runner import TextTestResult

from tap.directive import Directive
from tap.line import Bail, Plan, Result


class Factory(object):
    """A factory to produce commonly needed objects"""

    def make_ok(self, directive_text=''):
        return Result(
            True, 1, 'This is a description.', Directive(directive_text))

    def make_not_ok(self, directive_text=''):
        return Result(
            False, 1, 'This is a description.', Directive(directive_text))

    def make_bail(self, reason='Because it is busted.'):
        return Bail(reason)

    def make_plan(self, expected_tests=99, directive_text=''):
        return Plan(expected_tests, Directive(directive_text))

    def make_test_result(self):
        stream = tempfile.TemporaryFile(mode='w')
        return TextTestResult(stream, None, 1)

    def make_exc(self):
        """Make a traceback tuple.

        Doing this intentionally is not straight forward.
        """
        try:
            raise ValueError('boom')
        except ValueError:
            return sys.exc_info()
