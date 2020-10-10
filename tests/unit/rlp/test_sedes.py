# -*- coding: utf-8 -*-
"""The unit test for sedes module."""

import rlp

import pytest

from silksnake.rlp import sedes

# pylint: disable=line-too-long

def test_rlp_serializable():
    """ Unit test for RlpSerializable class. """
    class SimpleRlpSerializable(sedes.RlpSerializable):
        """ SimpleRlpSerializable """
        fields = [
            ('a', sedes.uint8),
            ('b', rlp.sedes.binary),
        ]

    serializable = SimpleRlpSerializable(2, b'')
    assert str(serializable)
    assert repr(serializable)

@pytest.mark.parametrize("block_number,result,should_pass", [
    # Valid test list
    (0, b'\x00\x00\x00\x00\x00\x00\x00\x00', True),
    (145278, b'\x00\x00\x00\x00\x00\x027~', True),

    # Invalid test list
    (None, b'', False),
    (-1, b'', False),
])
def test_encode_block_number(block_number: int, result: bytes, should_pass: bool):
    """ Unit test for encode_block_number function. """
    if should_pass:
        encoded_block_number = sedes.encode_block_number(block_number)
        assert encoded_block_number == result
    else:
        with pytest.raises((rlp.exceptions.SerializationError)):
            sedes.encode_block_number(block_number)

@pytest.mark.parametrize("block_number,result,should_pass", [
    # Valid test list
    (0, b'\x00\x00\x00\x00\x00\x00\x00\x00\x6e', True),
    (145278, b'\x00\x00\x00\x00\x00\x027~\x6e', True),

    # Invalid test list
    (None, b'', False),
    (-1, b'', False),
])
def test_encode_canonical_block_number(block_number: int, result: bytes, should_pass: bool):
    """ Unit test for encode_canonical_block_number function. """
    if should_pass:
        encoded_block_number = sedes.encode_canonical_block_number(block_number)
        assert encoded_block_number == result
    else:
        with pytest.raises((rlp.exceptions.SerializationError)):
            sedes.encode_canonical_block_number(block_number)

@pytest.mark.parametrize("block_number,block_hash,result,should_pass", [
    # Valid test list
    (0, 'bf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a', '0000000000000000bf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a', True),
    (3546492, '518667fb75544e833b69a889d89a7603e116a313a2b18b341cf40fa8d1ee1fb7', '0000000000361d7c518667fb75544e833b69a889d89a7603e116a313a2b18b341cf40fa8d1ee1fb7', True),

    # Invalid test list
    (None, '', '', False),
    (-1, '', '', False),
])
def test_encode_block_key(block_number: int, block_hash: str, result: str, should_pass: bool):
    """ Unit test for encode_block_key function. """
    block_hash_bytes = bytes.fromhex(block_hash) if block_hash else None
    if should_pass:
        block_key = sedes.encode_block_key(block_number, block_hash_bytes)
        assert block_key.hex() == result
    else:
        with pytest.raises((rlp.exceptions.SerializationError)):
            sedes.encode_block_key(block_number, block_hash_bytes)

@pytest.mark.parametrize("block_key,result,should_pass", [
    # Valid test list
    ('0000000000000000bf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a', '0000000000000000bf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a74', True),
    ('0000000000361d7c518667fb75544e833b69a889d89a7603e116a313a2b18b341cf40fa8d1ee1fb7', '0000000000361d7c518667fb75544e833b69a889d89a7603e116a313a2b18b341cf40fa8d1ee1fb774', True),

    # Invalid test list
    (None, '', False),
    ('', '', False),
])
def test_encode_difficulty_block_key(block_key: str, result: str, should_pass: bool):
    """ Unit test for encode_difficulty_block_key function. """
    block_key_bytes = bytes.fromhex(block_key) if block_key else None
    if should_pass:
        difficulty_block_key = sedes.encode_difficulty_block_key(block_key_bytes)
        assert difficulty_block_key.hex() == result
    else:
        with pytest.raises((TypeError)):
            sedes.encode_difficulty_block_key(block_key_bytes)

