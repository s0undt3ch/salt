# -*- coding: utf-8 -*-
'''
    :codeauthor: Jayesh Kariya <jayeshk@saltstack.com>
'''
# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import TestCase
from tests.support.mock import (
    MagicMock,
    patch
)

# Import Salt Libs
import salt.states.schedule as schedule


class ScheduleTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test cases for salt.states.schedule
    '''
    def setup_loader_modules(self):
        return {schedule: {}}

    # 'present' function tests: 1

    def test_present(self):
        '''
        Test to ensure a job is present in the schedule.
        '''
        name = 'job1'

        ret = {'name': name,
               'changes': {},
               'result': False,
               'comment': ''}

        mock_dict = MagicMock(side_effect=[ret, []])
        mock_mod = MagicMock(return_value=ret)
        mock_lst = MagicMock(side_effect=[{name: {}}, {name: {}}, {}, {}])
        with patch.dict(schedule.__salt__,
                        {'schedule.list': mock_lst,
                         'schedule.build_schedule_item': mock_dict,
                         'schedule.modify': mock_mod,
                         'schedule.add': mock_mod}):
            assert schedule.present(name) == ret

            with patch.dict(schedule.__opts__, {'test': False}):
                assert schedule.present(name) == ret

                assert schedule.present(name) == ret

            with patch.dict(schedule.__opts__, {'test': True}):
                ret.update({'result': True})
                assert schedule.present(name) == ret

    # 'absent' function tests: 1

    def test_absent(self):
        '''
        Test to ensure a job is absent from the schedule.
        '''
        name = 'job1'

        ret = {'name': name,
               'changes': {},
               'result': False,
               'comment': ''}

        mock_mod = MagicMock(return_value=ret)
        mock_lst = MagicMock(side_effect=[{name: {}}, {}])
        with patch.dict(schedule.__salt__,
                        {'schedule.list': mock_lst,
                         'schedule.delete': mock_mod}):
            with patch.dict(schedule.__opts__, {'test': False}):
                assert schedule.absent(name) == ret

            with patch.dict(schedule.__opts__, {'test': True}):
                comt = ('Job job1 not present in schedule')
                ret.update({'comment': comt, 'result': True})
                assert schedule.absent(name) == ret
