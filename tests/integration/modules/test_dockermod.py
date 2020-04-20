# -*- coding: utf-8 -*-
"""
Integration tests for the docker_container states
"""

from __future__ import absolute_import, print_function, unicode_literals

import random
import string
import sys

import pytest
import salt.utils.path
from salt.ext.six.moves import range
from tests.support.case import ModuleCase
from tests.support.mixins import SaltReturnAssertsMixin
from tests.support.unit import skipIf


def _random_name(prefix=""):
    ret = prefix
    for _ in range(8):
        ret += random.choice(string.ascii_lowercase)
    return ret


@pytest.mark.destructive_test
@skipIf(not salt.utils.path.which("dockerd"), "Docker not installed")
class DockerCallTestCase(ModuleCase, SaltReturnAssertsMixin):
    """
    Test docker_container states
    """

    def setUp(self):
        """
        setup docker.call tests
        """
        # Create temp dir
        self.random_name = _random_name(prefix="salt_test_")
        self.image_tag = sys.version_info[0]

        self.run_state("docker_image.present", tag=self.image_tag, name="python")
        self.run_state(
            "docker_container.running",
            name=self.random_name,
            image="python:{0}".format(self.image_tag),
            entrypoint="tail -f /dev/null",
        )

    def tearDown(self):
        """
        teardown docker.call tests
        """
        self.run_state("docker_container.absent", name=self.random_name, force=True)
        self.run_state(
            "docker_image.absent",
            images=["python:{0}".format(self.image_tag)],
            force=True,
        )
        delattr(self, "random_name")
        delattr(self, "image_tag")

    def test_docker_call(self):
        """
        check that docker.call works, and works with a container not running as root
        """
        ret = self.run_function("docker.call", [self.random_name, "test.ping"])
        assert ret is True

    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
    def test_docker_sls(self):
        """
        check that docker.sls works, and works with a container not running as root
        """
        ret = self.run_function("docker.apply", [self.random_name, "core"])
        self.assertSaltTrueReturn(ret)

    @pytest.mark.slow_test(seconds=60)  # Test takes >30 and <=60 seconds
    def test_docker_highstate(self):
        """
        check that docker.highstate works, and works with a container not running as root
        """
        ret = self.run_function("docker.apply", [self.random_name])
        self.assertSaltTrueReturn(ret)
