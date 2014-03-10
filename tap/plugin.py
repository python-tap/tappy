# Copyright (c) 2014, Matt Layman

import os
from unittest import SkipTest

from nose.plugins import Plugin

from tap.tracker import Tracker


class TAP(Plugin):
    '''
    This plugin provides test results in the Test Anything Protocol format.
    '''
    name = 'tap'

    def options(self, parser, env=os.environ):
        super(TAP, self).options(parser, env=env)

    def configure(self, options, conf):
        super(TAP, self).configure(options, conf)
        if self.enabled:
            self.tracker = Tracker()

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
