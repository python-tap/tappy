# Copyright (c) 2014, Matt Layman

import os

try:
    from unittest import SkipTest
except ImportError:
    class SkipTest(object):
        '''SkipTest does not exist earlier than Python 2.7'''
        pass

from nose.plugins import Plugin

from tap.tracker import Tracker


class TAP(Plugin):
    '''
    This plugin provides test results in the Test Anything Protocol format.
    '''
    name = 'tap'

    def options(self, parser, env=os.environ):
        super(TAP, self).options(parser, env=env)
        parser.add_option(
            '--tap-outdir',
            help='An optional output directory to write TAP files to. If the'
                 ' directory does not exist, it will be created.')

    def configure(self, options, conf):
        super(TAP, self).configure(options, conf)
        if self.enabled:
            self.tracker = Tracker(outdir=options.tap_outdir)

    def finalize(self, results):
        self.tracker.generate_tap_reports()

    def addError(self, test, err):
        err_cls, reason, _ = err
        if err_cls != SkipTest:
            self.tracker.add_not_ok(
                self._cls_name(test), self._description(test))
        else:
            self.tracker.add_skip(
                self._cls_name(test), self._description(test), reason)

    def addFailure(self, test, err):
        self.tracker.add_not_ok(self._cls_name(test), self._description(test))

    def addSuccess(self, test):
        self.tracker.add_ok(self._cls_name(test), self._description(test))

    def _cls_name(self, test):
        # nose masks the true test case name so the real class name is found
        # under the test attribute.
        return test.test.__class__.__name__

    def _description(self, test):
        return test.shortDescription() or str(test)
