import pytest
import salt.loader
from tests.support.pytest.helpers import FakeSaltExtension


@pytest.fixture(scope="module", autouse=True)
def salt_extension(tmp_path_factory):
    with FakeSaltExtension(tmp_path_factory=tmp_path_factory, name="saltextloadertest"):
        yield


def test_new_entry_points(salt_minion_factory):
    loader = salt.loader.minion_mods(salt_minion_factory.config)

    # A non existing module should not appear in the loader
    assert "monty.python" not in loader

    # But our extension's modules should appear on the loader
    assert "foobar.echo1" in loader
    assert "foobar.echo2" in loader


def test_old_entry_points(salt_minion_factory):
    loader = salt.loader.runner(salt_minion_factory.config)

    # A non existing runner module should not appear in the loader
    assert "monty.python" not in loader

    # But our extension's runner modules should appear on the loader
    assert "foobar.echo1" in loader
    assert "foobar.echo2" in loader
