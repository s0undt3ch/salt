# -*- coding: utf-8 -*-
"""
    :codeauthor: Pedro Algarvio (pedro@algarvio.me)


    tests.integration.states.match
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
<<<<<<< HEAD

=======
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
from __future__ import absolute_import, print_function, unicode_literals

import os

<<<<<<< HEAD
import pytest
import salt.utils.files
import salt.utils.stringutils
from tests.support.case import ModuleCase
=======
import salt.utils.files
import salt.utils.stringutils
from tests.support.case import ModuleCase
from tests.support.helpers import skip_if_not_root, slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
from tests.support.runtests import RUNTIME_VARS


class StateMatchTest(ModuleCase):
    """
    Validate the file state
    """

<<<<<<< HEAD
    @pytest.mark.skip_if_not_root
    @pytest.mark.slow_test(seconds=10)  # Test takes >5 and <=10 seconds
=======
    @skip_if_not_root
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_issue_2167_ipcidr_no_AttributeError(self):
        subnets = self.run_function("network.subnets")
        self.assertTrue(len(subnets) > 0)
        top_filename = "issue-2167-ipcidr-match.sls"
        top_file = os.path.join(RUNTIME_VARS.BASE_FILES, top_filename)
        try:
            with salt.utils.files.fopen(top_file, "w") as fp_:
                fp_.write(
                    salt.utils.stringutils.to_str(
                        "base:\n"
                        "  {0}:\n"
                        "    - match: ipcidr\n"
                        "    - test\n".format(subnets[0])
                    )
                )
            ret = self.run_function("state.top", [top_filename])
            self.assertNotIn(
                "AttributeError: 'Matcher' object has no attribute " "'functions'", ret
            )
        finally:
            os.remove(top_file)
