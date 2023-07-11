import pytest

import salt.crypt
from tests.support.mock import mock_open, patch

try:
    import M2Crypto  # pylint: disable=unused-import

    HAS_M2 = True
except ImportError:
    HAS_M2 = False
try:
    from Cryptodome.PublicKey import RSA

    HAS_PYCRYPTO_RSA = True
except ImportError:
    HAS_PYCRYPTO_RSA = False
if not HAS_PYCRYPTO_RSA:
    try:
        from Crypto.PublicKey import RSA  # nosec

        HAS_PYCRYPTO_RSA = True
    except ImportError:
        HAS_PYCRYPTO_RSA = False


@pytest.mark.skipif(not HAS_PYCRYPTO_RSA, reason="pycrypto >= 2.6 is not available")
@pytest.mark.skipif(HAS_M2, reason="m2crypto is used by salt.crypt if installed")
def test_verify_signature(key_data):
    with patch("salt.utils.files.fopen", mock_open(read_data=key_data.pubkey_data)):
        assert salt.crypt.verify_signature(
            "/keydir/keyname.pub", key_data.msg, key_data.sig
        )
