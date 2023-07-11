import attr
import pytest


@attr.s(frozen=True, slots=True)
class KeyData:
    msg = b"It's me, Mario"
    privkey_data = (
        b"-----BEGIN RSA PRIVATE KEY-----\n"
        b"MIIEpAIBAAKCAQEA75GR6ZTv5JOv90Vq8tKhKC7YQnhDIo2hM0HVziTEk5R4UQBW\n"
        b"a0CKytFMbTONY2msEDwX9iA0x7F5Lgj0X8eD4ZMsYqLzqjWMekLC8bjhxc+EuPo9\n"
        b"Dygu3mJ2VgRC7XhlFpmdo5NN8J2E7B/CNB3R4hOcMMZNZdi0xLtFoTfwU61UPfFX\n"
        b"14mV2laqLbvDEfQLJhUTDeFFV8EN5Z4H1ttLP3sMXJvc3EvM0JiDVj4l1TWFUHHz\n"
        b"eFgCA1Im0lv8i7PFrgW7nyMfK9uDSsUmIp7k6ai4tVzwkTmV5PsriP1ju88Lo3MB\n"
        b"4/sUmDv/JmlZ9YyzTO3Po8Uz3Aeq9HJWyBWHAQIDAQABAoIBAGOzBzBYZUWRGOgl\n"
        b"IY8QjTT12dY/ymC05GM6gMobjxuD7FZ5d32HDLu/QrknfS3kKlFPUQGDAbQhbbb0\n"
        b"zw6VL5NO9mfOPO2W/3FaG1sRgBQcerWonoSSSn8OJwVBHMFLG3a+U1Zh1UvPoiPK\n"
        b"S734swIM+zFpNYivGPvOm/muF/waFf8tF/47t1cwt/JGXYQnkG/P7z0vp47Irpsb\n"
        b"Yjw7vPe4BnbY6SppSxscW3KoV7GtJLFKIxAXbxsuJMF/rYe3O3w2VKJ1Sug1VDJl\n"
        b"/GytwAkSUer84WwP2b07Wn4c5pCnmLslMgXCLkENgi1NnJMhYVOnckxGDZk54hqP\n"
        b"9RbLnkkCgYEA/yKuWEvgdzYRYkqpzB0l9ka7Y00CV4Dha9Of6GjQi9i4VCJ/UFVr\n"
        b"UlhTo5y0ZzpcDAPcoZf5CFZsD90a/BpQ3YTtdln2MMCL/Kr3QFmetkmDrt+3wYnX\n"
        b"sKESfsa2nZdOATRpl1antpwyD4RzsAeOPwBiACj4fkq5iZJBSI0bxrMCgYEA8GFi\n"
        b"qAjgKh81/Uai6KWTOW2kX02LEMVRrnZLQ9VPPLGid4KZDDk1/dEfxjjkcyOxX1Ux\n"
        b"Klu4W8ZEdZyzPcJrfk7PdopfGOfrhWzkREK9C40H7ou/1jUecq/STPfSOmxh3Y+D\n"
        b"ifMNO6z4sQAHx8VaHaxVsJ7SGR/spr0pkZL+NXsCgYEA84rIgBKWB1W+TGRXJzdf\n"
        b"yHIGaCjXpm2pQMN3LmP3RrcuZWm0vBt94dHcrR5l+u/zc6iwEDTAjJvqdU4rdyEr\n"
        b"tfkwr7v6TNlQB3WvpWanIPyVzfVSNFX/ZWSsAgZvxYjr9ixw6vzWBXOeOb/Gqu7b\n"
        b"cvpLkjmJ0wxDhbXtyXKhZA8CgYBZyvcQb+hUs732M4mtQBSD0kohc5TsGdlOQ1AQ\n"
        b"McFcmbpnzDghkclyW8jzwdLMk9uxEeDAwuxWE/UEvhlSi6qdzxC+Zifp5NBc0fVe\n"
        b"7lMx2mfJGxj5CnSqQLVdHQHB4zSXkAGB6XHbBd0MOUeuvzDPfs2voVQ4IG3FR0oc\n"
        b"3/znuwKBgQChZGH3McQcxmLA28aUwOVbWssfXKdDCsiJO+PEXXlL0maO3SbnFn+Q\n"
        b"Tyf8oHI5cdP7AbwDSx9bUfRPjg9dKKmATBFr2bn216pjGxK0OjYOCntFTVr0psRB\n"
        b"CrKg52Qrq71/2l4V2NLQZU40Dr1bN9V+Ftd9L0pvpCAEAWpIbLXGDw==\n"
        b"-----END RSA PRIVATE KEY-----"
    )

    pubkey_data = (
        b"-----BEGIN PUBLIC KEY-----\n"
        b"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA75GR6ZTv5JOv90Vq8tKh\n"
        b"KC7YQnhDIo2hM0HVziTEk5R4UQBWa0CKytFMbTONY2msEDwX9iA0x7F5Lgj0X8eD\n"
        b"4ZMsYqLzqjWMekLC8bjhxc+EuPo9Dygu3mJ2VgRC7XhlFpmdo5NN8J2E7B/CNB3R\n"
        b"4hOcMMZNZdi0xLtFoTfwU61UPfFX14mV2laqLbvDEfQLJhUTDeFFV8EN5Z4H1ttL\n"
        b"P3sMXJvc3EvM0JiDVj4l1TWFUHHzeFgCA1Im0lv8i7PFrgW7nyMfK9uDSsUmIp7k\n"
        b"6ai4tVzwkTmV5PsriP1ju88Lo3MB4/sUmDv/JmlZ9YyzTO3Po8Uz3Aeq9HJWyBWH\n"
        b"AQIDAQAB\n"
        b"-----END PUBLIC KEY-----"
    )

    sig = (
        b"\x81^E\x12\x01?\\B\x7f\x0b*g\xa3p\xa7\xe4\xde+\xe8z\xa5\xc0\xf2\x92"
        b"\xd8Ny\x0e\xcd\xea\xb76\xd7\xa7\xfb\xfbx7T\x8d\x96\\\xa1\xbdm\xd0C"
        b"\x00\xf4@l\xb5\xf5\x93\x1a\x1fiC\x11\x92t\xed\xee\xaa\xde\xceQ\x96"
        b"\xbc\x9e\xe5\xd9\xcby\x02\xb1\x90\x8d(uV\xfe\x17$\xc6\x1c\x9fk\xc2 "
        b"\x08\xa8\xfd-O\x96&\xad\xddS\xecD\xdb\xd8\xd1W\x81\xe1\xb0\x8a"
        b"\x19n*\x0e\xa6:\xc0\xa0\x1e\xee\xec\xa4Hl\xa0\x92\xcc\xe8\x0c[\x07Un"
        b"\x03,\xedL.\xf86\x13NM\x0f7z\xe2\xd4\x11\xc1\xfa\x8dN|\xa5\x00\x0f"
        b"\xfb\x15wW*\x97d[=Kr\xf2\xe9\x87'\x83\xbb\x03\xdb,\xe72.O\xc8\xf6.\\4"
        b"\x98\xc2\x1dbN\xd8\xcd\xf9\x8b\x8e\x0c\xceMQ2\xeeB\xddd\x1b\xbf}\xfa"
        b"\x0e\x00Jm\xe0C\x9f&\x1e-\xe1\xda@\\\xb6\x04\xefwH\xc32\x8a\xfb\xb5"
        b"\xfd\xcc\xf1\x8a\xafT3W\xb3\xeb\x81\xd4\xd7\xbdMG4\xed\x02P\x9ay\xc7"
    )

    signature = (
        b"w\xac\xfe18o\xeb\xfb\x14+\x9e\xd1\xb7\x7fe}\xec\xd6\xe1P\x9e\xab"
        b"\xb5\x07\xe0\xc1\xfd\xda#\x04Z\x8d\x7f\x0b\x1f}:~\xb2s\x860u\x02N"
        b'\xd4q"\xb7\x86*\x8f\x1f\xd0\x9d\x11\x92\xc5~\xa68\xac>\x12H\xc2%y,'
        b"\xe6\xceU\x1e\xa3?\x0c,\xf0u\xbb\xd0[g_\xdd\x8b\xb0\x95:Y\x18\xa5*"
        b"\x99\xfd\xf3K\x92\x92 ({\xd1\xff\xd9F\xc8\xd6K\x86e\xf9\xa8\xad\xb0z"
        b"\xe3\x9dD\xf5k\x8b_<\xe7\xe7\xec\xf3\"'\xd5\xd2M\xb4\xce\x1a\xe3$"
        b"\x9c\x81\xad\xf9\x11\xf6\xf5>)\xc7\xdd\x03&\xf7\x86@ks\xa6\x05\xc2"
        b"\xd0\xbd\x1a7\xfc\xde\xe6\xb0\xad!\x12#\xc86Y\xea\xc5\xe3\xe2\xb3"
        b"\xc9\xaf\xfa\x0c\xf2?\xbf\x93w\x18\x9e\x0b\xa2a\x10:M\x05\x89\xe2W.Q"
        b"\xe8;yGT\xb1\xf2\xc6A\xd2\xc4\xbeN\xb3\xcfS\xaf\x03f\xe2\xb4)\xe7\xf6"
        b'\xdbs\xd0Z}8\xa4\xd2\x1fW*\xe6\x1c"\x8b\xd0\x18w\xb9\x7f\x9e\x96\xa3'
        b"\xd9v\xf7\x833\x8e\x01"
    )


@pytest.fixture
def key_data():
    return KeyData()
