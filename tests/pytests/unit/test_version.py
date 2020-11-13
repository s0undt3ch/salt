import salt.version
from tests.support.mock import patch


def test_versions_report_includes_salt_extensions():
    with patch(
        "salt.version.extensions_information", return_value={"foo-bar-ext": "1.0"}
    ):
        versions_information = salt.version.versions_information()
        assert "Salt Extensions" in versions_information
        assert "foo-bar-ext" in versions_information["Salt Extensions"]
        assert versions_information["Salt Extensions"]["foo-bar-ext"] == "1.0"


def test_versions_report_no_extensions_available():
    with patch("salt.utils.entrypoints.iter_entry_points", return_value=()):
        versions_information = salt.version.versions_information()
        assert "Salt Extensions" not in versions_information
