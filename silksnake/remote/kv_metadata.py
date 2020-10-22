# -*- coding: utf-8 -*-
"""The turbo-geth/silkworm KV application protocol metadata."""

from silksnake.core.constants import ADDRESS_SIZE

def encode_account_address(account_address: str) -> bytes:
    """ Encode the given hex account address as 20-byte buffer.
    """
    account_address = account_address[2:] if account_address.startswith('0x') else account_address
    return bytes.fromhex(account_address)

def encode_account_history_key(account_address: str, block_number: int) -> bytes:
    """ Encode the given hex account address and block number as 28-byte BigEndian buffer.
    """
    account_address_bytes = encode_account_address(account_address)
    block_number_bytes = int.to_bytes(block_number, 8, 'big')
    account_history_key = account_address_bytes + block_number_bytes
    return account_history_key

def decode_account_address_list(address_list_bytes: bytes):
    """ Decode the given data bytes as concatenated list of 20-byte addresses.
    """
    num_addresses = len(address_list_bytes) // ADDRESS_SIZE
    account_address_list = []
    for i in range(num_addresses):
        account_address = address_list_bytes[i : i + ADDRESS_SIZE]
        account_address_list.append(account_address)
    return account_address_list
