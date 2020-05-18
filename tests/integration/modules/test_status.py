# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import random

import pytest
import salt.utils.platform
from salt.ext import six
from tests.support.case import ModuleCase
<<<<<<< HEAD
=======
from tests.support.helpers import flaky, slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
from tests.support.unit import skipIf


@pytest.mark.windows_whitelisted
class StatusModuleTest(ModuleCase):
    """
    Test the status module
    """

    @skipIf(salt.utils.platform.is_windows(), "minion is windows")
    @pytest.mark.flaky(max_runs=4)
    @pytest.mark.slow_test(seconds=1)  # Test takes >0.5 and <=1 seconds
    def test_status_pid(self):
        """
        status.pid
        """
        status_pid = self.run_function("status.pid", ["salt"])
        grab_pids = status_pid.split()[:10]
        random_pid = random.choice(grab_pids)
        grep_salt = self.run_function("cmd.run", ["pgrep -f salt"])
        self.assertIn(random_pid, grep_salt)

    @skipIf(not salt.utils.platform.is_windows(), "windows only test")
<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_status_cpuload(self):
        """
        status.cpuload
        """
        ret = self.run_function("status.cpuload")
        self.assertTrue(isinstance(ret, float))

    @skipIf(not salt.utils.platform.is_windows(), "windows only test")
<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_status_saltmem(self):
        """
        status.saltmem
        """
        ret = self.run_function("status.saltmem")
        self.assertTrue(isinstance(ret, int))

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_status_diskusage(self):
        """
        status.diskusage
        """
        ret = self.run_function("status.diskusage")
        if salt.utils.platform.is_darwin():
            self.assertIn("not yet supported on this platform", ret)
        elif salt.utils.platform.is_windows():
            self.assertTrue(isinstance(ret["percent"], float))
        else:
            self.assertIn("total", str(ret))
            self.assertIn("available", str(ret))

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_status_procs(self):
        """
        status.procs
        """
        ret = self.run_function("status.procs")
        for x, y in six.iteritems(ret):
            self.assertIn("cmd", y)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_status_uptime(self):
        """
        status.uptime
        """
        ret = self.run_function("status.uptime")

        if salt.utils.platform.is_windows():
            self.assertTrue(isinstance(ret, float))
        else:
            self.assertTrue(isinstance(ret["days"], int))
