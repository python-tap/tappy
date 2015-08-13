# Copyright (c) 2015, Matt Layman

try:
    from unittest import mock
except ImportError:
    import mock

from tap.plugins import pytest
from tap.tests import TestCase
from tap.tracker import Tracker


class TestPytestPlugin(TestCase):

    def setUp(self):
        """The pytest plugin uses module scope so a fresh tracker
        must be installed each time."""
        pytest.tracker = Tracker()

    def test_tracker_outdir_set(self):
        config = mock.Mock()
        config.option.tap_outdir = 'fakeout'
        pytest.pytest_configure(config)
        self.assertEqual(pytest.tracker.outdir, 'fakeout')
