# Copyright (c) 2015, Matt Layman

import os

from tap.main import main
from tap.tests import TestCase


class TestMain(TestCase):
    """Tests for tap.main.main"""

    def test_exits_with_error(self):
        """The main function returns an error status if there were failures."""
        argv = ['/bin/fake', 'fake.tap']
        stream = open(os.devnull, 'w')

        status = main(argv, stream=stream)

        self.assertEqual(1, status)