@pytest.mark.parametrize("block_number_bytes,result,should_pass", [
    # Valid test list
    (b'\x00\x00\x00\x00\x00\x00\x00\x00', 0, True),
    (b'\x00\x00\x00\x00\x00\x027~', 145278, True),

    # Invalid test list
    (b'', None, False),
    (b'', -1, False),
])
def test_decode_block_number(block_number_bytes: bytes, result: int, should_pass: bool):
    """ Unit test for decode_block_number function. """
    if should_pass:
        decoded_block_number = sedes.decode_block_number(block_number_bytes)
        assert decoded_block_number == result
    else:
        with pytest.raises((rlp.exceptions.DeserializationError)):
            sedes.decode_block_number(block_number_bytes)

@pytest.mark.parametrize("block_key_bytes,result,should_pass", [
    # Valid test list
    (b'\x00\x00\x00\x00\x00\x00\x00\x00\x6e', 0, True),
    (b'\x00\x00\x00\x00\x00\x027~\x6e', 145278, True),

    # Invalid test list
    (b'', None, False),
    (b'', -1, False),
    (b'\x00\x00\x00\x00\x00\x00\x00\x00\x6f', 0, False)
])
def test_decode_canonical_block_number(block_key_bytes: bytes, result: bytes, should_pass: bool):
    """ Unit test for decode_canonical_block_number function. """
    if should_pass:
        decoded_block_number = sedes.decode_canonical_block_number(block_key_bytes)
        assert decoded_block_number == result
    else:
        with pytest.raises((AssertionError, IndexError)):
            sedes.decode_canonical_block_number(block_key_bytes)

@pytest.mark.parametrize("block_key_hex,block_number,block_hash,should_pass", [
    # Valid test list
    ('0000000000000000bf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a', 0, 'bf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a', True),
    ('0000000000361d7c518667fb75544e833b69a889d89a7603e116a313a2b18b341cf40fa8d1ee1fb7', 3546492, '518667fb75544e833b69a889d89a7603e116a313a2b18b341cf40fa8d1ee1fb7', True),

    # Invalid test list
    (None, 0, '', False),
    ('', 0, '', False),
])
def test_decode_block_key(block_key_hex: str, block_number: int, block_hash: str, should_pass: bool):
    """ Unit test for decode_block_key function. """
    block_key_bytes = bytes.fromhex(block_key_hex) if block_key_hex else None
    if should_pass:
        decoded_block_number, decoded_block_hash = sedes.decode_block_key(block_key_bytes)
        assert decoded_block_number == block_number
        assert decoded_block_hash.hex() == block_hash
    else:
        with pytest.raises((TypeError)):
            sedes.decode_block_key(block_key_bytes)

@pytest.mark.parametrize("block_key,block_number,block_hash,should_pass", [
    # Valid test list
    #('0000000000000000bf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a74', 0, '331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a74', True),
    ('0000000000361d7c518667fb75544e833b69a889d89a7603e116a313a2b18b341cf40fa8d1ee1fb774', 3546492, '518667fb75544e833b69a889d89a7603e116a313a2b18b341cf40fa8d1ee1fb7', True),

    # Invalid test list
    (None, 0, '', False),
])
def test_decode_difficulty_block_key(block_key: str, block_number: int, block_hash: str, should_pass: bool):
    """ Unit test for decode_difficulty_block_key function. """
    block_key_bytes = bytes.fromhex(block_key) if block_key else None
    if should_pass:
        decoded_block_number, decoded_block_hash = sedes.decode_difficulty_block_key(block_key_bytes)
        assert decoded_block_number == block_number
        assert decoded_block_hash.hex()[:32] == block_hash[:32]
    else:
        with pytest.raises((TypeError)):
            sedes.decode_difficulty_block_key(block_key_bytes)
