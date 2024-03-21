"""
    :codeauthor: Eric Vz <eric@base10.org>
"""

import pytest

import salt.modules.pacmanpkg as pacman
from tests.support.mock import MagicMock, patch
import salt.utils.systemd


@pytest.fixture
def configure_loader_modules():
    return {
        pacman: {},
    }


def test_list_pkgs():
    """
    Test if it list the packages currently installed in a dict
    """
    cmdmock = MagicMock(return_value="A 1.0\nB 2.0")
    sortmock = MagicMock()
    stringifymock = MagicMock()
    mock_ret = {"A": ["1.0"], "B": ["2.0"]}
    with patch.dict(
        pacman.__salt__,
        {
            "cmd.run": cmdmock,
            "pkg_resource.add_pkg": lambda pkgs, name, version: pkgs.setdefault(
                name, []
            ).append(version),
            "pkg_resource.sort_pkglist": sortmock,
            "pkg_resource.stringify": stringifymock,
        },
    ):
        assert pacman.list_pkgs() == mock_ret

    sortmock.assert_called_with(mock_ret)
    stringifymock.assert_called_with(mock_ret)


def test_list_pkgs_as_list():
    """
    Test if it lists the packages currently installed in a dict
    """
    cmdmock = MagicMock(return_value="A 1.0\nB 2.0")
    sortmock = MagicMock()
    stringifymock = MagicMock()
    mock_ret = {"A": ["1.0"], "B": ["2.0"]}
    with patch.dict(
        pacman.__salt__,
        {
            "cmd.run": cmdmock,
            "pkg_resource.add_pkg": lambda pkgs, name, version: pkgs.setdefault(
                name, []
            ).append(version),
            "pkg_resource.sort_pkglist": sortmock,
            "pkg_resource.stringify": stringifymock,
        },
    ):
        assert pacman.list_pkgs(True) == mock_ret

    sortmock.assert_called_with(mock_ret)
    assert stringifymock.call_count == 0


def test_pacman_install_sysupgrade_flag():
    """
    Test if the pacman.install function appends the '-u' flag only when sysupgrade is True
    """
    mock_parse_targets = MagicMock(return_value=({"somepkg": None}, "repository"))
    mock_has_scope = MagicMock(return_value=False)
    mock_list_pkgs = MagicMock(return_value={"somepkg": "1.0"})
    mock_run_all = MagicMock(return_value={"retcode": 0, "stderr": ""})

    with patch.dict(
        pacman.__salt__,
        {
            "cmd.run_all": mock_run_all,
            "pkg_resource.parse_targets": mock_parse_targets,
            "config.get": MagicMock(return_value=True),
        },
    ), patch.object(salt.utils.systemd, "has_scope", mock_has_scope), patch.object(
        pacman, "list_pkgs", mock_list_pkgs
    ):
        pacman.install(name="somepkg", sysupgrade=True)
        args, _ = pacman.__salt__["cmd.run_all"].call_args
        assert "-u" in args[0]

        pacman.install(name="somepkg", sysupgrade=None, refresh=True)
        args, _ = pacman.__salt__["cmd.run_all"].call_args
        assert "-u" not in args[0]
