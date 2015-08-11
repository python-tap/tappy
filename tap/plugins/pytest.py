# Copyright (c) 2015, Matt Layman

def pytest_addoption(parser):
    """Include all the command line options."""


def pytest_configure(config):
    """Set all the options before the test run."""


def pytest_itemcollected(item):
    """Track the test result."""


def pytest_collectreport(report):
    """Dump the results."""
