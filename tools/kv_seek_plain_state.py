#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The kv_seek_plain_state command allows to query the turbo-geth/silkworm KV 'Plain State' bucket."""

import argparse

import context # pylint: disable=unused-import

from silksnake.core.remote import kv_metadata
from silksnake.core.remote import kv_utils
from silksnake.core.remote.kv_utils import DEFAULT_TARGET
from silksnake.core.storage import account

def kv_seek_plain_state(account_address: str, storage_location: str = '0x0', target: str = DEFAULT_TARGET):
    """ Search for the provided account address in KV 'Plain State' bucket of turbo-geth/silkworm running at target.
    """
    account_address_bytes = kv_metadata.encode_account_address(account_address)

    print('REQ1 account_address:', account_address)
    key, value = kv_utils.kv_seek(kv_metadata.PLAIN_STATE_LABEL, account_address_bytes, target)
    assert key == account_address_bytes, 'ERR account address {} does not match!'.format(key.hex())
    stored_account = account.Account.from_bytes(value)
    print('RSP1 account:', stored_account)

    incarnation_bytes = kv_metadata.encode_incarnation(stored_account.incarnation)
    storage_location_bytes = kv_metadata.encode_storage_location(storage_location)
    storage_key = account_address_bytes + incarnation_bytes + storage_location_bytes

    print('REQ2 storage_location:', storage_location)
    key, value = kv_utils.kv_seek(kv_metadata.PLAIN_STATE_LABEL, storage_key, target)
    assert key == storage_key, 'ERR storage key {} does not match!'.format(key.hex())
    print('RSP2 storage value:', value.hex())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('account_address', help='the account address as hex string (w or w/o 0x prefix)')
    parser.add_argument('-l', '--location', default='0x0', help='the storage location as hex string (w or w/o 0x prefix)')
    parser.add_argument('-t', '--target', default='localhost:9090', help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_seek_plain_state(args.account_address, args.location, args.target)
