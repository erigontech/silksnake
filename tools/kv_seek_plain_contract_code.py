#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The kv_seek_plain_contract_code command allows to query the KV 'Plain Code Hash' table."""

import argparse

import context # pylint: disable=unused-import

from silksnake.helpers.dbutils import composite_keys, tables
from silksnake.core.constants import ADDRESS_SIZE
from silksnake.remote import kv_metadata
from silksnake.remote import kv_utils
from silksnake.remote.kv_remote import DEFAULT_TARGET

def kv_seek_plain_contract_code(account_address: str, incarnation: int, target: str = DEFAULT_TARGET):
    """ Search for the provided account address in KV 'Plain State' table running at target.
    """
    account_address_bytes = kv_metadata.encode_account_address(account_address)
    plain_code_key = composite_keys.create_storage_prefix(account_address_bytes, incarnation)

    print('REQ plain_code_key:', plain_code_key.hex())
    key, value = kv_utils.kv_seek(tables.PLAIN_CONTRACT_CODE_LABEL, plain_code_key, target)
    assert key[:ADDRESS_SIZE] == plain_code_key[:ADDRESS_SIZE], 'ERR code key {} does not match!'.format(key.hex())
    if key != plain_code_key:
        print('WARN required incarnation does NOT exist, value is from {} '.format(key[ADDRESS_SIZE:].hex()))
    print('RSP code_hash value:', value.hex())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('account_address', help='the account address as hex string (w or w/o 0x prefix)')
    parser.add_argument('-i', '--incarnation', default='0', help='the contract incarnation as positive integer')
    parser.add_argument('-t', '--target', default='localhost:9090', help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_seek_plain_contract_code(args.account_address, int(args.incarnation), args.target)
