#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_plain_state command allows to query the turbo-geth/silkworm KV 'Plain State' bucket."""

import argparse

import context # pylint: disable=unused-import

from silksnake.core import account
from silksnake.helpers import hashing
from silksnake.helpers.dbutils import composite_keys, tables
from silksnake.remote import kv_utils
from silksnake.remote.kv_remote import DEFAULT_TARGET
from silksnake.types.address import Address

def kv_seek_plain_state(account_address: str, storage_location: str = '0x0', target: str = DEFAULT_TARGET):
    """ Search for the provided account address in KV 'Plain State' bucket of turbo-geth/silkworm running at target.
    """
    account_address_bytes = Address.from_hex(account_address).bytes

    print('REQ1 account_address:', account_address)
    key, value = kv_utils.kv_seek(tables.PLAIN_STATE_LABEL, account_address_bytes, target)
    assert key == account_address_bytes, 'ERR account address {} does not match!'.format(key.hex())
    stored_account = account.Account.from_storage(value)
    print('RSP1 account:', stored_account)

    incarnation = stored_account.incarnation
    location_hash = hashing.hex_as_hash(storage_location)
    storage_key = composite_keys.create_plain_composite_storage_key(account_address_bytes, incarnation, location_hash)

    print('REQ2 storage_location:', storage_location)
    incarnation_bytes = composite_keys.encode_incarnation(incarnation)
    key, value = kv_utils.kv_seek(tables.PLAIN_STATE_LABEL, storage_key, target)
    key_prefix_length = len(account_address_bytes) + len(incarnation_bytes)
    key_prefix = key[:key_prefix_length]
    assert key_prefix == storage_key[:key_prefix_length], 'ERR storage key prefix {} does not match!'.format(key_prefix.hex())
    if key != storage_key:
        print('WARN required location does NOT exist, value is from {} '.format(key[key_prefix_length:].hex()))
    print('RSP2 storage value:', value.hex())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('account_address', help='the account address as hex string (w or w/o 0x prefix)')
    parser.add_argument('-l', '--location', default='0x0', help='the storage location as hex string (w or w/o 0x prefix)')
    parser.add_argument('-t', '--target', default='localhost:9090', help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_seek_plain_state(args.account_address, args.location, args.target)
