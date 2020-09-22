#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_block_number command allows to query the turbo-geth/silkworm KV 'Header Numbers' bucket."""

import argparse

import context # pylint: disable=unused-import

from silksnake.core.rlp import sedes
from silksnake.core.remote import kv_metadata
from silksnake.core.remote import kv_utils
from silksnake.core.remote.kv_utils import DEFAULT_TARGET

def kv_seek_block_number(block_hash: str, target: str = DEFAULT_TARGET):
    """ Search for the provided block hash in KV 'Header Numbers' bucket of turbo-geth/silkworm running at target.
    """
    block_hash = block_hash[2:] if block_hash.startswith('0x') else block_hash

    print('REQ block_hash:', block_hash)

    key, value = kv_utils.kv_seek(kv_metadata.BLOCK_HEADER_NUMBERS_LABEL, bytes.fromhex(block_hash), target)

    assert key.hex() == block_hash, 'ERR block hash {} does not match!'.format(key.hex())
    block_number = sedes.decode_block_number(value)

    print('RSP block_number:', block_number, '(' + str(value.hex()) + ')')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('block_hash', help='the block hash as hex string (w or w/o 0x prefix)')
    parser.add_argument('-t', '--target', default='localhost:9090', help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_seek_block_number(args.block_hash, args.target)
