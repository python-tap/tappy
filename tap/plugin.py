# Copyright (c) 2014, Matt Layman

import os

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
        self.tracker.add_not_ok(self._cls_name(test), self._description(test))

    def addFailure(self, test, err):
        self.tracker.add_not_ok(self._cls_name(test), self._description(test))

    def addSkip(self, test, reason):
        # TODO: deprecated in nose. Figure out what the Skip class is.
        self.tracker.add_skip(self._cls_name(test), self._description(test),
                              reason)

    def addSuccess(self, test):
        self.tracker.add_ok(self._cls_name(test), self._description(test))

    def _cls_name(self, test):
        return test.test.__class__.__name__

    def _description(self, test):
        return test.shortDescription() or str(test)
