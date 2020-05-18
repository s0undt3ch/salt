# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import pytest
from tests.support.case import ModuleCase
<<<<<<< HEAD
=======
from tests.support.helpers import slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@pytest.mark.windows_whitelisted
class DecoratorTest(ModuleCase):
<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_module(self):
        self.assertTrue(self.run_function("runtests_decorators.working_function"))

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
    def test_module(self):
        self.assertTrue(self.run_function("runtests_decorators.working_function"))

    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_depends(self):
        ret = self.run_function("runtests_decorators.depends")
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue(ret["ret"])
        self.assertTrue(isinstance(ret["time"], float))

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_missing_depends(self):
        self.assertEqual(
            {
                "runtests_decorators.missing_depends_will_fallback": None,
                "runtests_decorators.missing_depends": "'runtests_decorators.missing_depends' is not available.",
            },
            self.run_function("runtests_decorators.missing_depends"),
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_bool_depends(self):
        # test True
        self.assertTrue(self.run_function("runtests_decorators.booldependsTrue"))

        # test False
        self.assertIn(
            "is not available",
            self.run_function("runtests_decorators.booldependsFalse"),
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_depends_will_not_fallback(self):
        ret = self.run_function("runtests_decorators.depends_will_not_fallback")
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue(ret["ret"])
        self.assertTrue(isinstance(ret["time"], float))

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_missing_depends_will_fallback(self):
        self.assertListEqual(
            [False, "fallback"],
            self.run_function("runtests_decorators.missing_depends_will_fallback"),
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_command_success_retcode(self):
        ret = self.run_function("runtests_decorators.command_success_retcode")
        self.assertIs(ret, True)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_command_failure_retcode(self):
        ret = self.run_function("runtests_decorators.command_failure_retcode")
        self.assertEqual(
            ret, "'runtests_decorators.command_failure_retcode' is not available."
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_command_success_nonzero_retcode_true(self):
        ret = self.run_function(
            "runtests_decorators.command_success_nonzero_retcode_true"
        )
        self.assertIs(ret, True)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_command_failure_nonzero_retcode_true(self):
        ret = self.run_function(
            "runtests_decorators.command_failure_nonzero_retcode_true"
        )
        self.assertEqual(
            ret,
            "'runtests_decorators.command_failure_nonzero_retcode_true' is not available.",
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_command_success_nonzero_retcode_false(self):
        ret = self.run_function(
            "runtests_decorators.command_success_nonzero_retcode_false"
        )
        self.assertIs(ret, True)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_command_failure_nonzero_retcode_false(self):
        ret = self.run_function(
            "runtests_decorators.command_failure_nonzero_retcode_false"
        )
        self.assertEqual(
            ret,
            "'runtests_decorators.command_failure_nonzero_retcode_false' is not available.",
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_versioned_depend_insufficient(self):
        self.assertIn(
            "is not available",
            self.run_function("runtests_decorators.version_depends_false"),
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
    def test_versioned_depend_sufficient(self):
        self.assertTrue(self.run_function("runtests_decorators.version_depends_true"))

    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
    def test_versioned_depend_sufficient(self):
        self.assertTrue(self.run_function("runtests_decorators.version_depends_true"))

    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_versioned_depend_versionless(self):
        self.assertTrue(
            self.run_function("runtests_decorators.version_depends_versionless_true")
        )
