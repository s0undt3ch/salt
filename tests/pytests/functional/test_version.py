import importlib

import pkg_resources  # pylint: disable=3rd-party-module-not-gated

import pytest
import salt.utils.entrypoints
import salt.version
from tests.support.pytest.helpers import FakeSaltExtension


@pytest.fixture
def salt_extension(tmp_path_factory):
    with FakeSaltExtension(
        tmp_path_factory=tmp_path_factory, name="salt-ext-version-test"
    ) as salt_extension:
        importlib.reload(salt.utils.entrypoints)
        if salt.utils.entrypoints.USE_PKG_RESOURCES:
            # We need to reload pkg_resources or our newly installed extension
            # won't be picked up
            importlib.reload(pkg_resources)
        try:
            yield salt_extension
        finally:
            importlib.reload(salt.utils.entrypoints)
            if salt.utils.entrypoints.USE_PKG_RESOURCES:
                # pkg_resources caches, stuff, reload
                importlib.reload(pkg_resources)


def test_salt_extensions_in_versions_report(salt_extension):
    versions_information = salt.version.versions_information()
    assert "Salt Extensions" in versions_information
    assert salt_extension.name in versions_information["Salt Extensions"]


def test_salt_extensions_absent_in_versions_report():
    """
    Ensure that the 'Salt Extensions' header does not show up when no extension is installed
    """
    versions_information = salt.version.versions_information()
    assert "Salt Extensions" not in versions_information
