# -*- coding: utf-8 -*-
'''
mac_power tests
'''

# Import python libs
from __future__ import absolute_import, unicode_literals, print_function

# Import Salt Testing Libs
from tests.support.unit import TestCase

# Import Salt Libs
import salt.modules.mac_power as mac_power
from salt.exceptions import SaltInvocationError
import pytest


class MacPowerTestCase(TestCase):
    '''
    test mac_power execution module
    '''
    def test_validate_sleep_valid_number(self):
        '''
        test _validate_sleep function with valid number
        '''
        assert mac_power._validate_sleep(179) == \
                         179

    def test_validate_sleep_invalid_number(self):
        '''
        test _validate_sleep function with invalid number
        '''
        with pytest.raises(SaltInvocationError):
            mac_power._validate_sleep(181)

    def test_validate_sleep_valid_string(self):
        '''
        test _validate_sleep function with valid string
        '''
        assert mac_power._validate_sleep('never') == \
                         'Never'
        assert mac_power._validate_sleep('off') == \
                         'Never'

    def test_validate_sleep_invalid_string(self):
        '''
        test _validate_sleep function with invalid string
        '''
        with pytest.raises(SaltInvocationError):
            mac_power._validate_sleep('bob')

    def test_validate_sleep_bool_true(self):
        '''
        test _validate_sleep function with True
        '''
        with pytest.raises(SaltInvocationError):
            mac_power._validate_sleep(True)

    def test_validate_sleep_bool_false(self):
        '''
        test _validate_sleep function with False
        '''
        assert mac_power._validate_sleep(False) == \
                         'Never'

    def test_validate_sleep_unexpected(self):
        '''
        test _validate_sleep function with True
        '''
        with pytest.raises(SaltInvocationError):
            mac_power._validate_sleep(172.7)
