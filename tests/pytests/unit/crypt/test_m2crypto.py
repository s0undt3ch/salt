import os

import pytest

import salt.crypt
from tests.support.mock import MagicMock, mock_open, patch

try:
    import M2Crypto

    HAS_M2 = True
except ImportError:
    HAS_M2 = False


@pytest.mark.skipif(not HAS_M2, reason="m2crypto is not available")
@patch("os.umask", MagicMock())
@patch("os.chmod", MagicMock())
@patch("os.access", MagicMock(return_value=True))
@pytest.mark.slow_test
def test_gen_keys():
    with patch("M2Crypto.RSA.RSA.save_pem", MagicMock()) as save_pem:
        with patch("M2Crypto.RSA.RSA.save_pub_key", MagicMock()) as save_pub:
            with patch("os.path.isfile", return_value=True):
                assert salt.crypt.gen_keys(
                    "/keydir", "keyname", 2048
                ) == "/keydir{}keyname.pem".format(os.sep)
                save_pem.assert_not_called()
                save_pub.assert_not_called()

            with patch("os.path.isfile", return_value=False):
                assert salt.crypt.gen_keys(
                    "/keydir", "keyname", 2048
                ) == "/keydir{}keyname.pem".format(os.sep)
                save_pem.assert_called_once_with(
                    "/keydir{}keyname.pem".format(os.sep), cipher=None
                )
                save_pub.assert_called_once_with("/keydir{}keyname.pub".format(os.sep))


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


@pytest.mark.skipif(not HAS_M2, reason="m2crypto is not available")
def test_encrypt_decrypt_bin(key_data):
    priv_key = M2Crypto.RSA.load_key_string(
        salt.utils.stringutils.to_bytes(key_data.privkey_data)
    )
    pub_key = M2Crypto.RSA.load_pub_key_bio(
        M2Crypto.BIO.MemoryBuffer(salt.utils.stringutils.to_bytes(key_data.pubkey_data))
    )
    encrypted = salt.crypt.private_encrypt(priv_key, b"salt")
    decrypted = salt.crypt.public_decrypt(pub_key, encrypted)
    assert b"salt" == decrypted


@pytest.mark.skipif(not HAS_M2, reason="Skip when m2crypto is not installed")
def test_m2crypto_verify_bytes(key_data):
    message = salt.utils.stringutils.to_unicode("meh")
    with patch(
        "salt.utils.files.fopen",
        mock_open(read_data=salt.utils.stringutils.to_bytes(key_data.pubkey_data)),
    ):
        salt.crypt.verify_signature("/keydir/keyname.pub", message, key_data.signature)


@pytest.mark.skipif(not HAS_M2, reason="Skip when m2crypto is not installed")
def test_m2crypto_verify_unicode(key_data):
    message = salt.utils.stringutils.to_bytes("meh")
    with patch(
        "salt.utils.files.fopen",
        mock_open(read_data=salt.utils.stringutils.to_bytes(key_data.pubkey_data)),
    ):
        salt.crypt.verify_signature("/keydir/keyname.pub", message, key_data.signature)


@pytest.mark.skipif(not HAS_M2, reason="Skip when m2crypto is not installed")
def test_m2crypto_sign_bytes(key_data):
    message = salt.utils.stringutils.to_unicode("meh")
    key = M2Crypto.RSA.load_key_string(
        salt.utils.stringutils.to_bytes(key_data.privkey_data)
    )
    with patch("salt.crypt.get_rsa_key", return_value=key):
        signature = salt.crypt.sign_message(
            "/keydir/keyname.pem", message, passphrase="password"
        )
    assert signature == key_data.signature


@pytest.mark.skipif(not HAS_M2, reason="Skip when m2crypto is not installed")
def test_m2crypto_sign_unicode(key_data):
    message = salt.utils.stringutils.to_bytes("meh")
    key = M2Crypto.RSA.load_key_string(
        salt.utils.stringutils.to_bytes(key_data.privkey_data)
    )
    with patch("salt.crypt.get_rsa_key", return_value=key):
        signature = salt.crypt.sign_message(
            "/keydir/keyname.pem", message, passphrase="password"
        )
    assert signature == key_data.signature


@pytest.fixture
def bad_key_path(tmp_path):
    key_path = tmp_path / "cryptodom-3.4.6.pub"
    key_path.write_bytes(
        b"-----BEGIN RSA PUBLIC KEY-----\n"
        b"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzLtFhsvfbFDFaUgulSEX\n"
        b"Gl12XriL1DT78Ef2/u8HHaSMmPie37BLWas/zaHwI6066bIyYQJ/nUCahTaoHM7L\n"
        b"GlWc0wOU6zyfpihCRQHil05Y6F+olFBoZuYbFPvtp7/hJx/D7I/0n2o/c7M5i3Y2\n"
        b"3sBxAYNooIQHXHUmPQW6C9iu95ylZDW8JQzYy/EI4vCC8yQMdTK8jK1FQV0Sbwny\n"
        b"qcMxSyAWDoFbnhh2P2TnO8HOWuUOaXR8ZHOJzVcDl+a6ew+medW090x3K5O1f80D\n"
        b"+WjgnG6b2HG7VQpOCfM2GALD/FrxicPilvZ38X1aLhJuwjmVE4LAAv8DVNJXohaO\n"
        b"WQIDAQAB\n"
        b"-----END RSA PUBLIC KEY-----\n"
    )
    return key_path


@pytest.mark.skipif(not HAS_M2, reason="Skip when m2crypto is not installed")
def test_m2_bad_key(bad_key_path):
    """
    Load public key with an invalid header using m2crypto and validate it
    """
    key = salt.crypt.get_rsa_pub_key(bad_key_path)
    assert key.check_key() == 1


@pytest.mark.skipif(HAS_M2, reason="Skip when m2crypto is installed")
def test_crypto_bad_key(bad_key_path):
    """
    Load public key with an invalid header and validate it without m2crypto
    """
    key = salt.crypt.get_rsa_pub_key(bad_key_path)
    assert key.can_encrypt()
