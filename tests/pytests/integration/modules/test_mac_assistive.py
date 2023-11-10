"""
    :codeauthor: Nicole Thomas <nicole@saltstack.com>
"""

import pytest

pytestmark = [
    pytest.mark.destructive_test,
    pytest.mark.skip_if_not_root,
    pytest.mark.skip_initial_gh_actions_failure,
    pytest.mark.skip_unless_on_darwin,
]


@pytest.fixture(scope="function")
def osa_script():
    yield "/usr/bin/osascript"


@pytest.fixture(scope="function")
def setup_teardown_vars(salt_call_cli, osa_script):
    salt_call_cli.run("assistive.install", osa_script, True)
    try:
        yield
    finally:
        ret = salt_call_cli.run("assistive.installed", osa_script)
        osa_script_ret = ret.data
        if osa_script_ret:
            salt_call_cli.run("assistive.remove", osa_script)

        smile_bundle = "com.smileonmymac.textexpander"
        ret = salt_call_cli.run("assistive.installed", smile_bundle)
        smile_bundle_present = ret.data
        if smile_bundle_present:
            salt_call_cli.run("assistive.remove", smile_bundle)


@pytest.mark.slow_test
def test_install_and_remove(salt_call_cli, osa_script, setup_teardown_vars):
    """
    Tests installing and removing a bundled ID or command to use assistive access.
    """
    new_bundle = "com.smileonmymac.textexpander"
    assert salt_call_cli.run("assistive.install", new_bundle)
    assert salt_call_cli.run("assistive.remove", new_bundle)


@pytest.mark.slow_test
def test_installed(salt_call_cli, osa_script, setup_teardown_vars):
    """
    Tests the True and False return of assistive.installed.
    """
    # OSA script should have been installed in setUp function
    ret = salt_call_cli.run("assistive.installed", osa_script)
    assert ret.data
    # Clean up install
    salt_call_cli.run("assistive.remove", osa_script)
    # Installed should now return False
    ret = salt_call_cli.run("assistive.installed", osa_script)
    assert not ret.data


@pytest.mark.slow_test
def test_enable(salt_call_cli, osa_script, setup_teardown_vars):
    """
    Tests setting the enabled status of a bundled ID or command.
    """
    # OSA script should have been installed and enabled in setUp function
    # Now let's disable it, which should return True.
    ret = salt_call_cli.run("assistive.enable", osa_script, False)
    assert ret.data
    # Double check the script was disabled, as intended.
    ret = salt_call_cli.run("assistive.enabled", osa_script)
    assert not ret.data
    # Now re-enable
    ret = salt_call_cli.run("assistive.enable", osa_script)
    assert ret.data
    # Double check the script was enabled, as intended.
    ret = salt_call_cli.run("assistive.enabled", osa_script)
    assert ret.data


@pytest.mark.slow_test
def test_enabled(salt_call_cli, osa_script, setup_teardown_vars):
    """
    Tests if a bundled ID or command is listed in assistive access returns True.
    """
    # OSA script should have been installed in setUp function, which sets
    # enabled to True by default.
    ret = salt_call_cli.run("assistive.enabled", osa_script)
    assert ret.data
    # Disable OSA Script
    salt_call_cli.run("assistive.enable", osa_script, False)
    # Assert against new disabled status
    ret = salt_call_cli.run("assistive.enabled", osa_script)
    assert not ret.data
