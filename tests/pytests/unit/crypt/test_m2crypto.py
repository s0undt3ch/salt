import os

import pytest

import salt.crypt
from tests.support.mock import MagicMock, mock_open, patch

try:
    import M2Crypto

    HAS_M2 = True
except ImportError:
    HAS_M2 = False


@patch("os.umask", MagicMock())
@patch("os.chmod", MagicMock())
@patch("os.chown", MagicMock())
@patch("os.access", MagicMock(return_value=True))
@pytest.mark.slow_test
@pytest.mark.skipif(not HAS_M2, reason="m2crypto is not available")
def test_gen_keys_with_passphrase():
    with patch("M2Crypto.RSA.RSA.save_pem", MagicMock()) as save_pem:
        with patch("M2Crypto.RSA.RSA.save_pub_key", MagicMock()) as save_pub:
            with patch("os.path.isfile", return_value=True):
                assert salt.crypt.gen_keys(
                    "/keydir", "keyname", 2048, passphrase="password"
                ) == "/keydir{}keyname.pem".format(os.sep)
                save_pem.assert_not_called()
                save_pub.assert_not_called()

            with patch("os.path.isfile", return_value=False):
                assert salt.crypt.gen_keys(
                    "/keydir", "keyname", 2048, passphrase="password"
                ) == "/keydir{}keyname.pem".format(os.sep)
                callback = save_pem.call_args[1]["callback"]
                save_pem.assert_called_once_with(
                    "/keydir{}keyname.pem".format(os.sep),
                    cipher="des_ede3_cbc",
                    callback=callback,
                )
                assert callback(None) == b"password"
                save_pub.assert_called_once_with("/keydir{}keyname.pub".format(os.sep))


@pytest.mark.skipif(not HAS_M2, reason="m2crypto is not available")
def test_sign_message(key_data):
    key = M2Crypto.RSA.load_key_string(
        salt.utils.stringutils.to_bytes(key_data.privkey_data)
    )
    with patch("salt.crypt.get_rsa_key", return_value=key):
        assert (
            salt.crypt.sign_message("/keydir/keyname.pem", key_data.msg) == key_data.sig
        )


@pytest.mark.skipif(not HAS_M2, reason="m2crypto is not available")
def test_sign_message_with_passphrase(key_data):
    key = M2Crypto.RSA.load_key_string(
        salt.utils.stringutils.to_bytes(key_data.privkey_data)
    )
    with patch("salt.crypt.get_rsa_key", return_value=key):
        assert (
            salt.crypt.sign_message(
                "/keydir/keyname.pem", key_data.msg, passphrase="password"
            )
            == key_data.sig
        )


@pytest.mark.skipif(not HAS_M2, reason="m2crypto is not available")
def test_verify_signature(key_data):
    with patch(
        "salt.utils.files.fopen",
        mock_open(read_data=salt.utils.stringutils.to_bytes(key_data.pubkey_data)),
    ):
        assert salt.crypt.verify_signature(
            "/keydir/keyname.pub", key_data.msg, key_data.sig
        )
