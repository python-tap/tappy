# Copyright (c) 2015, Matt Layman

import inspect
import os
import tempfile
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from tap.tests import TestCase
from tap.tracker import Tracker


class TestTracker(TestCase):

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
        self.assertTrue(line.ok)
        self.assertEqual(line.description, 'a description')

    def test_adds_not_ok(self):
        tracker = Tracker()
        tracker.add_not_ok('FakeTestCase', 'a description')
        line = tracker._test_cases['FakeTestCase'][0]
        self.assertFalse(line.ok)
        self.assertEqual(line.description, 'a description')

    def test_adds_skip(self):
        tracker = Tracker()
        tracker.add_skip('FakeTestCase', 'a description', 'a reason')
        line = tracker._test_cases['FakeTestCase'][0]
        self.assertTrue(line.ok)
        self.assertEqual(line.description, 'a description')
        self.assertEqual(line.directive.text, 'SKIP a reason')

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

    def test_results_not_combined_by_default(self):
        tracker = Tracker()
        self.assertFalse(tracker.combined)

    def test_individual_report_has_no_plan_when_combined(self):
        outdir = tempfile.mkdtemp()
        tracker = Tracker(outdir=outdir, combined=True)
        tracker.add_ok('FakeTestCase', 'Look ma, no plan!')
        out_file = StringIO()

        tracker.generate_tap_report(
            'FakeTestCase', tracker._test_cases['FakeTestCase'], out_file)

        report = out_file.getvalue()
        self.assertTrue('Look ma' in report)
        self.assertFalse('1..' in report)

    def test_combined_results_in_one_file(self):
        outdir = tempfile.mkdtemp()
        tracker = Tracker(outdir=outdir, combined=True)
        tracker.add_ok('FakeTestCase', 'YESSS!')
        tracker.add_ok('DifferentFakeTestCase', 'GOAAL!')

        tracker.generate_tap_reports()

        self.assertFalse(
            os.path.exists(os.path.join(outdir, 'FakeTestCase.tap')))
        self.assertFalse(
            os.path.exists(os.path.join(outdir, 'DifferentFakeTestCase.tap')))
        with open(os.path.join(outdir, 'testresults.tap'), 'r') as f:
            report = f.read()
        expected = inspect.cleandoc(
            """# TAP results for FakeTestCase
            ok 1 - YESSS!
            # TAP results for DifferentFakeTestCase
            ok 2 - GOAAL!
            1..2
            """)
        self.assertEqual(report.strip(), expected)
