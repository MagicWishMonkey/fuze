import os
import sys
import hmac
import hashlib
from operator import xor
from itertools import izip, starmap
from struct import Struct

class Clipboard:
    def __init__(self):
        def macSetClipboard(text):
            outf = os.popen('pbcopy', 'w')
            outf.write(text)
            outf.close()

        def macGetClipboard():
            outf = os.popen('pbpaste', 'r')
            content = outf.read()
            outf.close()
            return content

        self.getter = macGetClipboard
        self.setter = macSetClipboard

    @staticmethod
    def read():
        return Clipboard().getter()

    @staticmethod
    def write(o):
        return Clipboard().setter(o)



class PasswordGenerator:
    """
    A PBKDF2 password hashing algorithm borrowed from
    https://github.com/mitsuhiko/python-pbkdf2.

    """
    __KEYLEN__ = 24
    __ITERATIONS__ = 1000
    __HASH_FUNC__ = hashlib.sha512
    __PACK_INT__ = Struct('>I').pack

    @staticmethod
    def generate(input, salt, iterations=None, keylen=None, hash_func=None):
        assert isinstance(input, basestring), "The input parameter is not a valid string!"
        assert isinstance(salt, basestring), "The input parameter is not a valid string!"

        if iterations is None:
            iterations = PasswordGenerator.__ITERATIONS__
        if keylen is None:
            keylen = PasswordGenerator.__KEYLEN__
        if hash_func is None:
            hash_func = PasswordGenerator.__HASH_FUNC__

        mac = hmac.new(input, None, hash_func)
        def _pseudorandom(x, mac=mac):
            h = mac.copy()
            h.update(x)
            return map(ord, h.digest())
        buf = []
        for block in xrange(1, -(-keylen // mac.digest_size) + 1):
            rv = u = _pseudorandom(salt + PasswordGenerator.__PACK_INT__(block))
            for i in xrange(iterations - 1):
                u = _pseudorandom(''.join(map(chr, u)))
                rv = starmap(xor, izip(rv, u))
            buf.extend(rv)
        txt = ''.join(map(chr, buf))[:keylen]
        return txt.encode('hex')

input = "{query}"
if input is None or len(input) == 0:
    input = Clipboard.read()

output = PasswordGenerator.generate(input, hashlib.md5(input).hexdigest())
Clipboard.write(output)
sys.stdout.write(output)