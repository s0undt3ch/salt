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
    patch)

# Import Salt Libs
import salt.modules.smf_service as smf


class SmfTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test cases for salt.modules.smf
    '''
    def setup_loader_modules(self):
        return {smf: {}}

    def test_get_running(self):
        '''
        Test to return the running services
        '''
        with patch.dict(smf.__salt__, {'cmd.run':
                                       MagicMock(return_value='A online\n')}):
            assert smf.get_running() == ['A']

    def test_get_stopped(self):
        '''
        Test to return the stopped services
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.run': MagicMock(return_value='A\n')}):
            assert smf.get_stopped() == ['A']

    def test_available(self):
        '''
        Test to returns ``True`` if the specified service is available,
        otherwise returns ``False``.
        '''
        with patch.dict(smf.__salt__, {'cmd.run': MagicMock(return_value='A')}):
            with patch.object(smf, 'get_all', return_value=('A')):
                assert smf.available('A')

    def test_missing(self):
        '''
        The inverse of service.available.
        Returns ``True`` if the specified service is not available, otherwise
        returns ``False``.
        '''
        with patch.dict(smf.__salt__, {'cmd.run': MagicMock(return_value='A')}):
            with patch.object(smf, 'get_all', return_value=('A')):
                assert not smf.missing('A')

    def test_get_all(self):
        '''
        Test to return all installed services
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.run': MagicMock(return_value='A\n')}):
            assert smf.get_all() == ['A']

    def test_start(self):
        '''
        Test to start the specified service
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.retcode': MagicMock(side_effect=[False, 3, None,
                                                               False, 4])}):
            assert smf.start('name')

            assert smf.start('name')

            assert not smf.start('name')

    def test_stop(self):
        '''
        Test to stop the specified service
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.retcode': MagicMock(return_value=False)}):
            assert smf.stop('name')

    def test_restart(self):
        '''
        Test to restart the named service
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.retcode': MagicMock(side_effect=[False, True])}):

            with patch.object(smf, 'start', return_value='A'):
                assert smf.restart('name') == 'A'

            assert not smf.restart('name')

    def test_reload_(self):
        '''
        Test to reload the named service
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.retcode': MagicMock(side_effect=[False, True])}):

            with patch.object(smf, 'start', return_value='A'):
                assert smf.reload_('name') == 'A'

            assert not smf.reload_('name')

    def test_status(self):
        '''
        Test to return the status for a service, returns a bool whether the
        service is running.
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.run': MagicMock(side_effect=['online',
                                                           'online1'])}):
            assert smf.status('name')

            assert not smf.status('name')

    def test_enable(self):
        '''
        Test to enable the named service to start at boot
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.retcode': MagicMock(return_value=False)}):
            assert smf.enable('name')

    def test_disable(self):
        '''
        Test to disable the named service to start at boot
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.retcode': MagicMock(return_value=False)}):
            assert smf.disable('name')

    def test_enabled(self):
        '''
        Test to check to see if the named service is enabled to start on boot
        '''
        with patch.dict(smf.__salt__,
                        {'cmd.run': MagicMock(side_effect=['fmri',
                                                           'A B true',
                                                           'fmri',
                                                           'A B false'])}):
            assert smf.enabled('name')

            assert not smf.enabled('name')

    def test_disabled(self):
        '''
        Test to check to see if the named service is disabled to start on boot
        '''
        with patch.object(smf, 'enabled', return_value=False):
            assert smf.disabled('name')

    def test_get_enabled(self):
        '''
        Test to return the enabled services
        '''
        with patch.object(smf, '_get_enabled_disabled', return_value=True):
            assert smf.get_enabled()

    def test_get_disabled(self):
        '''
        Test to return the disabled services
        '''
        with patch.object(smf, '_get_enabled_disabled', return_value=True):
            assert smf.get_disabled()
