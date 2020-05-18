# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import pytest
from tests.support.case import ModuleCase
<<<<<<< HEAD
=======
from tests.support.helpers import slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@pytest.mark.windows_whitelisted
class DataModuleTest(ModuleCase):
    """
    Validate the data module
    """

    def setUp(self):
        self.run_function("data.clear")
        self.addCleanup(self.run_function, "data.clear")

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_load_dump(self):
        """
        data.load
        data.dump
        """
        self.assertTrue(self.run_function("data.dump", ['{"foo": "bar"}']))
        self.assertEqual(self.run_function("data.load"), {"foo": "bar"})

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_get_update(self):
        """
        data.get
        data.update
        """
        self.assertTrue(self.run_function("data.update", ["spam", "eggs"]))
        self.assertEqual(self.run_function("data.get", ["spam"]), "eggs")

        self.assertTrue(self.run_function("data.update", ["unladen", "swallow"]))
        self.assertEqual(
            self.run_function("data.get", [["spam", "unladen"]]), ["eggs", "swallow"]
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_cas_update(self):
        """
        data.update
        data.cas
        data.get
        """
        self.assertTrue(self.run_function("data.update", ["spam", "eggs"]))
        self.assertTrue(self.run_function("data.cas", ["spam", "green", "eggs"]))
        self.assertEqual(self.run_function("data.get", ["spam"]), "green")
