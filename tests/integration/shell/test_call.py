# -*- coding: utf-8 -*-
"""
    :codeauthor: Pedro Algarvio (pedro@algarvio.me)


    tests.integration.shell.call
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from __future__ import absolute_import

import logging
import os
import pprint
import re
import shutil
import sys

import pytest
import salt.utils.files
import salt.utils.json
import salt.utils.platform
import salt.utils.yaml
<<<<<<< HEAD
from tests.support.helpers import PRE_PYTEST_SKIP, PRE_PYTEST_SKIP_REASON
=======
from salt.ext import six
from tests.integration.utils import testprogram
from tests.support.case import ShellCase
from tests.support.helpers import change_cwd, flaky, slowTest, with_tempfile
from tests.support.mixins import ShellCaseCommonTestsMixin
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
from tests.support.runtests import RUNTIME_VARS

log = logging.getLogger(__name__)


@pytest.mark.windows_whitelisted
<<<<<<< HEAD
class TestSaltCallCLI(object):
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_fib(self, salt_call_cli):
        ret = salt_call_cli.run("test.fib", "3")
        assert ret.exitcode == 0
        assert ret.json[0] == 2

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_fib_txt_output(self, salt_call_cli):
        ret = salt_call_cli.run("--output=txt", "test.fib", "3")
        assert ret.exitcode == 0
        assert ret.json is None
        assert (
            re.match(r"local: \(2, [0-9]{1}\.(([0-9]+)(e-([0-9]+))?)\)\s", ret.stdout)
            is not None
        )

    @pytest.mark.parametrize("indent", [-1, 0, 1])
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_json_out_indent(self, salt_call_cli, indent):
        ret = salt_call_cli.run(
            "--out=json", "--out-indent={}".format(indent), "test.ping"
        )
        assert ret.exitcode == 0
        assert ret.json is True
        if indent == -1:
            expected_output = '{"local": true}\n'
        elif indent == 0:
            expected_output = '{\n"local": true\n}\n'
        else:
            expected_output = '{\n "local": true\n}\n'
        stdout = ret.stdout
        if salt.utils.platform.is_windows():
            expected_output = expected_output.replace("\n", os.linesep)
        assert ret.stdout == expected_output

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_local_sls_call(self, salt_call_cli):
=======
class CallTest(ShellCase, testprogram.TestProgramCase, ShellCaseCommonTestsMixin):

    _call_binary_ = "salt-call"

    @slowTest
    def test_default_output(self):
        out = self.run_call("-l quiet test.fib 3")

        expect = ["local:", "    - 2"]
        self.assertEqual(expect, out[:-1])

    @slowTest
    def test_text_output(self):
        out = self.run_call("-l quiet --out txt test.fib 3")

        expect = ["local: (2"]

        self.assertEqual("".join(expect), "".join(out).rsplit(",", 1)[0])

    @slowTest
    def test_json_out_indent(self):
        out = self.run_call("test.ping -l quiet --out=json --out-indent=-1")
        self.assertIn('"local": true', "".join(out))

        out = self.run_call("test.ping -l quiet --out=json --out-indent=0")
        self.assertIn('"local": true', "".join(out))

        out = self.run_call("test.ping -l quiet --out=json --out-indent=1")
        self.assertIn('"local": true', "".join(out))

    @slowTest
    def test_local_sls_call(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        fileroot = os.path.join(RUNTIME_VARS.FILES, "file", "base")
        ret = salt_call_cli.run(
            "--local", "--file-root", fileroot, "state.sls", "saltcalllocal"
        )
<<<<<<< HEAD
        assert ret.exitcode == 0
        state_run_dict = next(iter(ret.json.values()))
        assert state_run_dict["name"] == "test.echo"
        assert state_run_dict["result"] is True
        assert state_run_dict["changes"]["ret"] == "hello"

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_local_salt_call(self, salt_call_cli):
=======
        self.assertIn("Name: test.echo", "".join(out))
        self.assertIn("Result: True", "".join(out))
        self.assertIn("hello", "".join(out))
        self.assertIn("Succeeded: 1", "".join(out))

    @with_tempfile()
    @slowTest
    def test_local_salt_call(self, name):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        This tests to make sure that salt-call does not execute the
        function twice, see https://github.com/saltstack/salt/pull/49552
        """
        with pytest.helpers.temp_file() as filename:

