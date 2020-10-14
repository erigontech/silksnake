# -*- coding: utf-8 -*-
"""The data type constants."""

from eth_typing import Hash32

from ..types.address import Address

ADDRESS_SIZE = 20
HASH_SIZE = 32
BLOCK_NUMBER_SIZE = 8
INCARNATION_SIZE = 8
TRIE_ROOT_SIZE = 32
UINT8_SIZE = 8
UINT32_SIZE = 32
UINT256_SIZE = 256

ZERO_ADDRESS = Address(ADDRESS_SIZE * b'\x00').bytes
ZERO_HASH32 = Hash32(32 * b'\x00')
