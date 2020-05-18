# -*- coding: utf-8 -*-
"""
    :codeauthor: Pedro Algarvio (pedro@algarvio.me)


    tests.integration.shell.cp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import absolute_import

import logging
import os

import pytest
import salt.utils.files
<<<<<<< HEAD
=======
import salt.utils.platform
import salt.utils.yaml
from salt.ext import six
from tests.support.case import ShellCase
from tests.support.helpers import slowTest
from tests.support.mixins import ShellCaseCommonTestsMixin
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
from tests.support.runtests import RUNTIME_VARS

log = logging.getLogger(__name__)


<<<<<<< HEAD
@pytest.fixture
def source_testfile():
    yield os.path.abspath(os.path.join(RUNTIME_VARS.BASE_FILES, "testfile"))
=======
@pytest.mark.windows_whitelisted
class CopyTest(ShellCase, ShellCaseCommonTestsMixin):

    _call_binary_ = "salt-cp"

    @slowTest
    def test_cp_testfile(self):
        """
        test salt-cp
        """
        minions = []
        for line in self.run_salt('--out yaml "*" test.ping'):
            if not line:
                continue
            data = salt.utils.yaml.safe_load(line)
            minions.extend(data.keys())

        self.assertNotEqual(minions, [])

        testfile = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "files",
                "file",
                "base",
                "testfile",
            )
        )
        with salt.utils.files.fopen(testfile, "r") as fh_:
            testfile_contents = fh_.read()
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@pytest.fixture
def dest_testfile():
    _copy_testfile_path = os.path.join(RUNTIME_VARS.TMP, "test_cp_testfile_copy")
    yield _copy_testfile_path
    if os.path.exists(_copy_testfile_path):
        os.unlink(_copy_testfile_path)


@pytest.mark.windows_whitelisted
@pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
def test_cp_testfile(salt_minion, salt_cp_cli, source_testfile, dest_testfile):
    """
    test salt-cp
    """
    ret = salt_cp_cli.run(
        source_testfile, dest_testfile, minion_tgt=salt_minion.config["id"]
    )
    assert ret.exitcode == 0
    assert ret.json[dest_testfile] is True
    assert os.path.exists(dest_testfile)
    with salt.utils.files.fopen(source_testfile) as rfh:
        source_testfile_contents = rfh.read()
    with salt.utils.files.fopen(dest_testfile) as rfh:
        dest_test_file = rfh.read()
    assert source_testfile_contents == dest_test_file
