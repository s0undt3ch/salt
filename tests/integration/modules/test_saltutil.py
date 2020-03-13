# -*- coding: utf-8 -*-
'''
Integration tests for the saltutil module.
'''

# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals
import os
import time
import textwrap

# Import Salt Testing libs
from tests.support.runtests import RUNTIME_VARS
from tests.support.case import ModuleCase
from tests.support.unit import skipIf

# Import Salt Libs
import salt.utils.files
import salt.utils.stringutils

import pytest


@pytest.mark.windows_whitelisted
class SaltUtilModuleTest(ModuleCase):
    '''
    Testcase for the saltutil execution module
    '''

    def setUp(self):
        self.run_function('saltutil.refresh_pillar')

    # Tests for the wheel function

    def test_wheel_just_function(self):
        '''
        Tests using the saltutil.wheel function when passing only a function.
        '''
        # Wait for the pillar refresh to kick in, so that grains are ready to go
        time.sleep(3)
        ret = self.run_function('saltutil.wheel', ['minions.connected'])
        assert 'minion' in ret['return']
        assert 'sub_minion' in ret['return']

    def test_wheel_with_arg(self):
        '''
        Tests using the saltutil.wheel function when passing a function and an arg.
        '''
        ret = self.run_function('saltutil.wheel', ['key.list', 'minion'])
        assert ret['return'] == {}

    @pytest.mark.skip('Test needs to be rewritten')
    def test_wheel_no_arg_raise_error(self):
        '''
        Tests using the saltutil.wheel function when passing a function that requires
        an arg, but one isn't supplied.
        '''
        with pytest.raises(TypeError):
            self.run_function('saltutil.wheel', ['key.list'])

    def test_wheel_with_kwarg(self):
        '''
        Tests using the saltutil.wheel function when passing a function and a kwarg.
        This function just generates a key pair, but doesn't do anything with it. We
        just need this for testing purposes.
        '''
        ret = self.run_function('saltutil.wheel', ['key.gen'], keysize=1024)
        assert 'pub' in ret['return']
        assert 'priv' in ret['return']


@pytest.mark.windows_whitelisted
class SyncGrainsTest(ModuleCase):
    def test_sync_grains(self):
        ret = self.run_function('saltutil.sync_grains')
        assert ret == []


@pytest.mark.windows_whitelisted
class SaltUtilSyncModuleTest(ModuleCase):
    '''
    Testcase for the saltutil sync execution module
    '''

    def setUp(self):
        whitelist = {'modules': [], }
        self.run_function('saltutil.sync_all', extmod_whitelist=whitelist)

    def tearDown(self):
        self.run_function('saltutil.sync_all')

    def test_sync_all(self):
        '''
        Test syncing all ModuleCase
        '''
        expected_return = {'engines': [],
                           'clouds': [],
                           'grains': [],
                           'beacons': [],
                           'utils': [],
                           'returners': [],
                           'modules': [
                                'modules.depends_versioned',
                                'modules.depends_versionless',
                                'modules.mantest',
                                'modules.override_test',
                                'modules.runtests_decorators',
                                'modules.runtests_helpers',
                                'modules.salttest'],
                           'renderers': [],
                           'log_handlers': [],
                           'matchers': [],
                           'states': [],
                           'sdb': [],
                           'proxymodules': [],
                           'executors': [],
                           'output': [],
                           'thorium': [],
                           'serializers': []}
        ret = self.run_function('saltutil.sync_all')
        assert ret == expected_return

    def test_sync_all_whitelist(self):
        '''
        Test syncing all ModuleCase with whitelist
        '''
        expected_return = {'engines': [],
                           'clouds': [],
                           'grains': [],
                           'beacons': [],
                           'utils': [],
                           'returners': [],
                           'modules': ['modules.salttest'],
                           'renderers': [],
                           'log_handlers': [],
                           'matchers': [],
                           'states': [],
                           'sdb': [],
                           'proxymodules': [],
                           'executors': [],
                           'output': [],
                           'thorium': [],
                           'serializers': []}
        ret = self.run_function('saltutil.sync_all', extmod_whitelist={'modules': ['salttest']})
        assert ret == expected_return

    def test_sync_all_blacklist(self):
        '''
        Test syncing all ModuleCase with blacklist
        '''
        expected_return = {'engines': [],
                           'clouds': [],
                           'grains': [],
                           'beacons': [],
                           'utils': [],
                           'returners': [],
                           'modules': ['modules.mantest',
                                       'modules.override_test',
                                       'modules.runtests_helpers',
                                       'modules.salttest'],
                           'renderers': [],
                           'log_handlers': [],
                           'matchers': [],
                           'states': [],
                           'sdb': [],
                           'proxymodules': [],
                           'executors': [],
                           'output': [],
                           'thorium': [],
                           'serializers': []}
        ret = self.run_function('saltutil.sync_all', extmod_blacklist={'modules': ['runtests_decorators', 'depends_versioned', 'depends_versionless']})
        assert ret == expected_return

    def test_sync_all_blacklist_and_whitelist(self):
        '''
        Test syncing all ModuleCase with whitelist and blacklist
        '''
        expected_return = {'engines': [],
                           'clouds': [],
                           'grains': [],
                           'beacons': [],
                           'utils': [],
                           'returners': [],
                           'executors': [],
                           'modules': [],
                           'renderers': [],
                           'log_handlers': [],
                           'matchers': [],
                           'states': [],
                           'sdb': [],
                           'proxymodules': [],
                           'output': [],
                           'thorium': [],
                           'serializers': []}
        ret = self.run_function('saltutil.sync_all', extmod_whitelist={'modules': ['runtests_decorators']},
                                extmod_blacklist={'modules': ['runtests_decorators']})
        assert ret == expected_return


@skipIf(True, 'Pillar refresh test is flaky. Skipping for now.')
@pytest.mark.windows_whitelisted
class SaltUtilSyncPillarTest(ModuleCase):
    '''
    Testcase for the saltutil sync pillar module
    '''

    @pytest.mark.flaky(max_runs=4)
    def test_pillar_refresh(self):
        '''
        test pillar refresh module
        '''
        pillar_key = 'itworked'

        pre_pillar = self.run_function('pillar.raw')
        assert pillar_key not in pre_pillar.get(pillar_key, 'didnotwork')

        with salt.utils.files.fopen(os.path.join(RUNTIME_VARS.TMP_PILLAR_TREE, 'add_pillar.sls'), 'w') as fp:
            fp.write(salt.utils.stringutils.to_str(
                '{0}: itworked'.format(pillar_key)
            ))

        with salt.utils.files.fopen(os.path.join(RUNTIME_VARS.TMP_PILLAR_TREE, 'top.sls'), 'w') as fp:
            fp.write(textwrap.dedent('''\
                     base:
                       '*':
                         - add_pillar
                     '''))

        self.run_function('saltutil.refresh_pillar')

        pillar = False
        timeout = time.time() + 30
        while not pillar:
            post_pillar = self.run_function('pillar.raw')
            try:
                assert pillar_key in post_pillar.get(pillar_key, 'didnotwork')
                pillar = True
            except AssertionError:
                if time.time() > timeout:
                    assert pillar_key in post_pillar.get(pillar_key, 'didnotwork')
                continue

        post_pillar = self.run_function('pillar.raw')
        assert pillar_key in post_pillar.get(pillar_key, 'didnotwork')

    def tearDown(self):
        for filename in os.listdir(RUNTIME_VARS.TMP_PILLAR_TREE):
            os.remove(os.path.join(RUNTIME_VARS.TMP_PILLAR_TREE, filename))
