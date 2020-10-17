# -*- coding: utf-8 -*-
"""The unit test for hashing module."""

import pytest

from silksnake.helpers.dbutils import composite_keys

# pylint: disable=line-too-long

@pytest.mark.parametrize("incarnation,result,should_pass", [
    # Valid test list
    (0, '0000000000000000', True),

    # Invalid test list
    (None, '', False),
])
def test_encode_incarnation(incarnation: int, result: str, should_pass: bool):
    """ Unit test for encode_incarnation. """
    result_bytes = bytes.fromhex(result) if result is not None else None
    if should_pass:
        assert composite_keys.encode_incarnation(incarnation) == result_bytes
    else:
        with pytest.raises((TypeError)):
            composite_keys.encode_incarnation(incarnation)

@pytest.mark.parametrize("address,incarnation,prefix,should_pass", [
    # Valid test list
    ('dcc703c0e500b653ca82273b7bfad8045d85a470', 0, 'dcc703c0e500b653ca82273b7bfad8045d85a4700000000000000000', True),

    # Invalid test list
    (None, 0, '', False),
])
def test_create_storage_prefix(address: str, incarnation: int, prefix: str, should_pass: bool):
    """ Unit test for create_storage_prefix. """
    address_bytes = bytes.fromhex(address) if address is not None else None
    prefix_bytes = bytes.fromhex(prefix)
    if should_pass:
        assert composite_keys.create_storage_prefix(address_bytes, incarnation) == prefix_bytes
    else:
        with pytest.raises((TypeError)):
            composite_keys.create_storage_prefix(address_bytes, incarnation)

@pytest.mark.parametrize("address_hash,incarnation,location_hash,key,should_pass", [
    # Valid test list
    ('aaa0a443b6b6c22cf89cf939be3f4e24147d194fb3812960dc64e7d3c434f25f', 0, 'f2ee15ea639b73fa3db9b34a245bdfa015c260c598b211bf05a1ecc4b3e3b4f2', 'aaa0a443b6b6c22cf89cf939be3f4e24147d194fb3812960dc64e7d3c434f25f0000000000000000f2ee15ea639b73fa3db9b34a245bdfa015c260c598b211bf05a1ecc4b3e3b4f2', True),

    # Invalid test list
    (None, 0, '', '', False),
    ('', 0, '', '0000000000000000', False),
])
def test_create_composite_storage_key(address_hash: str, incarnation: int, location_hash: str, key: str, should_pass: bool):
    """ Unit test for create_storage_prefix. """
    address_hash_bytes = bytes.fromhex(address_hash) if address_hash is not None else None
    location_hash_bytes = bytes.fromhex(location_hash) if location_hash is not None else None
    key_bytes = bytes.fromhex(key)
    if should_pass:
        assert composite_keys.create_composite_storage_key(address_hash_bytes, incarnation, location_hash_bytes) == key_bytes
    else:
        with pytest.raises((TypeError, ValueError)):
            composite_keys.create_composite_storage_key(address_hash_bytes, incarnation, location_hash_bytes)

@pytest.mark.parametrize("address,incarnation,location_hash,key,should_pass", [
    # Valid test list
    ('', 0, '', '0000000000000000', True),
    ('aaa0a443b6b6c22cf89cf939be3f4e24147d194fb3812960dc64e7d3c434f25f', 0, 'f2ee15ea639b73fa3db9b34a245bdfa015c260c598b211bf05a1ecc4b3e3b4f2', 'aaa0a443b6b6c22cf89cf939be3f4e24147d194fb3812960dc64e7d3c434f25f0000000000000000f2ee15ea639b73fa3db9b34a245bdfa015c260c598b211bf05a1ecc4b3e3b4f2', True),

    # Invalid test list
    (None, 0, '', '', False),
    #('', 0, '', '', False),
])
def test_create_plain_composite_storage_key(address: str, incarnation: int, location_hash: str, key: str, should_pass: bool):
    """ Unit test for create_storage_prefix. """
    address_bytes = bytes.fromhex(address) if address is not None else None
    location_hash_bytes = bytes.fromhex(location_hash) if location_hash is not None else None
    key_bytes = bytes.fromhex(key)
    if should_pass:
        assert composite_keys.create_plain_composite_storage_key(address_bytes, incarnation, location_hash_bytes) == key_bytes
    else:
        with pytest.raises((TypeError)):
            composite_keys.create_plain_composite_storage_key(address_bytes, incarnation, location_hash_bytes)
