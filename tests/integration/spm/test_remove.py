# -*- coding: utf-8 -*-
"""
Tests for the spm remove utility
"""
from __future__ import absolute_import, print_function, unicode_literals

import os
import shutil

import pytest
from tests.support.case import SPMCase
<<<<<<< HEAD
=======
from tests.support.helpers import destructiveTest, slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@pytest.mark.destructive_test
@pytest.mark.windows_whitelisted
class SPMRemoveTest(SPMCase):
    """
    Validate the spm remove command
    """

    def setUp(self):
        self.config = self._spm_config()
        self._spm_build_files(self.config)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_spm_remove(self):
        """
        test spm remove from an inital repo install
        """
        # first install apache package
        self._spm_create_update_repo(self.config)
        install = self.run_spm("install", self.config, "apache")

        sls = os.path.join(self.config["formula_path"], "apache", "apache.sls")

        self.assertTrue(os.path.exists(sls))

        # now remove an make sure file is removed
        remove = self.run_spm("remove", self.config, "apache")
        sls = os.path.join(self.config["formula_path"], "apache", "apache.sls")

        self.assertFalse(os.path.exists(sls))

        self.assertIn("... removing apache", remove)

    def tearDown(self):
        shutil.rmtree(self._tmp_spm)