<<<<<<< HEAD
            ret = salt_call_cli.run(
                "--local", "state.single", "file.append", name=filename, text="foo"
            )
            assert ret.exitcode == 0

            state_run_dict = next(iter(ret.json.values()))
            assert state_run_dict["changes"]

            # 2nd sanity check: make sure that "foo" only exists once in the file
            with salt.utils.files.fopen(filename) as fp_:
                contents = fp_.read()
            assert contents.count("foo") == 1, contents

    @pytest.mark.skip_on_windows(reason=PRE_PYTEST_SKIP_REASON)
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_user_delete_kw_output(self, salt_call_cli):
        ret = salt_call_cli.run("-d", "user.delete", _timeout=120)
        assert ret.exitcode == 0
        expected_output = "salt '*' user.delete name"
        if not salt.utils.platform.is_windows():
            expected_output += " remove=True force=True"
        assert expected_output in ret.stdout

    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_salt_documentation_too_many_arguments(self, salt_call_cli):
=======
        def _run_call(cmd):
            cmd = "--out=json " + cmd
            return salt.utils.json.loads("".join(self.run_call(cmd, local=True)))[
                "local"
            ]

        ret = _run_call('state.single file.append name={0} text="foo"'.format(name))
        ret = ret[next(iter(ret))]

        # Make sure we made changes
        assert ret["changes"]

        # 2nd sanity check: make sure that "foo" only exists once in the file
        with salt.utils.files.fopen(name) as fp_:
            contents = fp_.read()
        assert contents.count("foo") == 1, contents

    @skipIf(
        salt.utils.platform.is_windows() or salt.utils.platform.is_darwin(),
        "This test requires a supported master",
    )
    @slowTest
    def test_user_delete_kw_output(self):
        ret = self.run_call("-l quiet -d user.delete")
        assert "salt '*' user.delete name remove=True force=True" in "".join(ret)

    @slowTest
    def test_salt_documentation_too_many_arguments(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Test to see if passing additional arguments shows an error
        """
        ret = salt_call_cli.run("-d", "virtualenv.create", "/tmp/ve")
        assert ret.exitcode != 0
        assert "You can only get documentation for one method at one time" in ret.stderr

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_issue_6973_state_highstate_exit_code(self, salt_call_cli):
=======
    @slowTest
    def test_issue_6973_state_highstate_exit_code(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        If there is no tops/master_tops or state file matches
        for this minion, salt-call should exit non-zero if invoked with
        option --retcode-passthrough
        """
        src = os.path.join(RUNTIME_VARS.BASE_FILES, "top.sls")
        dst = os.path.join(RUNTIME_VARS.BASE_FILES, "top.sls.bak")
        shutil.move(src, dst)
        expected_comment = "No states found for this minion"
        try:
            ret = salt_call_cli.run("--retcode-passthrough", "state.highstate")
        finally:
            shutil.move(dst, src)
<<<<<<< HEAD
        assert ret.exitcode != 0
        assert expected_comment in ret.stdout

    @PRE_PYTEST_SKIP
    def test_issue_15074_output_file_append(self, salt_call_cli):

        with pytest.helpers.temp_file(name="issue-15074") as output_file_append:
            ret = salt_call_cli.run(
                "--output-file", output_file_append, "test.versions"
=======
        self.assertIn(expected_comment, "".join(stdout))
        self.assertNotEqual(0, retcode)

    @skipIf(sys.platform.startswith("win"), "This test does not apply on Win")
    @skipIf(True, "to be re-enabled when #23623 is merged")
    def test_return(self):
        self.run_call('cmd.run "echo returnTOmaster"')
        jobs = [a for a in self.run_run("jobs.list_jobs")]

        self.assertTrue(True in ["returnTOmaster" in j for j in jobs])
        # lookback jid
        first_match = [(i, j) for i, j in enumerate(jobs) if "returnTOmaster" in j][0]
        jid, idx = None, first_match[0]
        while idx > 0:
            jid = re.match("([0-9]+):", jobs[idx])
            if jid:
                jid = jid.group(1)
                break
            idx -= 1
        assert idx > 0
        assert jid
        master_out = [a for a in self.run_run("jobs.lookup_jid {0}".format(jid))]
        self.assertTrue(True in ["returnTOmaster" in a for a in master_out])

    @skipIf(salt.utils.platform.is_windows(), "Skip on Windows")
    @slowTest
    def test_syslog_file_not_found(self):
        """
        test when log_file is set to a syslog file that does not exist
        """
        config_dir = os.path.join(RUNTIME_VARS.TMP, "log_file_incorrect")
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)

        with change_cwd(config_dir):
            with salt.utils.files.fopen(
                self.get_config_file_path("minion"), "r"
            ) as fh_:
                minion_config = salt.utils.yaml.load(fh_.read())
                minion_config["log_file"] = "file:///dev/doesnotexist"
                with salt.utils.files.fopen(
                    os.path.join(config_dir, "minion"), "w"
                ) as fh_:
                    fh_.write(
                        salt.utils.yaml.dump(minion_config, default_flow_style=False)
                    )
            ret = self.run_script(
                "salt-call",
                '--config-dir {0} cmd.run "echo foo"'.format(config_dir),
                timeout=120,
                catch_stderr=True,
                with_retcode=True,
            )
            try:
                if sys.version_info >= (3, 5, 4):
                    self.assertIn("local:", ret[0])
                    self.assertIn(
                        "[WARNING ] The log_file does not exist. Logging not setup correctly or syslog service not started.",
                        ret[1],
                    )
                    self.assertEqual(ret[2], 0)
                else:
                    self.assertIn(
                        "Failed to setup the Syslog logging handler", "\n".join(ret[1])
                    )
                    self.assertEqual(ret[2], 2)
            finally:
                if os.path.isdir(config_dir):
                    shutil.rmtree(config_dir)

    @skipIf(True, "This test is unreliable. Need to investigate why more deeply.")
    @flaky
    def test_issue_15074_output_file_append(self):
        output_file_append = os.path.join(RUNTIME_VARS.TMP, "issue-15074")
        try:
            # Let's create an initial output file with some data
            _ = self.run_script(
                "salt-call",
                "-c {0} --output-file={1} test.versions".format(
                    RUNTIME_VARS.TMP_MINION_CONF_DIR, output_file_append
                ),
                catch_stderr=True,
                with_retcode=True,
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
            )
            assert ret.exitcode == 0

            with salt.utils.files.fopen(output_file_append) as ofa:
                first_run_output = ofa.read()

            assert first_run_output

            ret = salt_call_cli.run(
                "--output-file",
                output_file_append,
                "--output-file-append",
                "test.versions",
            )
            assert ret.exitcode == 0

            with salt.utils.files.fopen(output_file_append) as ofa:
                second_run_output = ofa.read()

            assert second_run_output

            assert second_run_output == first_run_output + first_run_output

    @PRE_PYTEST_SKIP
    def test_issue_14979_output_file_permissions(self, salt_call_cli):
        with pytest.helpers.temp_file(name="issue-14979") as output_file:
            with salt.utils.files.set_umask(0o077):
                # Let's create an initial output file with some data
                ret = salt_call_cli.run("--output-file", output_file, "--grains")
                assert ret.exitcode == 0
                try:
                    stat1 = os.stat(output_file)
                except OSError:
                    pytest.fail("Failed to generate output file {}".format(output_file))

                # Let's change umask
                os.umask(0o777)  # pylint: disable=blacklisted-function

                ret = salt_call_cli.run(
                    "--output-file", output_file, "--output-file-append", "--grains"
                )
                assert ret.exitcode == 0
                stat2 = os.stat(output_file)
                assert stat1.st_mode == stat2.st_mode
                # Data was appeneded to file
                assert stat1.st_size < stat2.st_size

                # Let's remove the output file
                os.unlink(output_file)

                # Not appending data
                ret = salt_call_cli.run("--output-file", output_file, "--grains")
                assert ret.exitcode == 0
                try:
                    stat3 = os.stat(output_file)
                except OSError:
                    pytest.fail("Failed to generate output file {}".format(output_file))
                # Mode must have changed since we're creating a new log file
<<<<<<< HEAD
                assert stat1.st_mode != stat3.st_mode

    @pytest.mark.skip_on_windows(reason="This test does not apply on Win")
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_42116_cli_pillar_override(self, salt_call_cli):
        ret = salt_call_cli.run(
            "state.apply",
            "issue-42116-cli-pillar-override",
            pillar={"myhost": "localhost"},
        )
        state_run_dict = next(iter(ret.json.values()))
        assert state_run_dict["changes"]
        assert (
            state_run_dict["comment"] == 'Command "ping -c 2 localhost" run'
        ), "CLI pillar override not found in pillar data. State Run Dictionary:\n{}".format(
            pprint.pformat(state_run_dict)
=======
                self.assertNotEqual(stat1.st_mode, stat3.st_mode)
            finally:
                if os.path.exists(output_file):
                    os.unlink(output_file)

    @skipIf(sys.platform.startswith("win"), "This test does not apply on Win")
    @slowTest
    def test_42116_cli_pillar_override(self):
        ret = self.run_call(
            "state.apply issue-42116-cli-pillar-override "
            'pillar=\'{"myhost": "localhost"}\''
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_pillar_items_masterless(self, salt_call_cli):
=======
    @slowTest
    def test_pillar_items_masterless(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Test to ensure we get expected output
        from pillar.items with salt-call
        """
<<<<<<< HEAD
        ret = salt_call_cli.run("--local", "pillar.items")
        assert ret.exitcode == 0
        assert "knights" in ret.json
        assert sorted(ret.json["knights"]) == sorted(
            ["Lancelot", "Galahad", "Bedevere", "Robin"]
=======
        get_items = self.run_call("pillar.items", local=True)
        exp_out = [
            "        - Lancelot",
            "        - Galahad",
            "        - Bedevere",
            "    monty:",
            "        python",
        ]
        for out in exp_out:
            self.assertIn(out, get_items)

    def tearDown(self):
        """
        Teardown method to remove installed packages
        """
        user = ""
        user_info = self.run_call(" grains.get username", local=True)
        if (
            user_info
            and isinstance(user_info, (list, tuple))
            and isinstance(user_info[-1], six.string_types)
        ):
            user = user_info[-1].strip()
        super(CallTest, self).tearDown()

    @slowTest
    def test_exit_status_unknown_argument(self):
        """
        Ensure correct exit status when an unknown argument is passed to salt-call.
        """

        call = testprogram.TestProgramSaltCall(
            name="unknown_argument", parent_dir=self._test_dir,
        )
        # Call setup here to ensure config and script exist
        call.setup()
        stdout, stderr, status = call.run(
            args=["--unknown-argument"], catch_stderr=True, with_retcode=True,
        )
        self.assert_exit_status(
            status, "EX_USAGE", message="unknown argument", stdout=stdout, stderr=stderr
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        )
        assert "monty" in ret.json
        assert ret.json["monty"] == "python"

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_masterless_highstate(self, salt_call_cli):
=======
    @slowTest
    def test_masterless_highstate(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        test state.highstate in masterless mode
        """
        destpath = os.path.join(RUNTIME_VARS.TMP, "testfile")
        ret = salt_call_cli.run("--local", "state.highstate")
        assert ret.exitcode == 0
        state_run_dict = next(iter(ret.json.values()))
        assert state_run_dict["result"] is True
        assert state_run_dict["__id__"] == destpath

    @pytest.mark.skip_on_windows
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_syslog_file_not_found(self, salt_call_cli):
        """
        test when log_file is set to a syslog file that does not exist
        """
        old_cwd = os.getcwd()
        with pytest.helpers.temp_directory("log_file_incorrect") as config_dir:

            try:
                os.chdir(config_dir)
                src_config = os.path.join(RUNTIME_VARS.TMP_MINION_CONF_DIR, "minion")
                with salt.utils.files.fopen(src_config, "r") as fh_:
                    minion_config = salt.utils.yaml.load(fh_.read())
                    minion_config["log_file"] = "file:///dev/doesnotexist"
                    with salt.utils.files.fopen(
                        os.path.join(config_dir, "minion"), "w"
                    ) as fh_:
                        fh_.write(
                            salt.utils.yaml.dump(
                                minion_config, default_flow_style=False
                            )
                        )
                ret = salt_call_cli.run(
                    "--config-dir",
                    config_dir,
                    "--log-level=debug",
                    "cmd.run",
                    "echo foo",
                )
                if sys.version_info >= (3, 5, 4):
                    assert ret.exitcode == 0
                    assert (
                        "[WARNING ] The log_file does not exist. Logging not setup correctly or syslog service not started."
                        in ret.stderr
                    )
                    assert ret.json == "foo", ret
                else:
                    assert ret.exitcode == 2
                    assert "Failed to setup the Syslog logging handler" in ret.stderr
            finally:
                os.chdir(old_cwd)

    @PRE_PYTEST_SKIP
    @pytest.mark.skip_on_windows
    def test_return(self, salt_call_cli, salt_run_cli):
        command = "echo returnTOmaster"
        ret = salt_call_cli.run("cmd.run", command)
        assert ret.exitcode == 0
        assert ret.json == "returnTOmaster"

        ret = salt_run_cli.run("jobs.list_jobs")
        assert ret.exitcode == 0
        jid = target = None
        for jid, details in ret.json.items():
            if command in details["Arguments"]:
                target = details["Target"]
                break

        ret = salt_run_cli.run("jobs.lookup_jid", jid, _timeout=60)
        assert ret.exitcode == 0
        assert target in ret.json
        assert ret.json[target] == "returnTOmaster"

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_exit_status_unknown_argument(self, salt_call_cli):
=======
    @slowTest
    def test_exit_status_correct_usage(self):
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
        """
        Ensure correct exit status when an unknown argument is passed to salt CLI.
        """
        ret = salt_call_cli.run("--unknown-argument")
        assert ret.exitcode == salt.defaults.exitcodes.EX_USAGE, ret
        assert "Usage" in ret.stderr
        assert "no such option: --unknown-argument" in ret.stderr

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_exit_status_correct_usage(self, salt_call_cli):
        """
        Ensure correct exit status when salt CLI starts correctly.

        """
        ret = salt_call_cli.run("test.true")
        assert ret.exitcode == salt.defaults.exitcodes.EX_OK, ret
