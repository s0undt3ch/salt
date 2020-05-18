# -*- coding: utf-8 -*-

# Import python libs
from __future__ import absolute_import, print_function, unicode_literals

import logging

import pytest

# Import Salt Testing libs
from tests.support.case import ModuleCase, ShellCase
<<<<<<< HEAD
=======
from tests.support.helpers import slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc

log = logging.getLogger(__name__)


class ExecutorTest(ModuleCase, ShellCase):
    def setup(self):
        self.run_function("saltutil.sync_all")

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_executor(self):
        """
        test that dunders are set
        """
        data = self.run_call("test.arg --module-executors=arg")
        self.assertIn("test.arg fired", "".join(data))
