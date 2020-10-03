# -*- coding: utf-8 -*-
"""The utility functions for hashing."""

from eth_hash.auto import keccak

from ..core.constants import HASH_SIZE

def bytes_to_hash(data: bytes) -> bytes:
    """ Returns the keccak256 digest of given bytes."""
    return keccak(data)

def hex_to_hash(data: str) -> bytes:
    """ Returns the keccak256 digest of given hex string."""
    data = data[2:] if data.startswith('0x') else data
    return keccak(bytes.fromhex(data))

def hex_as_hash(hex_string: str) -> bytes:
    """ Cast the given hex string as 32-byte hash."""
    hex_string = hex_string[2:] if hex_string.startswith('0x') else hex_string
    hex_string = hex_string.zfill(2*HASH_SIZE)
    return bytes.fromhex(hex_string)[:HASH_SIZE]
