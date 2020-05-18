# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import shutil

import salt.utils.platform
from tests.support.case import SSHCase
from tests.support.helpers import slowTest
from tests.support.unit import skipIf


@skipIf(salt.utils.platform.is_windows(), "salt-ssh not available on Windows")
class SSHMineTest(SSHCase):
    """
    testing salt-ssh with mine
    """

<<<<<<< HEAD
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_ssh_mine_get(self):
        """
        test salt-ssh with mine
        """
        ret = self.run_function("mine.get", ["localhost test.arg"], wipe=False)
        self.assertEqual(ret["localhost"]["args"], ["itworked"])

    def tearDown(self):
        """
        make sure to clean up any old ssh directories
        """
        salt_dir = self.run_function("config.get", ["thin_dir"], wipe=False)
        if os.path.exists(salt_dir):
            shutil.rmtree(salt_dir)
