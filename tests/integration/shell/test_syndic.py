# -*- coding: utf-8 -*-
"""
    :codeauthor: Pedro Algarvio (pedro@algarvio.me)


    tests.integration.shell.syndic
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import absolute_import

import logging
<<<<<<< HEAD
import time
=======
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc

import pytest
<<<<<<< HEAD
import salt.defaults.exitcodes
from saltfactories.exceptions import ProcessNotStarted
from tests.support.helpers import PRE_PYTEST_SKIP_REASON
=======
import salt.utils.files
import salt.utils.platform
import salt.utils.yaml
from tests.integration.utils import testprogram
from tests.support.case import ShellCase
from tests.support.helpers import slowTest
from tests.support.mixins import ShellCaseCommonTestsMixin
from tests.support.unit import skipIf
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc

try:
    from salt.utils.odict import OrderedDict
except ImportError:
    from collections import OrderedDict

log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def shell_tests_salt_master(request, salt_factories):
    return salt_factories.spawn_master(request, "syndic-shell-tests-mom")


@pytest.mark.windows_whitelisted
<<<<<<< HEAD
class TestSaltSyndicCLI(object):
    @pytest.mark.skip_on_windows(reason=PRE_PYTEST_SKIP_REASON)
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_exit_status_unknown_user(
        self, request, salt_factories, shell_tests_salt_master
    ):
=======
class SyndicTest(ShellCase, testprogram.TestProgramCase, ShellCaseCommonTestsMixin):
    """
    Test the salt-syndic command
    """

    _call_binary_ = "salt-syndic"

    @skipIf(salt.utils.platform.is_windows(), "Skip on Windows OS")
    @slowTest
    def test_exit_status_unknown_user(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Ensure correct exit status when the syndic is configured to run as an unknown user.
        """
        with pytest.raises(ProcessNotStarted) as exc:
            salt_factories.spawn_syndic(
                request,
                "syndic-shell-tests-unknown-user",
                master_of_masters_id=shell_tests_salt_master.config["id"],
                max_start_attempts=1,
                config_overrides={"syndic": {"user": "unknown-user"}},
            )

<<<<<<< HEAD
        assert exc.value.exitcode == salt.defaults.exitcodes.EX_NOUSER, exc.value
        assert "The user is not available." in exc.value.stderr, exc.value

    @pytest.mark.skip_on_windows(reason=PRE_PYTEST_SKIP_REASON)
    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_exit_status_unknown_argument(
        self, request, salt_factories, shell_tests_salt_master, tempdir
    ):
=======
    # pylint: disable=invalid-name
    @skipIf(salt.utils.platform.is_windows(), "Skip on Windows OS")
    @slowTest
    def test_exit_status_unknown_argument(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Ensure correct exit status when an unknown argument is passed to salt-syndic.
        """
        # We pass root_dir in order not to hit the max length socket path issue
        root_dir = tempdir.join("ex-st-unkn-arg-syndic").ensure(dir=True)
        with pytest.raises(ProcessNotStarted) as exc:
            salt_factories.spawn_syndic(
                request,
                "syndic-shell-tests-unknown-arguments",
                master_of_masters_id=shell_tests_salt_master.config["id"],
                max_start_attempts=1,
                base_script_args=["--unknown-argument"],
                config_defaults={"syndic": {"root_dir": root_dir}},
            )
<<<<<<< HEAD
        assert exc.value.exitcode == salt.defaults.exitcodes.EX_USAGE, exc.value
        assert "Usage" in exc.value.stderr, exc.value
        assert "no such option: --unknown-argument" in exc.value.stderr, exc.value

    @pytest.mark.skip_on_windows(reason=PRE_PYTEST_SKIP_REASON)
    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_exit_status_correct_usage(
        self, request, salt_factories, shell_tests_salt_master
    ):
        proc = salt_factories.spawn_syndic(
            request,
            "syndic-shell-tests",
            master_of_masters_id=shell_tests_salt_master.config["id"],
=======
        finally:
            # Although the start-up should fail, call shutdown() to set the
            # internal _shutdown flag and avoid the registered atexit calls to
            # cause timeout exceptions and respective traceback
            syndic.shutdown()

    @skipIf(salt.utils.platform.is_windows(), "Skip on Windows OS")
    @slowTest
    def test_exit_status_correct_usage(self):
        """
        Ensure correct exit status when salt-syndic starts correctly.

        Skipped on windows because daemonization not supported
        """

        syndic = testprogram.TestDaemonSaltSyndic(
            name="correct_usage", parent_dir=self._test_dir,
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        )
        assert proc.is_alive()
        time.sleep(1)
        ret = proc.terminate()
        assert ret.exitcode == salt.defaults.exitcodes.EX_OK, ret
