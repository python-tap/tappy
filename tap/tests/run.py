# Copyright (c) 2015, Matt Layman

import os
import unittest

from tap import TAPTestRunner

if __name__ == '__main__':
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    tests = loader.discover(tests_dir)
    runner = TAPTestRunner()
    runner.set_outdir('testout')
    runner.set_format('Hi: {method_name} - {short_description}')
    runner.run(tests)
