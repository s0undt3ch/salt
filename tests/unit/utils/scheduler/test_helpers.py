# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging

import pytest
from tests.unit.utils.scheduler.base import SchedulerTestsBase

log = logging.getLogger(__name__)


class SchedulerHelpersTest(SchedulerTestsBase):
    """
    Test scheduler helper functions
    """

    def setUp(self):
        super(SchedulerHelpersTest, self).setUp()
        self.schedule.opts["loop_interval"] = 1

    @pytest.mark.slow_test(seconds=1)  # Test takes >0.1 and <=1 seconds
    def test_get_schedule(self):
        """
        verify that the _get_schedule function works
        when remove_hidden is True and schedule data
        contains enabled key
        """
        job_name = "test_get_schedule"
        job = {
            "schedule": {
                "enabled": True,
                job_name: {"function": "test.ping", "seconds": 60},
            }
        }
        # Add the job to the scheduler
        self.schedule.opts.update(job)

        ret = self.schedule._get_schedule(remove_hidden=True)
        self.assertEqual(job["schedule"], ret)
