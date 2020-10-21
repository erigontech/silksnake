# -*- coding: utf-8 -*-
"""The unit test for hashing module."""

import pytest

from silksnake.helpers import hashing

# pylint: disable=line-too-long

@pytest.mark.parametrize("data,hashed,should_pass", [
    # Valid test list
    ('', 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', True),
    ('00', 'bc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a', True),

    # Invalid test list
    (None, '', False),
])
def test_bytes_to_hash(data: str, hashed: str, should_pass: bool):
    """ Unit test for bytes_to_hash. """
    data_bytes = bytes.fromhex(data) if data is not None else None
    hashed_bytes = bytes.fromhex(hashed)
    if should_pass:
        assert hashing.bytes_to_hash(data_bytes) == hashed_bytes
    else:
        with pytest.raises((TypeError, ValueError)):
            hashing.bytes_to_hash(data_bytes)

@pytest.mark.parametrize("data,hashed,should_pass", [
    # Valid test list
    ('', 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', True),
    ('00', 'bc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a', True),

    # Invalid test list
    (None, '', False),
])
def test_hex_to_hash(data: str, hashed: str, should_pass: bool):
    """ Unit test for hex_to_hash. """
    hashed_bytes = bytes.fromhex(hashed)
    if should_pass:
        assert hashing.hex_to_hash(data) == hashed_bytes
    else:
        with pytest.raises((AttributeError)):
            hashing.hex_to_hash(data)

@pytest.mark.parametrize("data,hashed_hex,should_pass", [
    # Valid test list
    ('', '0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', True),
    ('00', '0xbc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a', True),

    # Invalid test list
    (None, '', False),
])
def test_hex_to_hash_str(data: str, hashed_hex: str, should_pass: bool):
    """ Unit test for hex_to_hash_str. """
    if should_pass:
        assert hashing.hex_to_hash_str(data) == hashed_hex
    else:
        with pytest.raises((AttributeError)):
            hashing.hex_to_hash_str(data)

@pytest.mark.parametrize("data,hashed,should_pass", [
    # Valid test list
    ('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', True),
    ('0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', True),
    ('d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', '00d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', True),
    ('045d85a470', '000000000000000000000000000000000000000000000000000000045d85a470', True),
    ('bc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a00', 'bc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a', True),
    ('bc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a0000000000000000', 'bc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a', True),

    # Invalid test list
    (None, '', False),
])
def test_hex_as_hash(data: str, hashed: str, should_pass: bool):
    """ Unit test for hex_as_hash. """
    hashed_bytes = bytes.fromhex(hashed)
    if should_pass:
        assert hashing.hex_as_hash(data) == hashed_bytes
    else:
        with pytest.raises((AttributeError)):
            hashing.hex_as_hash(data)
