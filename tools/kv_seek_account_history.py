#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The kv_seek_account_history command allows to query the KV 'History of Accounts' table."""

import argparse

import context # pylint: disable=unused-import

from silksnake.remote import kv_metadata
from silksnake.remote import kv_utils
from silksnake.remote.kv_metadata import INVALID_BLOCK_NUMBER
from silksnake.remote.kv_remote import DEFAULT_TARGET

def kv_seek_account_history(account_address: str, block_number: int, target: str = DEFAULT_TARGET):
    """ Search for the provided account address in KV 'History of Accounts' table.
    """
    account_history_key = kv_metadata.encode_account_history_key(account_address, block_number)

    print('REQ1 account_address:', account_address, '(key: ' + str(account_history_key.hex()) + ')')

    print('RSP1 history: [')
    walker = lambda key, value: print('key:', key.hex(), 'value:', value.hex())
    kv_utils.kv_walk(target, kv_metadata.ACCOUNTS_HISTORY_LABEL, account_history_key, walker)
    print(']')

    print('REQ2 account_address:', account_address, '(key: ' + str(account_history_key.hex()) + ')')

    print('RSP2 history: [')
    walker = lambda key, value: print('key:', key.hex(), 'value:', value.hex())
    kv_utils.kv_walk(target, kv_metadata.STORAGE_HISTORY_LABEL, account_history_key, walker)
    print(']')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('account_address', help='the account address as hex string (w or w/o 0x prefix)')
    parser.add_argument('-b', '--block_number', default=INVALID_BLOCK_NUMBER, help='the block number as integer')
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_seek_account_history(args.account_address, int(args.block_number), args.target)
