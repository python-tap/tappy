import unittest

from tap.tests.factory import Factory


class TestCase(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.factory = Factory()
