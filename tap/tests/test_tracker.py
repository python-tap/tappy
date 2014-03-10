# Copyright (c) 2014, Matt Layman

import unittest

from tap.tracker import Tracker


class TestTracker(unittest.TestCase):

    def test_has_test_cases(self):
        tracker = Tracker()
        self.assertEqual(tracker._test_cases, {})

    def test_tracks_class(self):
        tracker = Tracker()
        tracker._track('FakeTestClass')
        self.assertEqual(tracker._test_cases.get('FakeTestClass'), [])

    def test_adds_ok(self):
        tracker = Tracker()
        tracker.add_ok('FakeTestCase', 'a description')
        line = tracker._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'ok')
        self.assertEqual(line.description, 'a description')
        self.assertEqual(line.directive, '')

    def test_adds_not_ok(self):
        tracker = Tracker()
        tracker.add_not_ok('FakeTestCase', 'a description')
        line = tracker._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'not ok')
        self.assertEqual(line.description, 'a description')
        self.assertEqual(line.directive, '')

    def test_adds_skip(self):
        tracker = Tracker()
        tracker.add_skip('FakeTestCase', 'a description', 'a reason')
        line = tracker._test_cases['FakeTestCase'][0]
        self.assertEqual(line.status, 'ok')
        self.assertEqual(line.description, 'a description')
        self.assertEqual(line.directive, '# SKIP a reason')
