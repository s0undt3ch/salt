# -*- coding: utf-8 -*-
"""
Validate the mac-defaults module
"""

from __future__ import absolute_import, print_function, unicode_literals

<<<<<<< HEAD
import pytest
from tests.support.case import ModuleCase
=======
from tests.support.case import ModuleCase
from tests.support.helpers import destructiveTest, runs_on, skip_if_not_root
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc

DEFAULT_DOMAIN = "com.apple.AppleMultitouchMouse"
DEFAULT_KEY = "MouseHorizontalScroll"
DEFAULT_VALUE = "0"


<<<<<<< HEAD
@pytest.mark.destructive_test
@pytest.mark.skip_if_not_root
@pytest.mark.skip_unless_on_darwin
=======
@destructiveTest
@skip_if_not_root
@runs_on(kernel="Darwin")
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
class MacDefaultsModuleTest(ModuleCase):
    """
    Integration tests for the mac_default module
    """

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=1)  # Test takes >0.5 and <=1 seconds
=======
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_macdefaults_write_read(self):
        """
        Tests that writes and reads macdefaults
        """
        write_domain = self.run_function(
            "macdefaults.write", [DEFAULT_DOMAIN, DEFAULT_KEY, DEFAULT_VALUE]
        )
        self.assertTrue(write_domain)

        read_domain = self.run_function(
            "macdefaults.read", [DEFAULT_DOMAIN, DEFAULT_KEY]
        )
        self.assertTrue(read_domain)
        self.assertEqual(read_domain, DEFAULT_VALUE)
