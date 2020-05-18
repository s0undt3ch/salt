# -*- coding: utf-8 -*-
"""
    :codeauthor: Alexander Pyatkin <asp@thexyz.net
"""
from __future__ import absolute_import, print_function, unicode_literals

<<<<<<< HEAD
import pytest
import salt.utils.json
import salt.utils.path
from tests.support.case import ModuleCase
=======
import salt.utils.json
import salt.utils.path
from tests.support.case import ModuleCase
from tests.support.helpers import destructiveTest, slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
from tests.support.mixins import SaltReturnAssertsMixin
from tests.support.unit import skipIf


@skipIf(salt.utils.path.which("bower") is None, "bower not installed")
class BowerStateTest(ModuleCase, SaltReturnAssertsMixin):
<<<<<<< HEAD
    @pytest.mark.destructive_test
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
=======
    @destructiveTest
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_bower_installed_removed(self):
        """
        Basic test to determine if Bower package was successfully installed and
        removed.
        """
        ret = self.run_state("file.directory", name="/salt_test_bower_1", makedirs=True)
        self.assertSaltTrueReturn(ret)
        ret = self.run_state(
            "bower.installed", name="underscore", dir="/salt_test_bower_1"
        )
        self.assertSaltTrueReturn(ret)
        ret = self.run_state(
            "bower.removed", name="underscore", dir="/salt_test_bower_1"
        )
        self.assertSaltTrueReturn(ret)
        ret = self.run_state("file.absent", name="/salt_test_bower_1")
        self.assertSaltTrueReturn(ret)

<<<<<<< HEAD
    @pytest.mark.destructive_test
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
=======
    @destructiveTest
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_bower_installed_pkgs(self):
        """
        Basic test to determine if Bower package successfully installs multiple
        packages.
        """
        ret = self.run_state("file.directory", name="/salt_test_bower_2", makedirs=True)
        self.assertSaltTrueReturn(ret)
        ret = self.run_state(
            "bower.installed",
            name="test",
            dir="/salt_test_bower_2",
            pkgs=["numeral", "underscore"],
        )
        self.assertSaltTrueReturn(ret)
        ret = self.run_state("file.absent", name="/salt_test_bower_2")
        self.assertSaltTrueReturn(ret)

<<<<<<< HEAD
    @pytest.mark.destructive_test
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
=======
    @destructiveTest
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_bower_installed_from_file(self):
        ret = self.run_state("file.directory", name="/salt_test_bower_3", makedirs=True)
        self.assertSaltTrueReturn(ret)
        bower_json = salt.utils.json.dumps(
            {
                "name": "salt_test_bower_3",
                "dependencies": {"numeral": "~1.5.3", "underscore": "~1.7.0"},
            }
        )
        ret = self.run_state(
            "file.managed", name="/salt_test_bower_3/bower.json", contents=bower_json
        )
        self.assertSaltTrueReturn(ret)
        ret = self.run_state("bower.bootstrap", name="/salt_test_bower_3")
        self.assertSaltTrueReturn(ret)
        ret = self.run_state("file.absent", name="/salt_test_bower_3")
        self.assertSaltTrueReturn(ret)
