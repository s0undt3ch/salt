# -*- coding: utf-8 -*-
"""
Integration tests for the zookeeper states
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging

import pytest
import salt.utils.path
from tests.support.case import ModuleCase
<<<<<<< HEAD
=======
from tests.support.helpers import destructiveTest, slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
from tests.support.mixins import SaltReturnAssertsMixin
from tests.support.unit import skipIf

try:
    import kazoo  # pylint: disable=import-error,unused-import

    HAS_KAZOO = True
except ImportError:
    HAS_KAZOO = False

log = logging.getLogger(__name__)


@pytest.mark.destructive_test
@skipIf(not salt.utils.path.which("dockerd"), "Docker not installed")
@skipIf(not HAS_KAZOO, "kazoo python library not installed")
class ZookeeperTestCase(ModuleCase, SaltReturnAssertsMixin):
    """
    Test zookeeper states
    """

    @classmethod
    def setUpClass(cls):
        cls.container_name = "zookeeper_salt"

    def setUp(self):
        self.run_state("docker_image.present", name="zookeeper")
        self.run_state(
            "docker_container.running",
            name=self.container_name,
            image="zookeeper",
            port_bindings="2181:2181",
        )

    def tearDown(self):
        self.run_state("docker_container.stopped", name=self.container_name)
        self.run_state("docker_container.absent", name=self.container_name)
        self.run_state("docker_image.absent", name="docker.io/zookeeper", force=True)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_zookeeper_present(self):
        ret = self.run_state(
            "zookeeper.present", name="/test/name", value="testuser", makepath=True,
        )
        self.assertSaltTrueReturn(ret)

        ret = self.run_state(
            "zookeeper.present",
            name="/test/name",
            value="daniel",
            acls=[
                {
                    "username": "daniel",
                    "password": "test",
                    "read": True,
                    "admin": True,
                    "write": True,
                },
                {"username": "testuser", "password": "test", "read": True},
            ],
            profile="prod",
        )
        self.assertSaltTrueReturn(ret)

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=120)  # Test takes >60 and <=120 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_zookeeper_absent(self):
        self.run_state(
            "zookeeper.present", name="/test/name", value="testuser", makepath=True,
        )
        ret = self.run_state("zookeeper.absent", name="/test/name",)
        self.assertSaltTrueReturn(ret)
        self.assertTrue(
            bool(ret["zookeeper_|-/test/name_|-/test/name_|-absent"]["changes"])
        )
        ret = self.run_state("zookeeper.absent", name="/test/name",)
        self.assertFalse(
            bool(ret["zookeeper_|-/test/name_|-/test/name_|-absent"]["changes"])
        )

<<<<<<< HEAD
    @pytest.mark.slow_test(seconds=30)  # Test takes >10 and <=30 seconds
=======
    @slowTest
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_zookeeper_acls(self):
        ret = self.run_state(
            "zookeeper.acls",
            name="/test/name",
            acls=[
                {
                    "username": "daniel",
                    "password": "test",
                    "read": True,
                    "admin": True,
                    "write": True,
                },
                {"username": "testuser", "password": "test", "read": True},
            ],
        )
        self.assertSaltFalseReturn(ret)

        ret = self.run_state(
            "zookeeper.present", name="/test/name", value="testuser", makepath=True,
        )

        ret = self.run_state(
            "zookeeper.acls",
            name="/test/name",
            acls=[
                {
                    "username": "daniel",
                    "password": "test",
                    "read": True,
                    "admin": True,
                    "write": True,
                },
                {"username": "testuser", "password": "test", "read": True},
            ],
        )
        self.assertSaltTrueReturn(ret)
