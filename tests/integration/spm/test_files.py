# -*- coding: utf-8 -*-
"""
Tests for the spm files utility
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
class SPMFilesTest(SPMCase):
    """
    Validate the spm files command
    """

    def setUp(self):
        self.config = self._spm_config()
        self._spm_build_files(self.config)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_spm_files(self):
        """
        test spm files
        """
        self._spm_create_update_repo(self.config)
        install = self.run_spm("install", self.config, "apache")
        get_files = self.run_spm("files", self.config, "apache")

        os.path.exists(
            os.path.join(self.config["formula_path"], "apache", "apache.sls")
        )

    def tearDown(self):
        shutil.rmtree(self._tmp_spm)
