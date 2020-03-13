# -*- coding: utf-8 -*-

# Import Python libs
from __future__ import absolute_import

# Import Salt Testing libs
from tests.support.case import ModuleCase
from tests.support.unit import skipIf

# Import Salt libs
import salt.utils.platform

import pytest


@skipIf(not salt.utils.platform.is_windows(), 'windows test only')
@pytest.mark.windows_whitelisted
class WinServermanagerTest(ModuleCase):
    '''
    Test for salt.modules.win_servermanager
    '''
    def test_list_available(self):
        '''
        Test list available features to install
        '''
        cmd = self.run_function('win_servermanager.list_available')
        assert 'DNS' in cmd
        assert 'NetworkController' in cmd
        assert 'RemoteAccess' in cmd
