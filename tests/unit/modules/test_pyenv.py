# -*- coding: utf-8 -*-
'''
    :codeauthor: Jayesh Kariya <jayeshk@saltstack.com>
'''

# Import Python Libs
from __future__ import absolute_import, unicode_literals, print_function

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import TestCase
from tests.support.mock import (
    MagicMock,
    patch,
)

# Import Salt Libs
import salt.modules.pyenv as pyenv


class PyenvTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test cases for salt.modules.pyenv
    '''
    def setup_loader_modules(self):
        return {pyenv: {}}

    # 'install' function tests: 1

    def test_install(self):
        '''
        Test if it install pyenv systemwide
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_ret = MagicMock(return_value=0)
        with patch.dict(pyenv.__salt__, {'config.option': mock_opt,
                                         'cmd.retcode': mock_ret}):
            assert pyenv.install()

    # 'update' function tests: 1

    def test_update(self):
        '''
        Test if it updates the current versions of pyenv and python-Build
        '''
        mock_opt = MagicMock(return_value='salt stack')
        with patch.dict(pyenv.__salt__, {'config.option': mock_opt}):
            assert not pyenv.update()

    # 'is_installed' function tests: 1

    def test_is_installed(self):
        '''
        Test if it check if pyenv is installed.
        '''
        mock_cmd = MagicMock(return_value=True)
        mock_opt = MagicMock(return_value='salt stack')
        with patch.dict(pyenv.__salt__, {'config.option': mock_opt,
                                         'cmd.has_exec': mock_cmd}):
            assert pyenv.is_installed()

    # 'install_python' function tests: 1

    def test_install_python(self):
        '''
        Test if it install a python implementation.
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_cmd = MagicMock(return_value=True)
        mock_all = MagicMock(return_value={'retcode': 0, 'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__grains__, {'os': 'Linux'}):
            mock_all = MagicMock(return_value={'retcode': 0, 'stdout': 'salt',
                                               'stderr': 'error'})
            with patch.dict(pyenv.__salt__, {'config.option': mock_opt,
                                             'cmd.has_exec': mock_cmd,
                                             'cmd.run_all': mock_all}):
                assert pyenv.install_python('2.0.0-p0') == 'error'

            mock_all = MagicMock(return_value={'retcode': True,
                                               'stdout': 'salt',
                                               'stderr': 'error'})
            with patch.dict(pyenv.__salt__, {'config.option': mock_opt,
                                             'cmd.has_exec': mock_cmd,
                                             'cmd.run_all': mock_all}):
                assert not pyenv.install_python('2.0.0-p0')

    # 'uninstall_python' function tests: 1

    def test_uninstall_python(self):
        '''
        Test if it uninstall a python implementation.
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_cmd = MagicMock(return_value=True)
        mock_all = MagicMock(return_value={'retcode': True,
                                           'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__salt__, {'cmd.has_exec': mock_cmd,
                                         'config.option': mock_opt,
                                         'cmd.run_all': mock_all}):
            assert pyenv.uninstall_python('2.0.0-p0')

    # 'versions' function tests: 1

    def test_versions(self):
        '''
        Test if it list the installed versions of python.
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_cmd = MagicMock(return_value=True)
        mock_all = MagicMock(return_value={'retcode': True,
                                           'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__salt__, {'cmd.has_exec': mock_cmd,
                                         'config.option': mock_opt,
                                         'cmd.run_all': mock_all}):
            assert pyenv.versions() == []

    # 'default' function tests: 1

    def test_default(self):
        '''
        Test if it returns or sets the currently defined default python.
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_cmd = MagicMock(return_value=True)
        mock_all = MagicMock(return_value={'retcode': True,
                                           'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__salt__, {'cmd.has_exec': mock_cmd,
                                         'config.option': mock_opt,
                                         'cmd.run_all': mock_all}):
            assert pyenv.default() == ''
            assert pyenv.default('2.0.0-p0')

    # 'list_' function tests: 1

    def test_list(self):
        '''
        Test if it list the installable versions of python.
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_cmd = MagicMock(return_value=True)
        mock_all = MagicMock(return_value={'retcode': True,
                                           'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__salt__, {'cmd.has_exec': mock_cmd,
                                         'config.option': mock_opt,
                                         'cmd.run_all': mock_all}):
            assert pyenv.list_() == []

    # 'rehash' function tests: 1

    def test_rehash(self):
        '''
        Test if it run pyenv rehash to update the installed shims.
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_cmd = MagicMock(return_value=True)
        mock_all = MagicMock(return_value={'retcode': True,
                                           'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__salt__, {'cmd.has_exec': mock_cmd,
                                         'config.option': mock_opt,
                                         'cmd.run_all': mock_all}):
            assert pyenv.rehash()

    # 'do' function tests: 1

    def test_do(self):
        '''
        Test if it execute a python command with pyenv's
        shims from the user or the system.
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_cmd = MagicMock(return_value=True)
        mock_all = MagicMock(return_value={'retcode': True, 'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__salt__, {'cmd.has_exec': mock_cmd,
                                         'config.option': mock_opt,
                                         'cmd.run_all': mock_all}):
            assert not pyenv.do('gem list bundler')

        mock_all = MagicMock(return_value={'retcode': 0, 'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__salt__, {'config.option': mock_opt,
                                         'cmd.has_exec': mock_cmd,
                                         'cmd.run_all': mock_all}):
            assert pyenv.do('gem list bundler') == 'salt'

    # 'do_with_python' function tests: 1

    def test_do_with_python(self):
        '''
        Test if it execute a python command with pyenv's
        shims using a specific python version.
        '''
        mock_opt = MagicMock(return_value='salt stack')
        mock_cmd = MagicMock(return_value=True)
        mock_all = MagicMock(return_value={'retcode': True, 'stdout': 'salt',
                                           'stderr': 'error'})
        with patch.dict(pyenv.__salt__, {'cmd.has_exec': mock_cmd,
                                         'config.option': mock_opt,
                                         'cmd.run_all': mock_all}):
            assert not pyenv.do_with_python('2.0.0-p0',
                                                  'gem list bundler')
