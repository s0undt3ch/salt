# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import pytest
from tests.support.case import ModuleCase
<<<<<<< HEAD
=======
from tests.support.helpers import slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@pytest.mark.windows_whitelisted
class AliasesTest(ModuleCase):
    """
    Validate aliases module
    """

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_set_target(self):
        """
        aliases.set_target and aliases.get_target
        """
        set_ret = self.run_function("aliases.set_target", alias="fred", target="bob")
        self.assertTrue(set_ret)
        tgt_ret = self.run_function("aliases.get_target", alias="fred")
        self.assertEqual(tgt_ret, "bob")

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_has_target(self):
        """
        aliases.set_target and aliases.has_target
        """
        set_ret = self.run_function("aliases.set_target", alias="fred", target="bob")
        self.assertTrue(set_ret)
        tgt_ret = self.run_function("aliases.has_target", alias="fred", target="bob")
        self.assertTrue(tgt_ret)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_list_aliases(self):
        """
        aliases.list_aliases
        """
        set_ret = self.run_function("aliases.set_target", alias="fred", target="bob")
        self.assertTrue(set_ret)
        tgt_ret = self.run_function("aliases.list_aliases")
        self.assertIsInstance(tgt_ret, dict)
        self.assertIn("fred", tgt_ret)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_rm_alias(self):
        """
        aliases.rm_alias
        """
        set_ret = self.run_function("aliases.set_target", alias="frank", target="greg")
        self.assertTrue(set_ret)
        self.run_function("aliases.rm_alias", alias="frank")
        tgt_ret = self.run_function("aliases.list_aliases")
        self.assertIsInstance(tgt_ret, dict)
        self.assertNotIn("alias=frank", tgt_ret)
