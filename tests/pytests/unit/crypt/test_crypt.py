"""
tests.pytests.unit.test_crypt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unit tests for salt's crypt module
"""

import os
import uuid

import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import salt.crypt
import salt.master
import salt.utils.files
from tests.support.mock import MagicMock, MockCall, mock_open, patch

PRIV_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAoAsMPt+4kuIG6vKyw9r3+OuZrVBee/2vDdVetW+Js5dTlgrJ
aghWWn3doGmKlEjqh7E4UTa+t2Jd6w8RSLnyHNJ/HpVhMG0M07MF6FMfILtDrrt8
ZX7eDVt8sx5gCEpYI+XG8Y07Ga9i3Hiczt+fu6HYwu96HggmG2pqkOrn3iGfqBvV
YVFJzSZYe7e4c1PeEs0xYcrA4k+apyGsMtpef8vRUrNicRLc7dAcvfhtgt2DXEZ2
d72t/CR4ygtUvPXzisaTPW0G7OWAheCloqvTIIPQIjR8htFxGTz02STVXfnhnJ0Z
k8KhqKF2v1SQvIYxsZU7jaDgl5i3zpeh58cYOwIDAQABAoIBABZUJEO7Y91+UnfC
H6XKrZEZkcnH7j6/UIaOD9YhdyVKxhsnax1zh1S9vceNIgv5NltzIsfV6vrb6v2K
Dx/F7Z0O0zR5o+MlO8ZncjoNKskex10gBEWG00Uqz/WPlddiQ/TSMJTv3uCBAzp+
S2Zjdb4wYPUlgzSgb2ygxrhsRahMcSMG9PoX6klxMXFKMD1JxiY8QfAHahPzQXy9
F7COZ0fCVo6BE+MqNuQ8tZeIxu8mOULQCCkLFwXmkz1FpfK/kNRmhIyhxwvCS+z4
JuErW3uXfE64RLERiLp1bSxlDdpvRO2R41HAoNELTsKXJOEt4JANRHm/CeyA5wsh
NpscufUCgYEAxhgPfcMDy2v3nL6KtkgYjdcOyRvsAF50QRbEa8ldO+87IoMDD/Oe
osFERJ5hhyyEO78QnaLVegnykiw5DWEF02RKMhD/4XU+1UYVhY0wJjKQIBadsufB
2dnaKjvwzUhPh5BrBqNHl/FXwNCRDiYqXa79eWCPC9OFbZcUWWq70s8CgYEAztOI
61zRfmXJ7f70GgYbHg+GA7IrsAcsGRITsFR82Ho0lqdFFCxz7oK8QfL6bwMCGKyk
nzk+twh6hhj5UNp18KN8wktlo02zTgzgemHwaLa2cd6xKgmAyuPiTgcgnzt5LVNG
FOjIWkLwSlpkDTl7ZzY2QSy7t+mq5d750fpIrtUCgYBWXZUbcpPL88WgDB7z/Bjg
dlvW6JqLSqMK4b8/cyp4AARbNp12LfQC55o5BIhm48y/M70tzRmfvIiKnEc/gwaE
NJx4mZrGFFURrR2i/Xx5mt/lbZbRsmN89JM+iKWjCpzJ8PgIi9Wh9DIbOZOUhKVB
9RJEAgo70LvCnPTdS0CaVwKBgDJW3BllAvw/rBFIH4OB/vGnF5gosmdqp3oGo1Ik
jipmPAx6895AH4tquIVYrUl9svHsezjhxvjnkGK5C115foEuWXw0u60uiTiy+6Pt
2IS0C93VNMulenpnUrppE7CN2iWFAiaura0CY9fE/lsVpYpucHAWgi32Kok+ZxGL
WEttAoGAN9Ehsz4LeQxEj3x8wVeEMHF6OsznpwYsI2oVh6VxpS4AjgKYqeLVcnNi
TlZFsuQcqgod8OgzA91tdB+Rp86NygmWD5WzeKXpCOg9uA+y/YL+0sgZZHsuvbK6
PllUgXdYxqClk/hdBFB7v9AQoaj7K9Ga22v32msftYDQRJ94xOI=
-----END RSA PRIVATE KEY-----
"""


PUB_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoAsMPt+4kuIG6vKyw9r3
+OuZrVBee/2vDdVetW+Js5dTlgrJaghWWn3doGmKlEjqh7E4UTa+t2Jd6w8RSLny
HNJ/HpVhMG0M07MF6FMfILtDrrt8ZX7eDVt8sx5gCEpYI+XG8Y07Ga9i3Hiczt+f
u6HYwu96HggmG2pqkOrn3iGfqBvVYVFJzSZYe7e4c1PeEs0xYcrA4k+apyGsMtpe
f8vRUrNicRLc7dAcvfhtgt2DXEZ2d72t/CR4ygtUvPXzisaTPW0G7OWAheCloqvT
IIPQIjR8htFxGTz02STVXfnhnJ0Zk8KhqKF2v1SQvIYxsZU7jaDgl5i3zpeh58cY
OwIDAQAB
-----END PUBLIC KEY-----
"""

