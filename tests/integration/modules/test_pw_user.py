# -*- coding: utf-8 -*-
"""
    :codeauthor: Pedro Algarvio (pedro@algarvio.me)

    tests.integration.modules.pw_user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from __future__ import absolute_import, print_function, unicode_literals

from tests.support.case import ModuleCase
<<<<<<< HEAD
from tests.support.helpers import random_string
=======
from tests.support.helpers import (
    destructiveTest,
    random_string,
    runs_on,
    skip_if_not_root,
)
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc


@runs_on(kernel="FreeBSD")
class PwUserModuleTest(ModuleCase):
<<<<<<< HEAD
    @pytest.mark.destructive_test
    @pytest.mark.skip_if_not_root
=======
    @destructiveTest
    @skip_if_not_root
>>>>>>> 9478961652890061dfd444737f3b6353806cb5fc
    def test_groups_includes_primary(self):
        # Let's create a user, which usually creates the group matching the name
        uname = random_string("PWU-", lowercase=False)
        if self.run_function("user.add", [uname]) is not True:
            # Skip because creating is not what we're testing here
            self.run_function("user.delete", [uname, True, True])
            self.skipTest("Failed to create user")

        try:
            uinfo = self.run_function("user.info", [uname])
            self.assertIn(uname, uinfo["groups"])

            # This uid is available, store it
            uid = uinfo["uid"]

            self.run_function("user.delete", [uname, True, True])

            # Now, a weird group id
            gname = random_string("PWU-", lowercase=False)
            if self.run_function("group.add", [gname]) is not True:
                self.run_function("group.delete", [gname, True, True])
                self.skipTest("Failed to create group")

            ginfo = self.run_function("group.info", [gname])

            # And create the user with that gid
            if self.run_function("user.add", [uname, uid, ginfo["gid"]]) is False:
                # Skip because creating is not what we're testing here
                self.run_function("user.delete", [uname, True, True])
                self.skipTest("Failed to create user")

            uinfo = self.run_function("user.info", [uname])
            self.assertIn(gname, uinfo["groups"])

        except AssertionError:
            self.run_function("user.delete", [uname, True, True])
            raise
