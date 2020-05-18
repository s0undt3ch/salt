# -*- coding: utf-8 -*-
"""
    tests.integration.shell.master_tops
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest
<<<<<<< HEAD


@pytest.mark.windows_whitelisted
@pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
def test_custom_tops_gets_utilized(salt_call_cli):
    ret = salt_call_cli.run("state.show_top")
    assert ret.exitcode == 0
    assert "master_tops_test" in ret.stdout
    assert ret.json == {"base": ["core", "master_tops_test"]}
=======
from tests.support.case import ShellCase
from tests.support.helpers import slowTest


@pytest.mark.windows_whitelisted
class MasterTopsTest(ShellCase):

    _call_binary_ = "salt"

    @slowTest
    def test_custom_tops_gets_utilized(self):
        resp = self.run_call("state.show_top")
        self.assertTrue(any("master_tops_test" in _x for _x in resp))
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
