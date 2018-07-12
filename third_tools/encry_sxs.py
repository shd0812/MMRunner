import base64
import binascii


def sxs_xor(orig, seed):
    dest = []
    rate = len(orig) // len(seed)
    smod = len(orig) % len(seed)#6
    new_seed = seed * rate + seed[0:smod]

    for i, x in enumerate(orig.decode("utf8")):
        o = chr(ord(x) ^ ord(new_seed[i]))
        dest.append(o)
    return "".join(dest)


def encryt_sxs(orig, seed):
    """加密方法：base64，异或，16进制"""
    new_orig=bytes(orig, encoding="utf8")
    bstr = binascii.hexlify(new_orig)
    enstr = sxs_xor(bstr, seed)
    new_enstr=bytes(enstr, encoding="utf8")
    test_enstr = base64.b64encode(new_enstr)
    new_enstr=test_enstr.decode("utf8")
    return new_enstr


def decrypt_sxs(dest, seed):
    """解密方法:base64,异或,16进制"""
    enstr = base64.b64decode(dest)
    bstr = sxs_xor(enstr,seed)
    hex_bstr= binascii.unhexlify(bstr)
    a = str(hex_bstr, 'ascii')
    return a


