# -*- coding: utf-8 -*-
"""
    :codeauthor: Nicole Thomas <nicole@saltstack.com>
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest
from salt.exceptions import CommandExecutionError
from salt.ext import six
from tests.support.case import ModuleCase

# Brew doesn't support local package installation - So, let's
# Grab some small packages available online for brew
ADD_PKG = "algol68g"
DEL_PKG = "acme"


@pytest.mark.destructive_test
@pytest.mark.skip_if_not_root
@pytest.mark.skip_unless_on_darwin
@pytest.mark.skip_if_binaries_missing("brew")
class BrewModuleTest(ModuleCase):
    """
    Integration tests for the brew module
    """

    @pytest.mark.slow_test(seconds=240)  # Test takes >120 and <=240 seconds
    def test_brew_install(self):
        """
        Tests the installation of packages
        """
        try:
            self.run_function("pkg.install", [ADD_PKG])
            pkg_list = self.run_function("pkg.list_pkgs")
            try:
                self.assertIn(ADD_PKG, pkg_list)
            except AssertionError:
                self.run_function("pkg.remove", [ADD_PKG])
                raise
        except CommandExecutionError:
            self.run_function("pkg.remove", [ADD_PKG])
            raise

    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_remove(self):
        """
        Tests the removal of packages
        """
        try:
            # Install a package to delete - If unsuccessful, skip the test
            self.run_function("pkg.install", [DEL_PKG])
            pkg_list = self.run_function("pkg.list_pkgs")
            if DEL_PKG not in pkg_list:
                self.run_function("pkg.install", [DEL_PKG])
                self.skipTest("Failed to install a package to delete")

            # Now remove the installed package
            self.run_function("pkg.remove", [DEL_PKG])
            del_list = self.run_function("pkg.list_pkgs")
            self.assertNotIn(DEL_PKG, del_list)
        except CommandExecutionError:
            self.run_function("pkg.remove", [DEL_PKG])
            raise

    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_version(self):
        """
        Test pkg.version for mac. Installs a package and then checks we can get
        a version for the installed package.
        """
        try:
            self.run_function("pkg.install", [ADD_PKG])
            pkg_list = self.run_function("pkg.list_pkgs")
            version = self.run_function("pkg.version", [ADD_PKG])
            try:
                self.assertTrue(
                    version,
                    msg=(
                        "version: {0} is empty,\
                                or other issue is present".format(
                            version
                        )
                    ),
                )
                self.assertIn(
                    ADD_PKG,
                    pkg_list,
                    msg=(
                        "package: {0} is not in\
                              the list of installed packages: {1}".format(
                            ADD_PKG, pkg_list
                        )
                    ),
                )
                # make sure the version is accurate and is listed in the pkg_list
                self.assertIn(
                    version,
                    six.text_type(pkg_list[ADD_PKG]),
                    msg=(
                        "The {0} version: {1} is \
                              not listed in the pkg_list: {2}".format(
                            ADD_PKG, version, pkg_list[ADD_PKG]
                        )
                    ),
                )
            except AssertionError:
                self.run_function("pkg.remove", [ADD_PKG])
                raise
        except CommandExecutionError:
            self.run_function("pkg.remove", [ADD_PKG])
            raise

    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_latest_version(self):
        """
        Test pkg.latest_version:
          - get the latest version available
          - install the package
          - get the latest version available
          - check that the latest version is empty after installing it
        """
        try:
            self.run_function("pkg.remove", [ADD_PKG])
            uninstalled_latest = self.run_function("pkg.latest_version", [ADD_PKG])

            self.run_function("pkg.install", [ADD_PKG])
            installed_latest = self.run_function("pkg.latest_version", [ADD_PKG])
            version = self.run_function("pkg.version", [ADD_PKG])
            try:
                self.assertTrue(isinstance(uninstalled_latest, six.string_types))
                self.assertEqual(installed_latest, version)
            except AssertionError:
                self.run_function("pkg.remove", [ADD_PKG])
                raise
        except CommandExecutionError:
            self.run_function("pkg.remove", [ADD_PKG])
            raise

    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
    def test_refresh_db(self):
        """
        Integration test to ensure pkg.refresh_db works with brew
        """
        refresh_brew = self.run_function("pkg.refresh_db")
        self.assertTrue(refresh_brew)

    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
    def test_list_upgrades(self):
        """
        Test pkg.list_upgrades: data is in the form {'name1': 'version1',
        'name2': 'version2', ... }
        """
        try:
            upgrades = self.run_function("pkg.list_upgrades")
            try:
                self.assertTrue(isinstance(upgrades, dict))
                if upgrades:
                    for name in upgrades:
                        self.assertTrue(isinstance(name, six.string_types))
                        self.assertTrue(isinstance(upgrades[name], six.string_types))
            except AssertionError:
                self.run_function("pkg.remove", [ADD_PKG])
                raise
        except CommandExecutionError:
            self.run_function("pkg.remove", [ADD_PKG])
            raise

    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
    def test_info_installed(self):
        """
        Test pkg.info_installed: info returned has certain fields used by
        mac_brew.latest_version
        """
        try:
            self.run_function("pkg.install", [ADD_PKG])
            info = self.run_function("pkg.info_installed", [ADD_PKG])
            try:
                self.assertTrue(ADD_PKG in info)
                self.assertTrue("versions" in info[ADD_PKG])
                self.assertTrue("revision" in info[ADD_PKG])
                self.assertTrue("stable" in info[ADD_PKG]["versions"])
            except AssertionError:
                self.run_function("pkg.remove", [ADD_PKG])
                raise
        except CommandExecutionError:
            self.run_function("pkg.remove", [ADD_PKG])
            raise

    def tearDown(self):
        """
        Clean up after tests
        """
        pkg_list = self.run_function("pkg.list_pkgs")

        # Remove any installed packages
        if ADD_PKG in pkg_list:
            self.run_function("pkg.remove", [ADD_PKG])
        if DEL_PKG in pkg_list:
            self.run_function("pkg.remove", [DEL_PKG])
