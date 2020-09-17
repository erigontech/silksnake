#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_block_header command allows to query the turbo-geth/silkworm KV 'Headers'."""

import argparse

import context # pylint: disable=unused-import

from silksnake.core.rlp import sedes
from silksnake.core.remote import kv_metadata
from silksnake.core.remote import kv_utils
from silksnake.core.remote.kv_utils import DEFAULT_TARGET

def kv_seek_block_header(block_number: int, target: str = DEFAULT_TARGET):
    """ Search for the provided block_number in KV 'Headers' bucket of turbo-geth/silkworm running at target.
    """
    encoded_block_number = sedes.encode_block_number(block_number)

    print('CANONICAL HEADER\nREQ1 block_number:', block_number, '(' + str(encoded_block_number.hex()) + ')')

    key, value = kv_utils.kv_seek(kv_metadata.BLOCK_HEADERS_LABEL, encoded_block_number, target)

    decoded_block_number = sedes.decode_block_number(key[:8]) # last byte is 0x6e
    block_hash = sedes.decode_block_hash(value)
    assert decoded_block_number == block_number, 'ERR block number does not match!'

    print('RSP1 block_hash:', block_hash.hex(), '\n')

    encoded_block_number_ext = encoded_block_number + b'\x74'

    print('FULL HEADER\nREQ2 block_number:', block_number, '(' + str(encoded_block_number_ext.hex()) + ')')

    key, value = kv_utils.kv_seek(kv_metadata.BLOCK_HEADERS_LABEL, encoded_block_number_ext, target)

    decoded_block_number, block_hash = sedes.decode_block_key(key)
    block_header = sedes.decode_block_header(value)
    assert decoded_block_number == block_number, 'ERR block number does not match!'

    print('RSP2 block_hash:', block_hash.hex(), ' block_header:', block_header)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('block_number', help='the block number as integer')
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_seek_block_header(int(args.block_number), args.target)
