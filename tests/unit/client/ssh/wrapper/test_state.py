# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`saltybob <bbaker@saltstack.com`
'''
from __future__ import absolute_import

# Import python libs

# Import Salt Testing libs
from tests.support.unit import TestCase

# Import Salt libs
from salt.client.ssh.wrapper import state


class StateTests(TestCase):
    def test_parse_mods(self):
        '''
        Test _parse_mods
        '''
        expected = ['a', 'b', 'c', 'd', 'e', 'f']
        mods = 'a,b, c,  d,e ,f  '

        actual = state._parse_mods(mods)
        assert expected == actual
