# -*- coding: utf-8 -*-
"""
    integration.cli_test
    ~~~~~~~~~~~~~~~~~~~~

    CLI related unit testing

    :codeauthor: Pedro Algarvio (pedro@algarvio.me)
"""
from __future__ import absolute_import, print_function

<<<<<<< HEAD
import pytest

# Import 3rd-party libs
=======
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
# pylint: disable=import-error
from salt.ext.six.moves import range  # pylint: disable=redefined-builtin
from tests.support.case import ShellCase
from tests.support.helpers import slowTest
from tests.support.mixins import ShellCaseCommonTestsMixin
from tests.support.unit import skipIf

try:
    import libcloud  # pylint: disable=unused-import

    HAS_LIBCLOUD = True
except ImportError:
    HAS_LIBCLOUD = False
# pylint: enable=import-error


@skipIf(HAS_LIBCLOUD is False, "salt-cloud requires >= libcloud 0.11.4")
@pytest.mark.slow_test(seconds=5)  # Inheritance used. Skip the whole class
class SaltCloudCliTest(ShellCase, ShellCaseCommonTestsMixin):

    _call_binary_ = "salt-cloud"

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_function_arguments(self):
        self.assertIn(
            "error: --function expects two arguments: " "<function-name> <provider>",
            "\n".join(self.run_cloud("--function show_image -h", catch_stderr=True)[1]),
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=5)  # Test takes >1 and <=5 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_list_providers_accepts_no_arguments(self):
        self.assertIn(
            "error: '--list-providers' does not accept any " "arguments",
            "\n".join(self.run_cloud("--list-providers ec2", catch_stderr=True)[1]),
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_mutually_exclusive_query_options(self):
        test_options = ["--query", "--full-query", "--select-query", "--list-providers"]
        while True:
            for idx in range(1, len(test_options)):
                self.assertIn(
                    "error: The options {0}/{1} are mutually "
                    "exclusive. Please only choose one of them".format(
                        test_options[0], test_options[idx]
                    ),
                    "\n".join(
                        self.run_cloud(
                            "{0} {1}".format(test_options[0], test_options[idx]),
                            catch_stderr=True,
                        )[1]
                    ),
                )
            # Remove the first option from the list
            test_options.pop(0)
            if len(test_options) <= 1:
                # Only one left? Stop iterating
                break

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_mutually_exclusive_list_options(self):
        test_options = ["--list-locations", "--list-images", "--list-sizes"]
        while True:
            for idx in range(1, len(test_options)):
                output = self.run_cloud(
                    "{0} ec2 {1} ec2".format(test_options[0], test_options[idx]),
                    catch_stderr=True,
                )
                try:
                    self.assertIn(
                        "error: The options {0}/{1} are mutually "
                        "exclusive. Please only choose one of them".format(
                            test_options[0], test_options[idx]
                        ),
                        "\n".join(output[1]),
                    )
                except AssertionError:
                    print(output)
                    raise
            # Remove the first option from the list
            test_options.pop(0)
            if len(test_options) <= 1:
                # Only one left? Stop iterating
                break
