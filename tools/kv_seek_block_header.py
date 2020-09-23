#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_block_header command allows to query the turbo-geth/silkworm KV 'Headers'."""

import argparse

import context # pylint: disable=unused-import

from silksnake.rlp import sedes
from silksnake.remote import kv_metadata
from silksnake.remote import kv_remote
from silksnake.remote import kv_utils
from silksnake.remote.kv_utils import DEFAULT_TARGET

def kv_seek_block_header(kv_view: kv_remote.RemoteView, block_height: int, count: int = 1):
    """ Search for the provided block range in KV 'Headers' bucket of turbo-geth/silkworm running at target.
    """
    for index, block_number in enumerate(range(block_height, block_height + count)):
        encoded_canonical_block_number = sedes.encode_canonical_block_number(block_number)
        print('CANONICAL HEADER\nREQ1 block_number:', block_number, '(k1: ' + str(encoded_canonical_block_number.hex()) + ')')
        key, block_hash = kv_view.get(kv_metadata.BLOCK_HEADERS_LABEL, encoded_canonical_block_number)
        decoded_block_number = sedes.decode_canonical_block_number(key)
        assert decoded_block_number == block_number, 'ERR block number {} does not match!'.format(decoded_block_number)
        print('RSP1 block_hash:', block_hash.hex(), '\n')

        encoded_block_key = sedes.encode_block_key(block_number, block_hash)
        print('FULL HEADER\nREQ2 block_number:', block_number, '(k2: ' + str(encoded_block_key.hex()) + ')')
        key, value = kv_view.get(kv_metadata.BLOCK_HEADERS_LABEL, encoded_block_key)
        decoded_block_number, decoded_block_hash = sedes.decode_block_key(key)
        block_header = sedes.decode_block_header(value)
        assert decoded_block_number == block_number, 'ERR block number {} does not match!'.format(decoded_block_number)
        assert decoded_block_hash == block_hash, 'ERR2 block hash {} does not match!'.format(decoded_block_hash)
        print('RSP2 block_header:', block_header, '\n')

        encoded_difficulty_block_key = sedes.encode_difficulty_block_key(encoded_block_key)
        print('DIFFICULTY HEADER\nREQ3 block_number:', block_number, '(k3: ' + str(encoded_difficulty_block_key.hex()) + ')')
        key, value = kv_view.get(kv_metadata.BLOCK_HEADERS_LABEL, encoded_difficulty_block_key)
        decoded_block_number, decoded_block_hash = sedes.decode_difficulty_block_key(key)
        block_total_difficulty = sedes.decode_block_total_difficulty(value)
        assert decoded_block_number == block_number, 'ERR block number {} does not match!'.format(decoded_block_number)
        assert decoded_block_hash == block_hash, 'ERR block hash {} does not match!'.format(decoded_block_hash)
        print('RSP3 block_total_difficulty:', block_total_difficulty)

        if index != count - 1:
            print('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('block_number', help='the block number as integer')
    parser.add_argument('-c', '--count', default=1, help='the number of blocks to seek as integer')
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_utils.kv_func(args.target, kv_seek_block_header, int(args.block_number), int(args.count))
