#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The kv_seek_plain_change_sets command allows to query the KV 'Account Changes' and 'Storage Changes' tables."""

import argparse

import context # pylint: disable=unused-import

from silksnake.remote import kv_metadata
from silksnake.remote import kv_remote
from silksnake.remote import kv_utils
from silksnake.remote.kv_remote import DEFAULT_TARGET

def kv_seek_plain_change_sets(kv_view: kv_remote.RemoteView, block_height: int, count: int = 1):
    """ Search for the provided block range in KV 'Account Changes' and 'Storage Changes' tables.
    """
    for index, block_number in enumerate(range(block_height, block_height + count)):
        change_set_key = kv_metadata.encode_timestamp(block_number)

        print('ACCOUNT CHANGES\nREQ1 block_number:', block_number, '(key: ' + str(change_set_key.hex()) + ')')
        key, value = kv_view.get(kv_metadata.PLAIN_ACCOUNTS_CHANGE_SET_LABEL, change_set_key)
        print('RSP1 key:', key.hex(), 'value:', value.hex(), '\n')

        print('STORAGE CHANGES\nREQ2 block_number:', block_number, '(key: ' + str(change_set_key.hex()) + ')')
        key, value = kv_view.get(kv_metadata.PLAIN_STORAGE_CHANGE_SET_LABEL, change_set_key)
        print('RSP2 key:', key.hex(), 'value:', value.hex(), '\n')

        if index != count - 1:
            print('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('block_number', help='the block number as integer')
    parser.add_argument('-c', '--count', default=1, help='the number of blocks to seek as integer')
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_utils.kv_func(args.target, kv_seek_plain_change_sets, int(args.block_number), int(args.count))
