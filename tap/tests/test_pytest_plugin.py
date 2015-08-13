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
        pytest.tracker = Tracker()

    def test_includes_options(self):
        group = mock.Mock()
        parser = mock.Mock()
        parser.getgroup.return_value = group
        pytest.pytest_addoption(parser)
        self.assertEqual(group.addoption.call_count, 1)

    def test_tracker_outdir_set(self):
        outdir = tempfile.mkdtemp()
        config = mock.Mock()
        config.option.tap_outdir = outdir
        pytest.pytest_configure(config)
        self.assertEqual(pytest.tracker.outdir, outdir)