PRIV_KEY2 = """
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAp+8cTxguO6Vg+YO92VfHgNld3Zy8aM3JbZvpJcjTnis+YFJ7
Zlkcc647yPRRwY9nYBNywahnt5kIeuT1rTvTsMBZWvmUoEVUj1Xg8XXQkBvb9Ozy
Gqy/G/p8KDDpzMP/U+XCnUeHiXTZrgnqgBIc2cKeCVvWFqDi0GRFGzyaXLaX3PPm
M7DJ0MIPL1qgmcDq6+7Ze0gJ9SrDYFAeLmbuT1OqDfufXWQl/82JXeiwU2cOpqWq
7n5fvPOWim7l1tzQ+dSiMRRm0xa6uNexCJww3oJSwvMbAmgzvOhqqhlqv+K7u0u7
FrFFojESsL36Gq4GBrISnvu2tk7u4GGNTYYQbQIDAQABAoIBAADrqWDQnd5DVZEA
lR+WINiWuHJAy/KaIC7K4kAMBgbxrz2ZbiY9Ok/zBk5fcnxIZDVtXd1sZicmPlro
GuWodIxdPZAnWpZ3UtOXUayZK/vCP1YsH1agmEqXuKsCu6Fc+K8VzReOHxLUkmXn
FYM+tixGahXcjEOi/aNNTWitEB6OemRM1UeLJFzRcfyXiqzHpHCIZwBpTUAsmzcG
QiVDkMTKubwo/m+PVXburX2CGibUydctgbrYIc7EJvyx/cpRiPZXo1PhHQWdu4Y1
SOaC66WLsP/wqvtHo58JQ6EN/gjSsbAgGGVkZ1xMo66nR+pLpR27coS7o03xCks6
DY/0mukCgYEAuLIGgBnqoh7YsOBLd/Bc1UTfDMxJhNseo+hZemtkSXz2Jn51322F
Zw/FVN4ArXgluH+XsOhvG/MFFpojwZSrb0Qq5b1MRdo9qycq8lGqNtlN1WHqosDQ
zW29kpL0tlRrSDpww3wRESsN9rH5XIrJ1b3ZXuO7asR+KBVQMy/+NcUCgYEA6MSC
c+fywltKPgmPl5j0DPoDe5SXE/6JQy7w/vVGrGfWGf/zEJmhzS2R+CcfTTEqaT0T
Yw8+XbFgKAqsxwtE9MUXLTVLI3sSUyE4g7blCYscOqhZ8ItCUKDXWkSpt++rG0Um
1+cEJP/0oCazG6MWqvBC4NpQ1nzh46QpjWqMwokCgYAKDLXJ1p8rvx3vUeUJW6zR
dfPlEGCXuAyMwqHLxXgpf4EtSwhC5gSyPOtx2LqUtcrnpRmt6JfTH4ARYMW9TMef
QEhNQ+WYj213mKP/l235mg1gJPnNbUxvQR9lkFV8bk+AGJ32JRQQqRUTbU+yN2MQ
HEptnVqfTp3GtJIultfwOQKBgG+RyYmu8wBP650izg33BXu21raEeYne5oIqXN+I
R5DZ0JjzwtkBGroTDrVoYyuH1nFNEh7YLqeQHqvyufBKKYo9cid8NQDTu+vWr5UK
tGvHnwdKrJmM1oN5JOAiq0r7+QMAOWchVy449VNSWWV03aeftB685iR5BXkstbIQ
EVopAoGAfcGBTAhmceK/4Q83H/FXBWy0PAa1kZGg/q8+Z0KY76AqyxOVl0/CU/rB
3tO3sKhaMTHPME/MiQjQQGoaK1JgPY6JHYvly2KomrJ8QTugqNGyMzdVJkXAK2AM
GAwC8ivAkHf8CHrHa1W7l8t2IqBjW1aRt7mOW92nfG88Hck0Mbo=
-----END RSA PRIVATE KEY-----
"""


