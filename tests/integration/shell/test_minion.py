# -*- coding: utf-8 -*-
"""
    :codeauthor: Pedro Algarvio (pedro@algarvio.me)


    tests.integration.shell.minion
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import absolute_import

import logging
import time

import pytest
<<<<<<< HEAD
import salt.defaults.exitcodes
from saltfactories.exceptions import ProcessNotStarted
from tests.support.helpers import PRE_PYTEST_SKIP_REASON
=======
import salt.utils.files
import salt.utils.platform
import salt.utils.yaml
import tests.integration.utils
from salt.ext import six
from tests.integration.utils import testprogram
from tests.support.case import ShellCase
from tests.support.helpers import slowTest
from tests.support.mixins import ShellCaseCommonTestsMixin
from tests.support.runtests import RUNTIME_VARS
from tests.support.unit import skipIf
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc

log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def shell_tests_salt_master(request, salt_factories):
    return salt_factories.spawn_master(request, "minion-shell-tests")


@pytest.fixture(scope="module")
def shell_tests_salt_minion_config(request, salt_factories, shell_tests_salt_master):
    return salt_factories.configure_minion(
        request,
        shell_tests_salt_master.config["id"],
        master_id=shell_tests_salt_master.config["id"],
        config_overrides={"user": "unknown-user"},
    )


<<<<<<< HEAD
@pytest.mark.windows_whitelisted
class TestSaltMinionCLI(object):
    @pytest.mark.skip_on_windows(reason=PRE_PYTEST_SKIP_REASON)
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
    def test_exit_status_unknown_user(
        self, request, salt_factories, shell_tests_salt_minion_config
    ):
=======
        pform = platform.uname()[0].lower()
        if pform not in ("linux",):
            self.skipTest(
                "salt-minion init script is unavailable on {1}".format(platform)
            )

        minions, _, init_script = self._initscript_setup(self._test_minions)

        try:
            # These tests are grouped together, rather than split into individual test functions,
            # because subsequent tests leverage the state from the previous test which minimizes
            # setup for each test.

            # I take visual readability with aligned columns over strict PEP8
            # (bad-whitespace) Exactly one space required after comma
            # pylint: disable=C0326
            ret = self._run_initscript(
                init_script, minions[:1], False, "bogusaction", 2
            )
            ret = self._run_initscript(
                init_script, minions[:1], False, "reload", 3
            )  # Not implemented
            ret = self._run_initscript(
                init_script, minions[:1], False, "stop", 0, "when not running"
            )
            ret = self._run_initscript(
                init_script, minions[:1], False, "status", 3, "when not running"
            )
            ret = self._run_initscript(
                init_script, minions[:1], False, "condrestart", 7, "when not running"
            )
            ret = self._run_initscript(
                init_script, minions[:1], False, "try-restart", 7, "when not running"
            )
            ret = self._run_initscript(
                init_script, minions, True, "start", 0, "when not running"
            )

            ret = self._run_initscript(
                init_script, minions, True, "status", 0, "when running"
            )
            # Verify that PIDs match
            mpids = {}
            for line in ret[0]:
                segs = line.decode(__salt_system_encoding__).split()
                minfo = segs[0].split(":")
                mpids[minfo[-1]] = int(segs[-1]) if segs[-1].isdigit() else None
            for minion in minions:
                self.assertEqual(
                    minion.daemon_pid,
                    mpids[minion.name],
                    'PID in "{0}" is {1} and does not match status PID {2}'.format(
                        minion.abs_path(minion.pid_path),
                        minion.daemon_pid,
                        mpids[minion.name],
                    ),
                )

            ret = self._run_initscript(
                init_script, minions, True, "start", 0, "when running"
            )
            ret = self._run_initscript(
                init_script, minions, True, "condrestart", 0, "when running"
            )
            ret = self._run_initscript(
                init_script, minions, True, "try-restart", 0, "when running"
            )
            ret = self._run_initscript(
                init_script, minions, False, "stop", 0, "when running"
            )

        finally:
            # Ensure that minions are shutdown
            for minion in minions:
                minion.shutdown()

    @skipIf(salt.utils.platform.is_windows(), "Skip on Windows OS")
    @slowTest
    def test_exit_status_unknown_user(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Ensure correct exit status when the minion is configured to run as an unknown user.
        """
        with pytest.raises(ProcessNotStarted) as exc:
            salt_factories.spawn_minion(
                request,
                shell_tests_salt_minion_config["id"],
                master_id=shell_tests_salt_minion_config["id"],
                max_start_attempts=1,
            )
<<<<<<< HEAD
=======
        finally:
            # Although the start-up should fail, call shutdown() to set the
            # internal _shutdown flag and avoid the registered atexit calls to
            # cause timeout exceptions and respective traceback
            minion.shutdown()

    #    @skipIf(salt.utils.platform.is_windows(), 'Skip on Windows OS')
    @slowTest
    def test_exit_status_unknown_argument(self):
        """
        Ensure correct exit status when an unknown argument is passed to salt-minion.
        """
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc

        assert exc.value.exitcode == salt.defaults.exitcodes.EX_NOUSER, exc.value
        assert "The user is not available." in exc.value.stderr, exc.value

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_exit_status_unknown_argument(
        self, request, salt_factories, shell_tests_salt_minion_config, tempdir
    ):
=======
    @skipIf(salt.utils.platform.is_windows(), "Skip on Windows OS")
    @slowTest
    def test_exit_status_correct_usage(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Ensure correct exit status when an unknown argument is passed to salt-minion.
        """
        # We pass root_dir in order not to hit the max length socket path issue
        root_dir = tempdir.join("ex-st-unkn-arg-minion").ensure(dir=True)
        with pytest.raises(ProcessNotStarted) as exc:
            salt_factories.spawn_minion(
                request,
                shell_tests_salt_minion_config["id"],
                master_id=shell_tests_salt_minion_config["id"],
                max_start_attempts=1,
                base_script_args=["--unknown-argument"],
                config_defaults={"root_dir": root_dir},
            )
        assert exc.value.exitcode == salt.defaults.exitcodes.EX_USAGE, exc.value
        assert "Usage" in exc.value.stderr, exc.value
        assert "no such option: --unknown-argument" in exc.value.stderr, exc.value

    @pytest.mark.skip_on_windows(reason=PRE_PYTEST_SKIP_REASON)
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
    def test_exit_status_correct_usage(
        self, request, salt_factories, shell_tests_salt_master
    ):
        proc = salt_factories.spawn_minion(
            request,
            shell_tests_salt_master.config["id"] + "-2",
            master_id=shell_tests_salt_master.config["id"],
        )
        assert proc.is_alive()
        time.sleep(1)
        ret = proc.terminate()
        assert ret.exitcode == salt.defaults.exitcodes.EX_OK, ret
