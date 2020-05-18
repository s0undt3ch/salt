# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest
import salt.utils.platform
from tests.support.case import ModuleCase
<<<<<<< HEAD
=======
from tests.support.helpers import destructiveTest, flaky, slowTest
from tests.support.unit import skipIf
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@pytest.mark.flaky(max_runs=4)
@pytest.mark.windows_whitelisted
@pytest.mark.skipif(
    not salt.utils.platform.is_windows(), reason="Test is Windows specific."
)
class NTPTest(ModuleCase):
    """
    Validate windows ntp module
    """

<<<<<<< HEAD
    @pytest.mark.destructive_test
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @destructiveTest
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_ntp_set_servers(self):
        """
        test ntp get and set servers
        """
        ntp_srv = "pool.ntp.org"
        set_srv = self.run_function("ntp.set_servers", [ntp_srv])
        self.assertTrue(set_srv)

        get_srv = self.run_function("ntp.get_servers")
        self.assertEqual(ntp_srv, get_srv[0])