PUB_KEY2 = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAp+8cTxguO6Vg+YO92VfH
gNld3Zy8aM3JbZvpJcjTnis+YFJ7Zlkcc647yPRRwY9nYBNywahnt5kIeuT1rTvT
sMBZWvmUoEVUj1Xg8XXQkBvb9OzyGqy/G/p8KDDpzMP/U+XCnUeHiXTZrgnqgBIc
2cKeCVvWFqDi0GRFGzyaXLaX3PPmM7DJ0MIPL1qgmcDq6+7Ze0gJ9SrDYFAeLmbu
T1OqDfufXWQl/82JXeiwU2cOpqWq7n5fvPOWim7l1tzQ+dSiMRRm0xa6uNexCJww
3oJSwvMbAmgzvOhqqhlqv+K7u0u7FrFFojESsL36Gq4GBrISnvu2tk7u4GGNTYYQ
bQIDAQAB
-----END PUBLIC KEY-----
"""


def test_get_rsa_pub_key_bad_key(tmp_path):
    """
    get_rsa_pub_key raises InvalidKeyError when encoutering a bad key
    """
    key_path = str(tmp_path / "key")
    with salt.utils.files.fopen(key_path, "w") as fp:
        fp.write("")
    with pytest.raises(salt.crypt.InvalidKeyError):
        salt.crypt.get_rsa_pub_key(key_path)


def test_cryptical_dumps_no_nonce():
    master_crypt = salt.crypt.Crypticle({}, salt.crypt.Crypticle.generate_key_string())
    data = {"foo": "bar"}
    ret = master_crypt.dumps(data)

    # Validate message structure
    assert isinstance(ret, bytes)
    une = master_crypt.decrypt(ret)
    une.startswith(master_crypt.PICKLE_PAD)
    assert salt.payload.loads(une[len(master_crypt.PICKLE_PAD) :]) == data

    # Validate load back to orig data
    assert master_crypt.loads(ret) == data


def test_cryptical_dumps_valid_nonce():
    nonce = uuid.uuid4().hex
    master_crypt = salt.crypt.Crypticle({}, salt.crypt.Crypticle.generate_key_string())
    data = {"foo": "bar"}
    ret = master_crypt.dumps(data, nonce=nonce)

    assert isinstance(ret, bytes)
    une = master_crypt.decrypt(ret)
    une.startswith(master_crypt.PICKLE_PAD)
    nonce_and_data = une[len(master_crypt.PICKLE_PAD) :]
    assert nonce_and_data.startswith(nonce.encode())
    assert salt.payload.loads(nonce_and_data[len(nonce) :]) == data

    assert master_crypt.loads(ret, nonce=nonce) == data


def test_cryptical_dumps_invalid_nonce():
    nonce = uuid.uuid4().hex
    master_crypt = salt.crypt.Crypticle({}, salt.crypt.Crypticle.generate_key_string())
    data = {"foo": "bar"}
    ret = master_crypt.dumps(data, nonce=nonce)
    assert isinstance(ret, bytes)
    with pytest.raises(salt.crypt.SaltClientError, match="Nonce verification error"):
        assert master_crypt.loads(ret, nonce="abcde")


def test_verify_signature(tmp_path):
    tmp_path.joinpath("foo.pem").write_text(PRIV_KEY.strip())
    tmp_path.joinpath("foo.pub").write_text(PUB_KEY.strip())
    tmp_path.joinpath("bar.pem").write_text(PRIV_KEY2.strip())
    tmp_path.joinpath("bar.pub").write_text(PUB_KEY2.strip())
    msg = b"foo bar"
    sig = salt.crypt.sign_message(str(tmp_path.joinpath("foo.pem")), msg)
    assert salt.crypt.verify_signature(str(tmp_path.joinpath("foo.pub")), msg, sig)


def test_verify_signature_bad_sig(tmp_path):
    tmp_path.joinpath("foo.pem").write_text(PRIV_KEY.strip())
    tmp_path.joinpath("foo.pub").write_text(PUB_KEY.strip())
    tmp_path.joinpath("bar.pem").write_text(PRIV_KEY2.strip())
    tmp_path.joinpath("bar.pub").write_text(PUB_KEY2.strip())
    msg = b"foo bar"
    sig = salt.crypt.sign_message(str(tmp_path.joinpath("foo.pem")), msg)
    assert not salt.crypt.verify_signature(str(tmp_path.joinpath("bar.pub")), msg, sig)


def test_pwdata_decrypt():
    key_string = """\
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAzhBRyyHa7b63RLE71uKMKgrpulcAJjaIaN68ltXcCvy4w9pi
Kj+4I3Qp6RvUaHOEmymqyjOMjQc6iwpe0scCFqh3nUk5YYaLZ3WAW0htQVlnesgB
ZiBg9PBeTQY/LzqtudL6RCng/AX+fbnCsddlIysRxnUoNVMvz0gAmCY2mnTDjcTt
pyxuk2T0AHSHNCKCalm75L1bWDFF+UzFemf536tBfBUGRWR6jWTij85vvCntxHS/
HdknaTJ50E7XGVzwBJpCyV4Y2VXuW/3KrCNTqXw+jTmEw0vlcshfDg/vb3IxsUSK
5KuHalKq/nUIc+F4QCJOl+A10goGdIfYC1/67QIDAQABAoIBAAOP+qoFWtCTZH22
hq9PWVb8u0+yY1lFxhPyDdaZueUiu1r/coUCdv996Z+TEJgBr0AzdzVpsLtbbaKr
ujnwoNOdc/vvISPTfKN8P4zUcrcXgZd4z7VhR+vUH/0652q8m/ZDdHorMy2IOP8Z
cAk9DQ2PmA4TRm+tkX0G5KO8vWLsK921aRMWdsKJyQ0lYxl7M8JWupFsCJFr/U+8
dAVtwnUiS7RnhBABZ1cfNTHYhXVAh4d+a9y/gZ00a66OGqPxiXfhjjDUZ6fGvWKN
FlhKWEg6YqIx/H4aNXkLI5Rzzhdx/c2ukNm7+X2veRcAW7bcTwk8wxJxciEP5pBi
1el9VE0CgYEA/lbzdE2M4yRBvTfYYC6BqZcn+BqtrAUc2h3fEy+p7lwlet0af1id
gWpYpOJyLc0AUfR616/m2y3PwEH/nMKDSTuU7o/qKNtlHW0nQcnhDCjTUydS3+J/
JM3dhfgVqi03rjqNcgHA2eOEwcu/OBZtiaC0wqKbuRZRtfGffyoO3ssCgYEAz2iw
wqu/NkA+MdQIxz/a3Is7gGwoFu6h7O+XU2uN8Y2++jSBw9AzzWj31YCvyjuJPAE+
gxHm6yOnNoLVn423NtibHejhabzHNIK6UImH99bSTKabsxfF2BX6v982BimU1jwc
bYykzws37oN/poPb5FTpEiAUrsd2bAMn/1S43icCgYEAulHkY0z0aumCpyUkA8HO
BvjOtPiGRcAxFLBRXPLL3+vtIQachLHcIJRRf+jLkDXfiCo7W4pm6iWzTbqLkMEG
AD3/qowPFAM1Hct6uL01efzmYsIp+g0o60NMhvnolRQu+Bm4yM30AyqjdHzYBjSX
5fyuru8EeSCal1j8aOHcpuUCgYEAhGhDH6Pg59NPYSQJjpm3MMA59hwV473n5Yh2
xKyO6zwgRT6r8MPDrkhqnwQONT6Yt5PbwnT1Q/t4zhXsJnWkFwFk1U1MSeJYEa+7
HZsPECs2CfT6xPRSO0ac00y+AmUdPT8WruDwfbSdukh8f2MCR9vlBsswKPvxH7dM
G3aMplUCgYEAmMFgB/6Ox4OsQPPC6g4G+Ezytkc4iVkMEcjiVWzEsYATITjq3weO
/XDGBYJoBhYwWPi9oBufFc/2pNtWy1FKKXPuVyXQATdA0mfEPbtsHjMFQNZbeKnm
0na/SysSDCK3P+9ijlbjqLjMmPEmhJxGWTJ7khnTTkfre7/w9ZxJxi8=
-----END RSA PRIVATE KEY-----"""
    pwdata = b"""\
