# -*- coding: utf-8 -*-

# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals

# Import Salt Testing libs
from tests.support.case import SyndicCase

import pytest


@pytest.mark.windows_whitelisted
class TestSyndic(SyndicCase):
    '''
    Validate the syndic interface by testing the test module
    '''
    def test_ping(self):
        '''
        test.ping
        '''
        assert self.run_function('test.ping')

    def test_fib(self):
        '''
        test.fib
        '''
        assert self.run_function(
                    'test.fib',
                    ['20'],
                    )[0] == \
                6765
