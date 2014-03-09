# Copyright (c) 2014, Matt Layman

import os

from nose.plugins import Plugin


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
            # TODO: implement plugin
            print "I should generate some TAP!"