V\x80+b\xca\x06M\xb6\x12\xc6\xe8\xf2\xb5\xbb\xd8m\xc0\x97\x9a\xeb\xb9q\x19\xc3\
\xcdi\xb84\x90\xaf\x12kT\xe2@u\xd6\xe8T\x89\xa3\xc7\xb2Y\xd1N\x00\xa9\xc0"\xbe\
\xed\xb1\xc3\xb7^\xbf\xbd\x8b\x13\xd3/L\x1b\xa1`\xe2\xea\x03\x98\x82\xf3uS&|\
\xe5\xd8J\xce\xfc\x97\x8d\x0b\x949\xc0\xbd^\xef\xc6\xfd\xce\xbb\x1e\xd0"(m\xe1\
\x95\xfb\xc8/\x07\x93\xb8\xda\x8f\x99\xfe\xdc\xd5\xcb\xdb\xb2\xf11M\xdbD\xcf\
\x95\x13p\r\xa4\x1c{\xd5\xdb\xc7\xe5\xaf\x95F\x97\xa9\x00p~\xb5\xec\xa4.\xd0\
\xa4\xb4\xf4f\xcds,Y/\xa1:WF\xb8\xc7\x07\xaa\x0b<\'~\x1b$D9\xd4\x8d\xf0x\xc5\
\xee\xa8:\xe6\x00\x10\xc5i\x11\xc7]C8\x05l\x8b\x9b\xc3\x83e\xf7y\xadi:0\xb4R\
\x1a(\x04&yL8\x19s\n\x11\x81\xfd?\xfb2\x80Ll\xa1\xdc\xc9\xb6P\xca\x8d\'\x11\xc1\
\x07\xa5\xa1\x058\xc7\xce\xbeb\x92\xbf\x0bL\xec\xdf\xc3M\x83\xfb$\xec\xd5\xf9\
"""
    assert salt.crypt.pwdata_decrypt(key_string, pwdata) == "1234"


@pytest.mark.slow_test
def test_gen_keys():
    open_priv_wb = MockCall("/keydir{}keyname.pem".format(os.sep), "wb+")
    open_pub_wb = MockCall("/keydir{}keyname.pub".format(os.sep), "wb+")

    with patch.multiple(
        os,
        umask=MagicMock(),
        chmod=MagicMock(),
        access=MagicMock(return_value=True),
    ):
        with patch("salt.utils.files.fopen", mock_open()) as m_open, patch(
            "os.path.isfile", return_value=True
        ):
            result = salt.crypt.gen_keys("/keydir", "keyname", 2048)
            assert result == "/keydir{}keyname.pem".format(os.sep), result
            assert open_priv_wb not in m_open.calls
            assert open_pub_wb not in m_open.calls

        with patch("salt.utils.files.fopen", mock_open()) as m_open, patch(
            "os.path.isfile", return_value=False
        ):
            salt.crypt.gen_keys("/keydir", "keyname", 2048)
            assert open_priv_wb in m_open.calls
            assert open_pub_wb in m_open.calls


@pytest.mark.slow_test
def test_gen_keys_with_passphrase():
    key_path = os.path.join(os.sep, "keydir")
    open_priv_wb = MockCall(os.path.join(key_path, "keyname.pem"), "wb+")
    open_pub_wb = MockCall(os.path.join(key_path, "keyname.pub"), "wb+")

    with patch("os.umask", MagicMock()), patch("os.chmod", MagicMock()), patch(
        "os.chown", MagicMock(), create=True
    ), patch("os.access", MagicMock(return_value=True)):
        with patch("salt.utils.files.fopen", mock_open()) as m_open, patch(
            "os.path.isfile", return_value=True
        ):
            assert salt.crypt.gen_keys(
                key_path, "keyname", 2048, passphrase="password"
            ) == os.path.join(key_path, "keyname.pem")
            result = salt.crypt.gen_keys(
                key_path, "keyname", 2048, passphrase="password"
            )
            assert result == os.path.join(key_path, "keyname.pem"), result
            assert open_priv_wb not in m_open.calls
            assert open_pub_wb not in m_open.calls

        with patch("salt.utils.files.fopen", mock_open()) as m_open, patch(
            "os.path.isfile", return_value=False
        ):
            salt.crypt.gen_keys(key_path, "keyname", 2048)
            assert open_priv_wb in m_open.calls
            assert open_pub_wb in m_open.calls


def test_sign_message(key_data):
    key = serialization.load_pem_private_key(
        key_data.privkey_data, None, default_backend()
    )
    with patch("salt.crypt.get_rsa_key", return_value=key):
        sig = salt.crypt.sign_message("/keydir/keyname.pem", key_data.msg)
        assert sig == key_data.sig


def test_sign_message_with_passphrase(key_data):
    key = serialization.load_pem_private_key(
        key_data.privkey_data, None, default_backend()
    )
    with patch("salt.crypt.get_rsa_key", return_value=key):
        sig = salt.crypt.sign_message(
            "/keydir/keyname.pem", key_data.msg, passphrase="password"
        )
        assert sig == key_data.sig


def test_encrypt_decrypt_bin(key_data):
    priv_key = serialization.load_pem_private_key(
        key_data.privkey_data, None, default_backend()
    )
    pub_key = serialization.load_pem_public_key(key_data.pubkey_data)
    encrypted = salt.crypt.private_encrypt(priv_key, b"salt")
    decrypted = salt.crypt.public_decrypt(pub_key, encrypted)
    assert b"salt" == decrypted


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


def test_m2_bad_key(bad_key_path):
    """
    Load public key with an invalid header using m2crypto and validate it
    """
    key = salt.crypt.get_rsa_pub_key(bad_key_path)
    assert key.check_key() == 1


def test_crypto_bad_key(bad_key_path):
    """
    Load public key with an invalid header and validate it without m2crypto
    """
    key = salt.crypt.get_rsa_pub_key(bad_key_path)
    assert key.can_encrypt()
