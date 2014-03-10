# Copyright (c) 2014, Matt Layman

import unittest

# There is some weird conflict with `TestLoader.discover` if `nose.case.Test`
# is imported directly. Importing `nose.case` works.
from nose import case

from tap.plugin import TAP


class FakeTestCase(object):

    def __call__(self):
        pass


class TestPlugin(unittest.TestCase):

    @classmethod
    def _make_one(cls):
        plugin = TAP()
        plugin.enabled = True
        plugin.configure(None, None)
        return plugin

    def test_adds_error(self):
        plugin = self._make_one()
        plugin.addError(case.Test(FakeTestCase()), (None, None, None))
        line = plugin.tracker._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'not ok')

    def test_adds_skip(self):
        plugin = self._make_one()
        plugin.addError(case.Test(
            FakeTestCase()), (unittest.SkipTest, 'a reason', None))
        line = plugin.tracker._test_cases['FakeTestCase'][0]
        self.assertEqual(line.directive, '# SKIP a reason')
