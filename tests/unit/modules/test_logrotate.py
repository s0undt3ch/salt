# -*- coding: utf-8 -*-
"""
    :codeauthor: Jayesh Kariya <jayeshk@saltstack.com>
"""

# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals

import pytest
import salt.modules.logrotate as logrotate

# Import Salt Libs
from salt.exceptions import SaltInvocationError

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.mock import MagicMock, patch
from tests.support.unit import TestCase

PARSE_CONF = {
    "include files": {"rsyslog": ["/var/log/syslog"]},
    "rotate": 1,
    "/var/log/wtmp": {"rotate": 1},
}


class LogrotateTestCase(TestCase, LoaderModuleMockMixin):
    """
    Test cases for salt.modules.logrotate
    """

    def setup_loader_modules(self):
        return {logrotate: {}}

    # 'show_conf' function tests: 1

    @pytest.mark.slow_test(seconds=1)  # Test takes >0.1 and <=1 seconds
    def test_show_conf(self):
        """
        Test if it show parsed configuration
        """
        with patch("salt.modules.logrotate._parse_conf", MagicMock(return_value=True)):
            self.assertTrue(logrotate.show_conf())

    # 'set_' function tests: 4

    def test_set(self):
        """
        Test if it set a new value for a specific configuration line
        """
        with patch(
            "salt.modules.logrotate._parse_conf", MagicMock(return_value=PARSE_CONF)
        ), patch.dict(
            logrotate.__salt__, {"file.replace": MagicMock(return_value=True)}
        ):
            self.assertTrue(logrotate.set_("rotate", "2"))

    def test_set_failed(self):
        """
        Test if it fails to set a new value for a specific configuration line
        """
        with patch(
            "salt.modules.logrotate._parse_conf", MagicMock(return_value=PARSE_CONF)
        ):
            kwargs = {"key": "/var/log/wtmp", "value": 2}
            self.assertRaises(SaltInvocationError, logrotate.set_, **kwargs)

    def test_set_setting(self):
        """
        Test if it set a new value for a specific configuration line
        """
        with patch.dict(
            logrotate.__salt__, {"file.replace": MagicMock(return_value=True)}
        ), patch(
            "salt.modules.logrotate._parse_conf", MagicMock(return_value=PARSE_CONF)
        ):
            self.assertTrue(logrotate.set_("/var/log/wtmp", "rotate", "2"))

    def test_set_setting_failed(self):
        """
        Test if it fails to set a new value for a specific configuration line
        """
        with patch(
            "salt.modules.logrotate._parse_conf", MagicMock(return_value=PARSE_CONF)
        ):
            kwargs = {"key": "rotate", "value": "/var/log/wtmp", "setting": "2"}
            self.assertRaises(SaltInvocationError, logrotate.set_, **kwargs)
