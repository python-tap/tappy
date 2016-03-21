# Copyright (c) 2016, Matt Layman

import os
import sys

try:
    from unittest import SkipTest
except ImportError:  # pragma: no cover
    class SkipTest(object):
        """SkipTest does not exist earlier than Python 2.7"""
        pass

from nose.plugins import Plugin
from nose.suite import ContextSuite

from tap import formatter
from tap.i18n import _
from tap.tracker import Tracker


class DummyStream(object):
    def write(self, *args):
        pass

    def writeln(self, *args):
        pass

    def flush(self):
        pass


class TAP(Plugin):
    """This plugin provides test results in the Test Anything Protocol format.
    """
    name = 'tap'

    def options(self, parser, env=os.environ):
        super(TAP, self).options(parser, env=env)
        parser.add_option(
            '--tap-stream', default=False, action='store_true',
            help=_('Stream TAP output instead of the default test runner'
                   ' output.'))
        parser.add_option(
            '--tap-outdir', metavar='PATH', help=_(
                'An optional output directory to write TAP files to. '
                'If the directory does not exist, it will be created.'))
        parser.add_option(
            '--tap-combined', default=False, action='store_true',
            help=_('Store all TAP test results into a combined output file.'))
        parser.add_option(
            '--tap-format', default='', metavar='FORMAT',
            help=_(
                'An optional format string for the TAP output.'
                ' The format options are:'
                ' {short_description} for the short description, and'
                ' {method_name} for the test method name.'))

    def configure(self, options, conf):
        super(TAP, self).configure(options, conf)
        if self.enabled:
            self.tracker = Tracker(
                outdir=options.tap_outdir, combined=options.tap_combined,
                streaming=options.tap_stream)
        self._format = options.tap_format

    def finalize(self, results):
        self.tracker.generate_tap_reports()

    def setOutputStream(self, stream):
        # When streaming is on, hijack the stream and return a dummy to send
        # standard nose output to oblivion.
        if self.tracker.streaming:
            self.tracker.stream = stream
            return DummyStream()
        return stream

    def addError(self, test, err):
        err_cls, reason, _ = err
        if err_cls != SkipTest:
            diagnostics = formatter.format_exception(err)
            self.tracker.add_not_ok(
                self._cls_name(test), self._description(test),
                diagnostics=diagnostics)
        else:
            self.tracker.add_skip(
                self._cls_name(test), self._description(test), reason)

    def addFailure(self, test, err):
        diagnostics = formatter.format_exception(err)
        self.tracker.add_not_ok(
            self._cls_name(test), self._description(test),
            diagnostics=diagnostics)

    def addSuccess(self, test):
        self.tracker.add_ok(self._cls_name(test), self._description(test))

    def _cls_name(self, test):
        if isinstance(test, ContextSuite):
            # In the class setup and teardown, test is a ContextSuite
            # instead of a test case. Grab the name from the context.
            return test.context.__name__
        else:
            # nose masks the true test case name so the real class name
            # is found under the test attribute.
            return test.test.__class__.__name__

    def _description(self, test):
        if self._format:
            try:
                return self._format.format(
                    method_name=str(test),
                    short_description=test.shortDescription() or '')
            except KeyError:
                sys.exit(_(
                    'Bad format string: {format}\n'
                    'Replacement options are: {{short_description}} and '
                    '{{method_name}}').format(format=self._format))

        return test.shortDescription() or str(test)
