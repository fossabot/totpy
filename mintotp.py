#!/usr/bin/env python3

import base64
import hmac
import struct
import sys
import time


def hotp(key, counter, digits=6, digest='sha1'):
    key_padded = key.upper() + '=' * ((8 - len(key)) % 8)
    key_decoded = base64.b32decode(key_padded)
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key_decoded, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].zfill(digits)


def totp(key, time_step=30, digits=6, digest='sha1'):
    counter = int(time.time() / time_step)
    return hotp(key, counter, digits, digest)


def main(key=None):
    if not key:
        key = sys.argv[1]
    print(totp(key))


if __name__ == '__main__':
    main()
