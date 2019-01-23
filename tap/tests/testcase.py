# Copyright (c) 2019, Matt Layman and contributors

import unittest

from tap.tests.factory import Factory


class TestCase(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super(TestCase, self).__init__(methodName)
        self.factory = Factory()
