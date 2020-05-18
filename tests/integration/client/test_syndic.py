# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import pytest
from tests.support.case import SyndicCase
<<<<<<< HEAD
=======
from tests.support.helpers import slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@pytest.mark.windows_whitelisted
class TestSyndic(SyndicCase):
    """
    Validate the syndic interface by testing the test module
    """

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_ping(self):
        """
        test.ping
        """
        self.assertTrue(self.run_function("test.ping"))

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_fib(self):
        """
        test.fib
        """
        self.assertEqual(self.run_function("test.fib", ["20"],)[0], 6765)
