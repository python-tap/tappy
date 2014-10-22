# Copyright (c) 2014, Matt Layman

import os
import tempfile
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

    def test_generates_tap_reports_in_new_outdir(self):
        tempdir = tempfile.mkdtemp()
        outdir = os.path.join(tempdir, 'non', 'existent', 'path')
        tracker = Tracker(outdir=outdir)
        tracker.add_ok('FakeTestCase', 'I should be in the specified dir.')

        tracker.generate_tap_reports()

        tap_file = os.path.join(outdir, 'FakeTestCase.tap')
        self.assertTrue(os.path.exists(tap_file))

    def test_generates_tap_reports_in_existing_outdir(self):
        outdir = tempfile.mkdtemp()
        tracker = Tracker(outdir=outdir)
        tracker.add_ok('FakeTestCase', 'I should be in the specified dir.')

        tracker.generate_tap_reports()

        tap_file = os.path.join(outdir, 'FakeTestCase.tap')
        self.assertTrue(os.path.exists(tap_file))
