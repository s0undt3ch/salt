# -*- coding: utf-8 -*-
"""
Test the saltcheck module
"""
from __future__ import absolute_import, print_function, unicode_literals

<<<<<<< HEAD
import pytest

# Import Salt Testing libs
from tests.support.case import ModuleCase
=======
from tests.support.case import ModuleCase
from tests.support.helpers import slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


class SaltcheckModuleTest(ModuleCase):
    """
    Test the saltcheck module
    """

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_saltcheck_run(self):
        """
        saltcheck.run_test
        """
        saltcheck_test = {
            "module_and_function": "test.echo",
            "assertion": "assertEqual",
            "expected_return": "This works!",
            "args": ["This works!"],
        }
        ret = self.run_function("saltcheck.run_test", test=saltcheck_test)
        self.assertDictContainsSubset({"status": "Pass"}, ret)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_saltcheck_state(self):
        """
        saltcheck.run_state_tests
        """
        saltcheck_test = "validate-saltcheck"
        ret = self.run_function("saltcheck.run_state_tests", [saltcheck_test])
        self.assertDictContainsSubset(
            {"status": "Pass"}, ret[0]["validate-saltcheck"]["echo_test_hello"]
        )
        self.assertDictContainsSubset({"Failed": 0}, ret[1]["TEST RESULTS"])

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_topfile_validation(self):
        """
        saltcheck.run_highstate_tests
        """
        expected_top_states = self.run_function("state.show_top").get("base", [])
        expected_top_states.append("TEST RESULTS")
        ret = self.run_function("saltcheck.run_highstate_tests")
        for top_state_dict in ret:
            self.assertIn(list(top_state_dict)[0], expected_top_states)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_saltcheck_checkall(self):
        """
        Validate saltcheck.run_state_tests check_all for the default saltenv of base.
        validate-saltcheck state hosts a saltcheck-tests directory with 2 .tst files. By running
          check_all=True, both files should be found and show passed results.
        """
        saltcheck_test = "validate-saltcheck"
        ret = self.run_function(
            "saltcheck.run_state_tests", [saltcheck_test], check_all=True
        )
        self.assertDictContainsSubset(
            {"status": "Pass"}, ret[0]["validate-saltcheck"]["echo_test_hello"]
        )
        self.assertDictContainsSubset(
            {"status": "Pass"}, ret[0]["validate-saltcheck"]["check_all_validate"]
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_saltcheck_checkall_saltenv(self):
        """
        Validate saltcheck.run_state_tests check_all for the prod saltenv
        validate-saltcheck state hosts a saltcheck-tests directory with 2 .tst files. By running
          check_all=True, both files should be found and show passed results.
        """
        saltcheck_test = "validate-saltcheck"
        ret = self.run_function(
            "saltcheck.run_state_tests",
            [saltcheck_test],
            saltenv="prod",
            check_all=True,
        )
        self.assertDictContainsSubset(
            {"status": "Pass"}, ret[0]["validate-saltcheck"]["echo_test_prod_env"]
        )
        self.assertDictContainsSubset(
            {"status": "Pass"}, ret[0]["validate-saltcheck"]["check_all_validate_prod"]
        )
