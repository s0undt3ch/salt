# -*- coding: utf-8 -*-
'''
    :codeauthor: Jayesh Kariya <jayeshk@saltstack.com>
'''
# Import Python libs
from __future__ import absolute_import, unicode_literals, print_function

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import TestCase
from tests.support.mock import (
    MagicMock,
    patch
)

# Import Salt Libs
import salt.states.splunk_search as splunk_search


class SplunkSearchTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test cases for salt.states.splunk_search
    '''
    def setup_loader_modules(self):
        return {splunk_search: {}}

    # 'present' function tests: 1

    def test_present(self):
        '''
        Test to ensure a search is present.
        '''
        name = 'API Error Search'

        ret = {'name': name,
               'changes': {},
               'result': None,
               'comment': ''}

        mock = MagicMock(side_effect=[True, False, False, True])
        with patch.dict(splunk_search.__salt__, {'splunk_search.get': mock,
                                                 'splunk_search.create': mock}):
            with patch.dict(splunk_search.__opts__, {'test': True}):
                comt = ("Would update {0}".format(name))
                ret.update({'comment': comt})
                assert splunk_search.present(name) == ret

                comt = ("Would create {0}".format(name))
                ret.update({'comment': comt})
                assert splunk_search.present(name) == ret

            with patch.dict(splunk_search.__opts__, {'test': False}):
                ret.update({'comment': '', 'result': True,
                            'changes': {'new': {}, 'old': False}})
                assert splunk_search.present(name) == ret

    # 'absent' function tests: 1

    def test_absent(self):
        '''
        Test to ensure a search is absent.
        '''
        name = 'API Error Search'

        ret = {'name': name,
               'result': None,
               'comment': ''}

        mock = MagicMock(side_effect=[True, False])
        with patch.dict(splunk_search.__salt__, {'splunk_search.get': mock}):
            with patch.dict(splunk_search.__opts__, {'test': True}):
                comt = ("Would delete {0}".format(name))
                ret.update({'comment': comt})
                assert splunk_search.absent(name) == ret

            comt = ('{0} is absent.'.format(name))
            ret.update({'comment': comt, 'result': True,
                        'changes': {}})
            assert splunk_search.absent(name) == ret
