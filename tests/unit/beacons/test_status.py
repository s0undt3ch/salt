# -*- coding: utf-8 -*-
"""
    :codeauthor: Pedro Algarvio (pedro@algarvio.me)
    :copyright: Copyright 2017 by the SaltStack Team, see AUTHORS for more details.


    tests.unit.beacons.test_status
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Status beacon test cases
"""
from __future__ import absolute_import

<<<<<<< HEAD
import pytest

# Salt libs
=======
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
import salt.config
import salt.loader
import salt.modules.status as status_module
from salt.beacons import status
from tests.support.helpers import slowTest
from tests.support.mixins import LoaderModuleMockMixin
<<<<<<< HEAD

# Salt testing libs
=======
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
from tests.support.unit import TestCase


class StatusBeaconTestCase(TestCase, LoaderModuleMockMixin):
    """
    Test case for salt.beacons.status
    """

    def setup_loader_modules(self):
        opts = salt.config.DEFAULT_MINION_OPTS.copy()
        opts["grains"] = salt.loader.grains(opts)
        module_globals = {
            "__opts__": opts,
            "__salt__": "autoload",
            "__context__": {},
            "__grains__": opts["grains"],
        }
        return {status: module_globals, status_module: module_globals}

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_empty_config(self, *args, **kwargs):
        config = []

        ret = status.validate(config)
        self.assertEqual(ret, (True, "Valid beacon configuration"))

        ret = status.beacon(config)
        expected = sorted(["loadavg", "meminfo", "cpustats", "vmstats", "time"])

        self.assertEqual(sorted(list(ret[0]["data"])), expected)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_deprecated_dict_config(self):
        config = {"time": ["all"]}

        ret = status.validate(config)
        self.assertEqual(
            ret, (False, "Configuration for status beacon must be a list.")
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_list_config(self):
        config = [{"time": ["all"]}]

        ret = status.validate(config)
        self.assertEqual(ret, (True, "Valid beacon configuration"))

        ret = status.beacon(config)
        expected = ["time"]

        self.assertEqual(list(ret[0]["data"]), expected)
