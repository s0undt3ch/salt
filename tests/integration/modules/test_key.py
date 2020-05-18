# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import re

import pytest
from tests.support.case import ModuleCase
<<<<<<< HEAD
=======
from tests.support.helpers import slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@pytest.mark.windows_whitelisted
class KeyModuleTest(ModuleCase):
<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_key_finger(self):
        """
        test key.finger to ensure we receive a valid fingerprint
        """
        out = self.run_function("key.finger")
        match = re.match("([0-9a-z]{2}:){15,}[0-9a-z]{2}$", out)
        self.assertTrue(match)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_key_finger_master(self):
        """
        test key.finger_master to ensure we receive a valid fingerprint
        """
        out = self.run_function("key.finger_master")
        match = re.match("([0-9a-z]{2}:){15,}[0-9a-z]{2}$", out)
        self.assertTrue(match)
