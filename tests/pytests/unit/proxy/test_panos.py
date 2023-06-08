import pytest

import salt.proxy.panos as panos
from tests.support.mock import MagicMock, call, patch


@pytest.fixture
def configure_loader_modules():
    with patch.dict(panos.DETAILS):
        yield {panos: {"__pillar__": {}}}


@pytest.fixture
def opts():
    return {"proxy": {"proxytype": "panos", "host": "hosturl.com", "apikey": "api_key"}}


@pytest.mark.parametrize("verify", [True, False, None])
def test_init(opts, verify):
    opts["proxy"]["verify_ssl"] = verify
    if verify is None:
        opts["proxy"].pop("verify_ssl")
        verify = True
    mock_http = MagicMock(
        return_value={"status": 200, "text": "<data>some_test_data</data>"}
    )
    with patch("salt.utils.http.query", mock_http):
        panos.init(opts)
    assert mock_http.call_args_list == [
        call(
            "https://hosturl.com/api/",
            data={
                "type": "op",
                "cmd": "<show><system><info></info></system></show>",
                "key": "api_key",
            },
            decode=True,
            decode_type="plain",
            method="POST",
            raise_error=True,
            status=True,
            verify_ssl=verify,
        )
    ]
