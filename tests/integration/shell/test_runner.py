# -*- coding: utf-8 -*-
"""
Tests for the salt-run command
"""

from __future__ import absolute_import

import re

import pytest
import salt.utils.files
import salt.utils.platform
import salt.utils.yaml
<<<<<<< HEAD
from saltfactories.exceptions import ProcessTimeout
from tests.support.helpers import PYTEST_MIGRATION_XFAIL_REASON
=======
from tests.integration.utils import testprogram
from tests.support.case import ShellCase
from tests.support.helpers import skip_if_not_root, slowTest
from tests.support.mixins import ShellCaseCommonTestsMixin
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc

USERA = "saltdev-runner"
USERA_PWD = "saltdev"
HASHED_USERA_PWD = "$6$SALTsalt$ZZFD90fKFWq8AGmmX0L3uBtS9fXL62SrTk5zcnQ6EkD6zoiM3kB88G1Zvs0xm/gZ7WXJRs5nsTBybUvGSqZkT."


@pytest.fixture(scope="module")
def saltdev_account(sminion):
    try:
        assert sminion.functions.user.add(USERA, createhome=False)
        assert sminion.functions.shadow.set_password(
            USERA, USERA_PWD if salt.utils.platform.is_darwin() else HASHED_USERA_PWD
        )
        assert USERA in sminion.functions.user.list_users()
        # Run tests
        yield
    finally:
        sminion.functions.user.delete(USERA, remove=True)


@pytest.fixture
def salt_run_cli(salt_factories, salt_minion, salt_master):
    """
    Override salt_run_cli fixture to provide an increased default_timeout to the calls
    """
    return salt_factories.get_salt_run_cli(
        salt_master.config["id"], default_timeout=120
    )


@pytest.mark.windows_whitelisted
class TestSaltRun(object):
    """
    Test the salt-run command
    """

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_in_docs(self, salt_run_cli):
=======
    @slowTest
    def test_in_docs(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        test the salt-run docs system
        """
        ret = salt_run_cli.run("-d")
        assert "jobs.active:" in ret.stdout
        assert "jobs.list_jobs:" in ret.stdout
        assert "jobs.lookup_jid:" in ret.stdout
        assert "manage.down:" in ret.stdout
        assert "manage.up:" in ret.stdout
        assert "network.wol:" in ret.stdout
        assert "network.wollist:" in ret.stdout

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_not_in_docs(self, salt_run_cli):
=======
    @slowTest
    def test_notin_docs(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        test the salt-run docs system
        """
        ret = salt_run_cli.run("-d")
        assert "jobs.SaltException:" not in ret.stdout

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_salt_documentation_too_many_arguments(self, salt_run_cli):
=======
    @slowTest
    def test_salt_documentation_too_many_arguments(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Test to see if passing additional arguments shows an error
        """
        ret = salt_run_cli.run("-d", "virt.list", "foo")
        assert ret.exitcode != 0
        assert "You can only get documentation for one method at one time" in ret.stderr

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_exit_status_unknown_argument(self, salt_run_cli):
=======
    @slowTest
    def test_exit_status_unknown_argument(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Ensure correct exit status when an unknown argument is passed to salt-run.
        """
        ret = salt_run_cli.run("--unknown-argument")
        assert ret.exitcode == salt.defaults.exitcodes.EX_USAGE, ret
        assert "Usage" in ret.stderr
        assert "no such option: --unknown-argument" in ret.stderr

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_exit_status_correct_usage(self, salt_run_cli):
=======
        runner = testprogram.TestProgramSaltRun(
            name="run-unknown_argument", parent_dir=self._test_dir,
        )
        # Call setup here to ensure config and script exist
        runner.setup()
        stdout, stderr, status = runner.run(
            args=["--unknown-argument"], catch_stderr=True, with_retcode=True,
        )
        self.assert_exit_status(
            status, "EX_USAGE", message="unknown argument", stdout=stdout, stderr=stderr
        )
        # runner.shutdown() should be unnecessary since the start-up should fail

    @slowTest
    def test_exit_status_correct_usage(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Ensure correct exit status when salt-run starts correctly.
        """
        ret = salt_run_cli.run()
        assert ret.exitcode == salt.defaults.exitcodes.EX_OK, ret

<<<<<<< HEAD
    @pytest.mark.skip_if_not_root
    @pytest.mark.parametrize("flag", ["--auth", "--eauth", "--external-auth", "-a"])
    @pytest.mark.skip_on_windows(reason="PAM is not supported on Windows")
    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_salt_run_with_eauth_all_args(
        self, salt_run_cli, saltdev_account, flag, grains
    ):
=======
        runner = testprogram.TestProgramSaltRun(
            name="run-correct_usage", parent_dir=self._test_dir,
        )
        # Call setup here to ensure config and script exist
        runner.setup()
        stdout, stderr, status = runner.run(catch_stderr=True, with_retcode=True,)
        self.assert_exit_status(
            status, "EX_OK", message="correct usage", stdout=stdout, stderr=stderr
        )

    @skip_if_not_root
    @slowTest
    def test_salt_run_with_eauth_all_args(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        test salt-run with eauth
        tests all eauth args
        """
        try:
            ret = salt_run_cli.run(
                flag,
                "pam",
                "--username",
                USERA,
                "--password",
                USERA_PWD,
                "test.arg",
                "arg",
                kwarg="kwarg1",
            )
<<<<<<< HEAD
        except ProcessTimeout as exc:
            if grains["os_family"] != "Debian":
                # This test only seems to be flaky on Debian and Ubuntu
                raise exc from None
            pytest.xfail(PYTEST_MIGRATION_XFAIL_REASON)
        assert ret.exitcode == 0, ret
        assert ret.json, ret
        expected = {"args": ["arg"], "kwargs": {"kwarg": "kwarg1"}}
        assert ret.json == expected, ret

    @pytest.mark.skip_if_not_root
    @pytest.mark.skip_on_windows(reason="PAM is not supported on Windows")
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
    def test_salt_run_with_eauth_bad_passwd(self, salt_run_cli, saltdev_account):
=======
            expect = [
                "args:",
                "    - arg",
                "kwargs:",
                "    ----------",
                "    kwarg:",
                "        kwarg1",
            ]
            self.assertEqual(expect, run_cmd)
        self._remove_user()

    @skip_if_not_root
    @slowTest
    def test_salt_run_with_eauth_bad_passwd(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        test salt-run with eauth and bad password
        """
        ret = salt_run_cli.run(
            "-a",
            "pam",
            "--username",
            USERA,
            "--password",
            "wrongpassword",
            "test.arg",
            "arg",
            kwarg="kwarg1",
        )
        assert (
            ret.stdout
            == 'Authentication failure of type "eauth" occurred for user {}.'.format(
                USERA
            )
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_salt_run_with_wrong_eauth(self, salt_run_cli):
=======
    @slowTest
    def test_salt_run_with_wrong_eauth(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        test salt-run with wrong eauth parameter
        """
        ret = salt_run_cli.run(
            "-a",
            "wrongeauth",
            "--username",
            USERA,
            "--password",
            USERA_PWD,
            "test.arg",
            "arg",
            kwarg="kwarg1",
        )
        assert ret.exitcode == 0, ret
        assert re.search(
            r"^The specified external authentication system \"wrongeauth\" is not available\nAvailable eauth types: auto, .*",
            ret.stdout.replace("\r\n", "\n"),
        )
