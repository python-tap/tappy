# Copyright (c) 2016, Matt Layman

import tempfile
try:
    from unittest.runner import TextTestResult
except ImportError:
    # Support Python 2.6.
    from unittest import _TextTestResult as TextTestResult

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
