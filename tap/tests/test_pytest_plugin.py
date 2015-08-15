# Copyright (c) 2015, Matt Layman

try:
    from unittest import mock
except ImportError:
    import mock
import tempfile

from tap.plugins import pytest
from tap.tests import TestCase
from tap.tracker import Tracker


class TestPytestPlugin(TestCase):

    def setUp(self):
        """The pytest plugin uses module scope so a fresh tracker
        must be installed each time."""
        # When running this suite with pytest, save and restore the tracker.
        self._tracker = pytest.tracker
        pytest.tracker = Tracker()

    def tearDown(self):
        pytest.tracker = self._tracker

    def _make_config(self):
        config = mock.Mock()
        config.option.tap_outdir = None
        config.option.tap_combined = False
        return config

    def test_includes_options(self):
        group = mock.Mock()
        parser = mock.Mock()
        parser.getgroup.return_value = group
        pytest.pytest_addoption(parser)
        self.assertEqual(group.addoption.call_count, 2)

    def test_tracker_outdir_set(self):
        outdir = tempfile.mkdtemp()
        config = self._make_config()
        config.option.tap_outdir = outdir
        pytest.pytest_configure(config)
        self.assertEqual(pytest.tracker.outdir, outdir)

    def test_tracker_combined_set(self):
        config = self._make_config()
        config.option.tap_combined = True
        pytest.pytest_configure(config)
        self.assertTrue(pytest.tracker.combined)

    def test_track_when_call_report(self):
        """Only the call reports are tracked."""
        pytest.tracker = mock.Mock()
        report = mock.Mock(when='setup', outcome='passed')
        pytest.pytest_runtest_logreport(report)
        self.assertFalse(pytest.tracker.add_ok.called)

    def test_tracks_ok(self):
        pytest.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        report = mock.Mock(when='call', outcome='passed', location=location)
        pytest.pytest_runtest_logreport(report)
        pytest.tracker.add_ok.assert_called_once_with(
            'TestFake', 'TestFake.test_me')

    def test_tracks_not_ok(self):
        pytest.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        report = mock.Mock(when='call', outcome='failed', location=location)
        pytest.pytest_runtest_logreport(report)
        pytest.tracker.add_not_ok.assert_called_once_with(
            'TestFake', 'TestFake.test_me')

    def test_tracks_skip(self):
        pytest.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        longrepr = ('', '', 'Skipped: a reason')
        report = mock.Mock(
            when='call', outcome='skipped', location=location,
            longrepr=longrepr)
        pytest.pytest_runtest_logreport(report)
        pytest.tracker.add_skip.assert_called_once_with(
            'TestFake', 'TestFake.test_me', 'a reason')

    def test_generates_reports(self):
        pytest.tracker = mock.Mock()
        pytest.pytest_unconfigure(None)
        pytest.tracker.generate_tap_reports.assert_called_once_with()
