# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest
import salt.utils.platform
from tests.support.case import ModuleCase
from tests.support.helpers import slowTest
from tests.support.unit import skipIf


@skipIf(not salt.utils.platform.is_windows(), "windows tests only")
@pytest.mark.windows_whitelisted
class AutoRunsModuleTest(ModuleCase):
    """
    Test the autoruns module
    """

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_win_autoruns_list(self):
        """
        test win_autoruns.list module
        """
        ret = self.run_function("autoruns.list")
        self.assertIn("HKLM", str(ret))
        self.assertTrue(isinstance(ret, dict))
