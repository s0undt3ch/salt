# -*- coding: utf-8 -*-

# Import Python libs
from __future__ import absolute_import

# Import Salt Testing libs
from tests.support.case import ModuleCase
from tests.support.unit import skipIf

# Import Salt libs
import salt.utils.platform

import pytest


@skipIf(not salt.utils.platform.is_windows(), 'windows tests only')
@pytest.mark.windows_whitelisted
class AutoRunsModuleTest(ModuleCase):
    '''
    Test the autoruns module
    '''
    def test_win_autoruns_list(self):
        '''
        test win_autoruns.list module
        '''
        ret = self.run_function('autoruns.list')
        assert 'HKLM' in str(ret)
        assert isinstance(ret, dict)
