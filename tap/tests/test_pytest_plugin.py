# Copyright (c) 2016, Matt Layman

try:
    from unittest import mock
except ImportError:
    import mock
import tempfile

from tap.plugins import _pytest
from tap.tests import TestCase
from tap.tracker import Tracker


class TestPytestPlugin(TestCase):

    def setUp(self):
        """The pytest plugin uses module scope so a fresh tracker
        must be installed each time."""
        # When running this suite with pytest, save and restore the tracker.
        self._tracker = _pytest.tracker
        _pytest.tracker = Tracker()

    def tearDown(self):
        _pytest.tracker = self._tracker

    def _make_config(self):
        config = mock.Mock()
        config.option.tap_stream = False
        config.option.tap_files = False
        config.option.tap_outdir = None
        config.option.tap_combined = False
        return config

    def test_includes_options(self):
        group = mock.Mock()
        parser = mock.Mock()
        parser.getgroup.return_value = group
        _pytest.pytest_addoption(parser)
        self.assertEqual(group.addoption.call_count, 4)

    def test_tracker_stream_set(self):
        config = self._make_config()
        config.option.tap_stream = True
        _pytest.pytest_configure(config)
        self.assertTrue(_pytest.tracker.streaming)

    def test_tracker_outdir_set(self):
        outdir = tempfile.mkdtemp()
        config = self._make_config()
        config.option.tap_outdir = outdir
        _pytest.pytest_configure(config)
        self.assertEqual(_pytest.tracker.outdir, outdir)

    def test_tracker_combined_set(self):
        config = self._make_config()
        config.option.tap_combined = True
        _pytest.pytest_configure(config)
        self.assertTrue(_pytest.tracker.combined)

    def test_track_when_call_report(self):
        """Only the call reports are tracked."""
        _pytest.tracker = mock.Mock()
        report = mock.Mock(when='setup', outcome='passed')
        _pytest.pytest_runtest_logreport(report)
        self.assertFalse(_pytest.tracker.add_ok.called)

    def test_tracks_ok(self):
        _pytest.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        report = mock.Mock(when='call', outcome='passed', location=location)
        _pytest.pytest_runtest_logreport(report)
        _pytest.tracker.add_ok.assert_called_once_with(
            'TestFake', 'TestFake.test_me')

    def test_tracks_not_ok(self):
        _pytest.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        report = mock.Mock(when='call', outcome='failed', location=location)
        _pytest.pytest_runtest_logreport(report)
        _pytest.tracker.add_not_ok.assert_called_once_with(
            'TestFake', 'TestFake.test_me', diagnostics='')

    def test_tracks_skip(self):
        _pytest.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        longrepr = ('', '', 'Skipped: a reason')
        report = mock.Mock(
            when='call', outcome='skipped', location=location,
            longrepr=longrepr)
        _pytest.pytest_runtest_logreport(report)
        _pytest.tracker.add_skip.assert_called_once_with(
            'TestFake', 'TestFake.test_me', 'a reason')

    def test_generates_reports_for_stream(self):
        config = self._make_config()
        config.option.tap_stream = True
        _pytest.tracker = mock.Mock()
        _pytest.pytest_unconfigure(config)
        _pytest.tracker.generate_tap_reports.assert_called_once_with()

    def test_generates_reports_for_files(self):
        config = self._make_config()
        config.option.tap_files = True
        _pytest.tracker = mock.Mock()
        _pytest.pytest_unconfigure(config)
        _pytest.tracker.generate_tap_reports.assert_called_once_with()

    def test_generates_reports_for_combined(self):
        config = self._make_config()
        config.option.tap_combined = True
        _pytest.tracker = mock.Mock()
        _pytest.pytest_unconfigure(config)
        _pytest.tracker.generate_tap_reports.assert_called_once_with()

    def test_skips_reporting_with_no_output_option(self):
        config = self._make_config()
        _pytest.tracker = mock.Mock()
        _pytest.pytest_unconfigure(config)
        self.assertFalse(_pytest.tracker.generate_tap_reports.called)
