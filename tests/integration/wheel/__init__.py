# coding: utf-8

# Import Python libs
import os

# Import Salt Testing libs
import integration

# Import Salt libs
import salt.auth
import salt.wheel


class WheelModuleTest(integration.TestCase, integration.AdaptedConfigurationTestCaseMixIn):
    def setUp(self):
        '''
        Configure an eauth user to test with
        '''
        self.wheel = salt.wheel.Wheel(self.get_config('client_config'))

    def test_master_call(self):
        '''
        Test executing master_call with lowdata

        The choice of using key.list_all for this is arbitrary and should be
        changed to some mocked function that is more testing friendly.
        '''
        self.wheel.master_call(**{
            'client': 'wheel',
            'fun': 'key.list_all',
            'eauth': 'auto',
            'username': 'saltdev_auto',
            'password': 'saltdev',
        })

    def test_token(self):
        '''
        Test executing master_call with lowdata

        The choice of using key.list_all for this is arbitrary and should be
        changed to some mocked function that is more testing friendly.
        '''
        auth = salt.auth.LoadAuth(self.get_config('client_config'))
        token = auth.mk_token({
            'username': 'saltdev_auto',
            'password': 'saltdev',
            'eauth': 'auto',
        })

        self.wheel.master_call(**{
            'client': 'wheel',
            'fun': 'key.list_all',
            'token': token['token'],
        })

    def test_wildcard_auth(self):
        low = {
            'username': 'the_s0und_of_t3ch',
            'password': 'willrockyou',
            'eauth': 'auto',
            'fun': 'key.list_all',
        }

        self.wheel.cmd_sync(low)


if __name__ == '__main__':
    from integration import run_tests
    run_tests(WheelModuleTest, needs_daemon=True)
