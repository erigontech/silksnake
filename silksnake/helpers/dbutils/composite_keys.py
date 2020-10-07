# -*- coding: utf-8 -*-
"""The utility functions for database composite keys."""

from silksnake.core.constants import HASH_SIZE

def create_storage_prefix(address_bytes: bytes, incarnation: int) -> bytes:
    """ create_storage_prefix """
    incarnation_bytes = int.to_bytes(incarnation, 8, 'big')
    return address_bytes + incarnation_bytes

def create_composite_storage_key(address_hash: bytes, incarnation: int, location_hash: bytes) -> bytes:
    """ create_composite_storage_key """
    if len(address_hash) != HASH_SIZE:
        raise ValueError('wrong address_hash size, expected {0} got {1} bytes'.format(HASH_SIZE, len(address_hash)))
    return create_storage_prefix(address_hash, incarnation) + location_hash

def create_plain_composite_storage_key(address_bytes: bytes, incarnation: int, location_hash: bytes) -> bytes:
    """ create_composite_storage_key """
    return create_storage_prefix(address_bytes, incarnation) + location_hash
