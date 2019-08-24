# -*- coding: utf-8 -*-
'''
Tests for the librato returner
'''
# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals
import logging

# Import Salt Testing libs
from tests.support.case import TestCase

# Import salt libs
from salt.returners import librato_return

log = logging.getLogger(__name__)


class LibratoTest(TestCase):
    '''
    Test the librato returner
    '''

    def test_count_runtimes(self):
        '''
        Test the calculations
        '''
        # JOBS DIR and FILES
        mock_ret_obj = {
            "fun_args": [],
            "return": {
                "test-return-state": {
                    "comment": "insertcommenthere",
                    "name": "test-state-1",
                    "start_time": "01: 19: 51.105566",
                    "result": True,
                    "duration": 3.645,
                    "__run_num__": 193,
                    "changes": {},
                    "__id__": "test-return-state"
                },
                "test-return-state2": {
                    "comment": "insertcommenthere",
                    "name": "test-state-2",
                    "start_time": "01: 19: 51.105566",
                    "result": False,
                    "duration": 3.645,
                    "__run_num__": 194,
                    "changes": {},
                    "__id__": "test-return-state"
                }
            },
            "retcode": 2,
            "success": True,
            "fun": "state.highstate",
            "id": "Librato-Test",
            "out": "highstate"
        }

        results = librato_return._calculate_runtimes(mock_ret_obj['return'])
        self.assertEqual(results['num_failed_states'], 1)
        self.assertEqual(results['num_passed_states'], 1)
        self.assertEqual(results['runtime'], 7.29)
