# -*- coding: utf-8 -*-
"""The turbo-geth/silkworm database timestamp codec."""

def encode_timestamp(timestamp: int) -> bytes:
    """ Encode the given block number a.k.a. timestamp as suffix bytes.
        This encoding ET has the property: if a < b, then ET(a) < ET(b) lexicographically.
    """
    suffix = bytearray()
    limit = 32

    for bytecount in range(1, 9):
        if timestamp < limit:
            suffix = bytearray(bytecount)
            value = timestamp
            for i in range(bytecount - 1, 0, -1):
                suffix[i] = value & 0xFF
                value >>= 8
            suffix[0] = value | (bytecount << 5) # 3 most significant bits of the first byte are bytecount
            break
        limit <<= 8

    if len(suffix) == 0:
        raise ValueError('timestamp is empty')

    return bytes(suffix)

def decode_timestamp(suffix: bytes) -> (int, bytes):
    """ Decode the given suffix bytes as block number a.k.a. timestamp.
    """
    if len(suffix) == 0:
        raise ValueError('timestamp is empty')

    bytecount = int(suffix[0] >> 5)
    timestamp = int(suffix[0] & 0x1F)
    for i in range(1, bytecount):
        timestamp = (timestamp << 8) | int(suffix[i])

    return timestamp, suffix[bytecount:]
