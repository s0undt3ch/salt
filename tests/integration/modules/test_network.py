# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest
import salt.utils.path
import salt.utils.platform
from tests.support.case import ModuleCase
from tests.support.unit import skipIf

URL = "google-public-dns-a.google.com"


@pytest.mark.windows_whitelisted
class NetworkTest(ModuleCase):
    """
    Validate network module
    """

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_network_ping(self):
        """
        network.ping
        """
        ret = self.run_function("network.ping", [URL])
        exp_out = ["ping", URL, "ms", "time"]
        for out in exp_out:
            self.assertIn(out, ret.lower())

    @skipIf(salt.utils.platform.is_darwin(), "not supported on macosx")
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_network_netstat(self):
        """
        network.netstat
        """
        ret = self.run_function("network.netstat")
        exp_out = ["proto", "local-address"]
        for val in ret:
            for out in exp_out:
                self.assertIn(out, val)

    @pytest.mark.slow_test(seconds=240)  # Test takes >120 and <=240 seconds
    def test_network_traceroute(self):
        """
        network.traceroute
        """
        if (
            not salt.utils.path.which("traceroute")
            and not salt.utils.platform.is_windows()
        ):
            self.skipTest("traceroute not installed")
        ret = self.run_function("network.traceroute", [URL])
        exp_out = ["hostname", "ip"]
        for out in exp_out:
            self.assertIn(out, exp_out)

    @skipIf(not salt.utils.platform.is_windows(), "windows only test")
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_network_nslookup(self):
        """
        network.nslookup
        """
        ret = self.run_function("network.nslookup", [URL])
        exp_out = ["Server", "Address"]
        for out in exp_out:
            self.assertIn(out, exp_out)
