#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_tx_senders command allows to query the turbo-geth/silkworm KV 'Receipts' bucket."""

import argparse

import context # pylint: disable=unused-import

from silksnake.rlp import sedes
from silksnake.remote import kv_metadata
from silksnake.remote import kv_remote
from silksnake.remote import kv_utils
from silksnake.remote.kv_remote import DEFAULT_TARGET

def kv_seek_tx_senders(kv_view: kv_remote.RemoteView, block_height: int, count: int = 1):
    """ Search for the provided block range in KV 'Receipts' bucket of turbo-geth/silkworm running at target.
    """
    for index, block_number in enumerate(range(block_height, block_height + count)):
        encoded_canonical_block_number = sedes.encode_canonical_block_number(block_number)
        print('CANONICAL HEADER\nREQ1 block_number:', block_number, '(key: ' + str(encoded_canonical_block_number.hex()) + ')')
        key, block_hash = kv_view.get(kv_metadata.BLOCK_HEADERS_LABEL, encoded_canonical_block_number)
        decoded_block_number = sedes.decode_canonical_block_number(key)
        assert decoded_block_number == block_number, 'ERR block number {} does not match!'.format(decoded_block_number)
        print('RSP1 block_hash:', block_hash.hex(), '\n')

        encoded_block_key = sedes.encode_block_key(block_number, block_hash)
        print('TX_SENDERS\nREQ2 block_number:', block_number, '(key: ' + str(encoded_block_key.hex()) + ')')
        key, value = kv_view.get(kv_metadata.TRANSACTION_SENDERS_LABEL, encoded_block_key)
        account_address_list = kv_metadata.decode_account_address_list(value) if key == encoded_block_key else []
        print('RSP2 senders(' + str(len(account_address_list)) + '): [')
        for account_address in account_address_list:
            print('address#' + str(account_address_list.index(account_address)), account_address.hex())
        print(']' if index == count - 1 else ']\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('block_number', help='the block number as integer')
    parser.add_argument('-c', '--count', default=1, help='the number of blocks to seek as integer')
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_utils.kv_func(args.target, kv_seek_tx_senders, int(args.block_number), int(args.count))
