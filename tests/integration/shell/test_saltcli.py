# -*- coding: utf-8 -*-
"""
    :codeauthor: Thayne Harbaugh (tharbaug@adobe.com)

    tests.integration.shell.saltcli
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :NOTE: this was named ``saltcli`` rather than ``salt`` because ``salt`` conflates
           in the python importer with the expected ``salt`` namespace and breaks imports.
"""

from __future__ import absolute_import

import logging
import os
import shutil

import pytest
import salt.defaults.exitcodes
import salt.utils.path
<<<<<<< HEAD
=======
from tests.integration.utils import testprogram
from tests.support.case import ShellCase
from tests.support.helpers import slowTest
from tests.support.runtests import RUNTIME_VARS
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc

log = logging.getLogger(__name__)


@pytest.mark.windows_whitelisted
<<<<<<< HEAD
class TestRetcode(object):
=======
class SaltTest(testprogram.TestProgramCase):
    """
    Various integration tests for the salt executable.
    """

    # pylint: disable=invalid-name
    @slowTest
    def test_exit_status_unknown_argument(self):
        """
        Ensure correct exit status when an unknown argument is passed to salt-run.
        """

        runner = testprogram.TestProgramSalt(
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
        """
        Ensure correct exit status when salt-run starts correctly.
        """

        runner = testprogram.TestProgramSalt(
            name="run-correct_usage", parent_dir=self._test_dir,
        )
        # Call setup here to ensure config and script exist
        runner.setup()
        stdout, stderr, status = runner.run(
            args=["*", "-h"], catch_stderr=True, with_retcode=True,
        )
        self.assert_exit_status(
            status, "EX_OK", message="correct usage", stdout=stdout, stderr=stderr
        )


@pytest.mark.windows_whitelisted
class RetcodeTestCase(ShellCase):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    """
    Tests to ensure that we set non-zero retcodes when execution fails
    """

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_zero_exit_code_salt(self, salt_cli):
        """
        Test that a zero exit code is set when there are no errors and there is
        no explicit False result set in the return data.
        """
        ret = salt_cli.run("test.ping", minion_tgt="minion")
        assert ret.exitcode == 0, ret

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_zero_exit_code_salt_call(self, salt_call_cli):
=======
        retcode = _run("test.raise_exception salt.exceptions.SaltInvocationError")
        assert retcode == self.error_status, retcode

        retcode = _run(
            "test.raise_exception " 'OSError 2 "No such file or directory" /tmp/foo.txt'
        )
        assert retcode == self.error_status, retcode

        retcode = _run('test.echo "{foo: bar, result: False}"')
        assert retcode == self.error_status, retcode

        retcode = _run('test.echo "{foo: bar, success: False}"')
        assert retcode == self.error_status, retcode

    @slowTest
    def test_zero_exit_code(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Test that a zero exit code is set when there are no errors and there is
        no explicit False result set in the return data.
        """
        ret = salt_call_cli.run("test.ping")
        assert ret.exitcode == 0, ret

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_context_retcode_salt(self, salt_cli):
=======
    @slowTest
    def test_context_retcode(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Test that a nonzero retcode set in the context dunder will cause the
        salt CLI to set a nonzero retcode.
        """
        # test.retcode will set the retcode in the context dunder
        ret = salt_cli.run("test.retcode", "0", minion_tgt="minion")
        assert ret.exitcode == 0, ret
        ret = salt_cli.run("test.retcode", "42", minion_tgt="minion")
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_context_retcode_salt_call(self, salt_call_cli):
        """
        Test that a nonzero retcode set in the context dunder will cause the
        salt CLI to set a nonzero retcode.
        """
        # Test salt-call, making sure to also confirm the behavior of
        # retcode_passthrough.
        ret = salt_call_cli.run("test.retcode", "0")
        assert ret.exitcode == 0, ret
        ret = salt_call_cli.run("test.retcode", "42")
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret
        ret = salt_call_cli.run("--retcode-passthrough", "test.retcode", "42")
        assert ret.exitcode == 42, ret

        # Test a state run that exits with one or more failures
        ret = salt_call_cli.run("state.single", "test.fail_without_changes", "foo")
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret
        ret = salt_call_cli.run(
            "--retcode-passthrough", "state.single", "test.fail_without_changes", "foo"
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_STATE_FAILURE, ret

        # Test a state compiler error
        ret = salt_call_cli.run("state.apply", "thisslsfiledoesnotexist")
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret
        ret = salt_call_cli.run(
            "--retcode-passthrough", "state.apply", "thisslsfiledoesnotexist"
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_STATE_COMPILER_ERROR, ret

    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_salt_error(self, salt_cli):
        """
        Test that we return the expected retcode when a minion function raises
        an exception.
        """
        ret = salt_cli.run("test.raise_exception", "TypeError", minion_tgt="minion")
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_cli.run(
            "test.raise_exception",
            "salt.exceptions.CommandNotFoundError",
            minion_tgt="minion",
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_cli.run(
            "test.raise_exception",
            "salt.exceptions.CommandExecutionError",
            minion_tgt="minion",
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_cli.run(
            "test.raise_exception",
            "salt.exceptions.SaltInvocationError",
            minion_tgt="minion",
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_cli.run(
            "test.raise_exception",
            "OSError",
            "2",
            '"No such file or directory" /tmp/foo.txt',
            minion_tgt="minion",
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_cli.run(
            "test.echo", "{foo: bar, result: False}", minion_tgt="minion"
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_cli.run(
            "test.echo", "{foo: bar, success: False}", minion_tgt="minion"
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_salt_call_error(self, salt_call_cli):
=======
    @slowTest
    def test_salt_error(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Test that we return the expected retcode when a minion function raises
        an exception.
        """
        ret = salt_call_cli.run("test.raise_exception", "TypeError")
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_call_cli.run(
            "test.raise_exception", "salt.exceptions.CommandNotFoundError"
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_call_cli.run(
            "test.raise_exception", "salt.exceptions.CommandExecutionError"
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_call_cli.run(
            "test.raise_exception", "salt.exceptions.SaltInvocationError"
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_call_cli.run(
            "test.raise_exception",
            "OSError",
            "2",
            "No such file or directory",
            "/tmp/foo.txt",
        )
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

        ret = salt_call_cli.run("test.echo", "{foo: bar, result: False}")
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

<<<<<<< HEAD
        ret = salt_call_cli.run("test.echo", "{foo: bar, success: False}")
        assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_missing_minion(self, salt_cli, salt_master):
=======
    @slowTest
    def test_missing_minion(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Test that a minion which doesn't respond results in a nonzeo exit code
        """
        good = salt.utils.path.join(salt_master.config["pki_dir"], "minions", "minion")
        bad = salt.utils.path.join(salt_master.config["pki_dir"], "minions", "minion2")
        try:
            # Copy the key
            shutil.copyfile(good, bad)
            ret = salt_cli.run(
                "--timeout=5", "test.ping", minion_tgt="minion2", _timeout=120
            )
            assert ret.exitcode == salt.defaults.exitcodes.EX_GENERIC, ret
        finally:
            # Now get rid of it
            try:
                os.remove(bad)
            except OSError as exc:
                if exc.errno != os.errno.ENOENT:
                    log.error(
                        "Failed to remove %s, this may affect other tests: %s", bad, exc
                    )

    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_exit_status_unknown_argument(self, salt_cli):
        """
        Ensure correct exit status when an unknown argument is passed to salt CLI.
        """
        ret = salt_cli.run("--unknown-argument")
        assert ret.exitcode == salt.defaults.exitcodes.EX_USAGE, ret
        assert "Usage" in ret.stderr
        assert "no such option: --unknown-argument" in ret.stderr

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_exit_status_correct_usage(self, salt_cli):
        """
        Ensure correct exit status when salt CLI starts correctly.

        """
        ret = salt_cli.run("test.ping", minion_tgt="minion")
        assert ret.exitcode == salt.defaults.exitcodes.EX_OK, ret
