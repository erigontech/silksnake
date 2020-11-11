#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The kv_seek_plain_contract_code command allows to query the KV 'Plain Code Hash' table."""

import argparse

import context # pylint: disable=unused-import

from silksnake.helpers.dbutils import composite_keys, tables
from silksnake.core.constants import ADDRESS_SIZE
from silksnake.remote import kv_utils
from silksnake.remote.kv_remote import DEFAULT_TARGET
from silksnake.types.address import Address

def kv_seek_plain_contract_code(account_address: str, incarnation: int, target: str = DEFAULT_TARGET):
    """ Search for the provided account address in KV 'Plain Contract Code' table running at target.
    """
    account_address_bytes = Address.from_hex(account_address).bytes
    plain_code_key = composite_keys.create_storage_prefix(account_address_bytes, incarnation)

    print('REQ1 plain_code_key:', plain_code_key.hex())
    key, code_hash_bytes = kv_utils.kv_seek(tables.PLAIN_CONTRACT_CODE_LABEL, plain_code_key, target)
    assert key[:ADDRESS_SIZE] == plain_code_key[:ADDRESS_SIZE], 'ERR code key {} does not match!'.format(key.hex())
    if key != plain_code_key:
        print('WARN required incarnation does NOT exist, value is from {} '.format(key[ADDRESS_SIZE:].hex()))
    print('RSP1 code_hash value:', code_hash_bytes.hex())

    print('REQ2 code_hash:', code_hash_bytes.hex())
    key, value = kv_utils.kv_seek(tables.CODE_LABEL, code_hash_bytes, target)
    assert key == code_hash_bytes, 'ERR code hash key {} does not match!'.format(key.hex())
    print('RSP2 code value:', value.hex())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('account_address', help='the account address as hex string (w or w/o 0x prefix)')
    parser.add_argument('-i', '--incarnation', default='0', help='the contract incarnation as positive integer')
    parser.add_argument('-t', '--target', default='localhost:9090', help='the server location as string <address>:<port>')
    args = parser.parse_args()

    kv_seek_plain_contract_code(args.account_address, int(args.incarnation), args.target)
