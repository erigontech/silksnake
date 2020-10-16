#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_block_body command allows to query the turbo-geth/silkworm KV 'Block Bodies' bucket."""

import argparse

import context # pylint: disable=unused-import

from silksnake.rlp import sedes
from silksnake.helpers.dbutils import tables
from silksnake.remote import kv_utils
from silksnake.remote.kv_remote import DEFAULT_TARGET

def kv_seek_block_body(block_height: int, count: int = 1, target: str = DEFAULT_TARGET):
    """ Search for the provided block range in KV 'Block Bodies' bucket of turbo-geth/silkworm running at target.
    """
    for index, block_number in enumerate(range(block_height, block_height + count)):
        encoded_block_number = sedes.encode_block_number(block_number)

        print('REQ block_number:', block_number, '(key: ' + str(encoded_block_number.hex()) + ')')

        key, value = kv_utils.kv_seek(tables.BLOCK_BODIES_LABEL, encoded_block_number, target)

        decoded_block_number, block_hash = sedes.decode_block_key(key)
        assert decoded_block_number == block_number, 'ERR block number {} does not match!'.format(decoded_block_number)
        block = sedes.decode_block_body(value)

        print('RSP block_hash:', block_hash.hex(), 'transactions(' + str(len(block.transactions)) + '): [')
        for transaction in block.transactions:
            print('tx#' + str(block.transactions.index(transaction)), transaction)
        print('] ommers(' + str(len(block.ommer_block_headers)) + '): [')
        for ommer in block.ommer_block_headers:
            print('ommer#' + str(block.ommer_block_headers.index(ommer)), ommer)
        print(']' if index == count - 1 else ']\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('block_number', help='the block number as integer')
    parser.add_argument('-c', '--count', default=1, help='the number of blocks to seek as integer')
    parser.add_argument('-t', '--target', default='localhost:9090', help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_seek_block_body(int(args.block_number), int(args.count), args.target)
