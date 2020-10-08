#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_eth_supply command allows to query the custom 'ETH_SUPPLY.v2' table."""

import argparse

import context # pylint: disable=unused-import

from silksnake.rlp import sedes
from silksnake.helpers.dbutils import tables
from silksnake.remote import kv_remote
from silksnake.remote import kv_utils
from silksnake.remote.kv_remote import DEFAULT_TARGET

def kv_seek_eth_supply(kv_view: kv_remote.RemoteView, block_height: int, count: int = 1):
    """ Search for the provided block range in 'ETH_SUPPLY.v2' table of Turbo-Geth/Silkworm running at target.
    """
    for block_number in range(block_height, block_height + count):
        encoded_block_number = sedes.encode_block_number(block_number)
        print('REQ block_number:', block_number, '(key: ' + str(encoded_block_number.hex()) + ')')
        key, value = kv_view.get(tables.ETH_SUPPLY_LABEL, encoded_block_number)
        assert key == encoded_block_number, 'ERR key `{0}` does not match!'.format(key.hex())
        supply = int.from_bytes(value, 'big')
        print('RSP supply:', supply, '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('block_number', help='the block number as integer')
    parser.add_argument('-c', '--count', default=1, help='the number of blocks to seek as integer')
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_utils.kv_func(args.target, kv_seek_eth_supply, int(args.block_number), int(args.count))
