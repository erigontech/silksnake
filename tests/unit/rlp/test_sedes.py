# -*- coding: utf-8 -*-
"""The unit test for sedes module."""

import rlp

import pytest

from silksnake.rlp import sedes

# pylint: disable=line-too-long,too-many-locals,too-many-arguments

def test_rlp_serializable():
    """ Unit test for RlpSerializable class. """
    class SimpleRlpSerializable(sedes.RlpSerializable):
        """ SimpleRlpSerializable """
        fields = [
            ('a', sedes.uint8),
            ('b', rlp.sedes.binary),
        ]

    serializable = SimpleRlpSerializable(2, b'')
    assert serializable.hash
    assert serializable.hash
    assert str(serializable)
    assert repr(serializable)

def test_transaction():
    """ Unit test for Transaction. """
    txn = sedes.Transaction(
        nonce=0,
        gas_price=1000,
        gas_limit=10000000,
        to='',
        value=0,
        data=0,
        v=27,
        r=0,
        s=0
    )
    assert str(txn)
    assert repr(txn)
    txn.sender = ''
    assert str(txn)
    assert repr(txn)

def test_block_header():
    """ Unit test for BlockHeader. """
    header1 = sedes.BlockHeader()
    assert str(header1)
    assert repr(header1)
    assert header1.block_number == 0
    assert header1.block_hash_hex
    header2 = sedes.BlockHeader(block_number=100)
    assert header2.block_number == 100

def test_block_body():
    """ Unit test for BlockHeader. """
    body = sedes.BlockBody([], [])
    assert str(body)
    assert repr(body)

def test_block():
    """ Unit test for BlockHeader. """
    block1 = sedes.Block()
    assert str(block1)
    assert repr(block1)
    block2 = sedes.Block(sedes.BlockHeader(block_number=100), sedes.BlockBody([], []))
    assert block2.header.block_number == 100
    assert block2.hash == block2.header.hash
    assert str(block2)
    assert repr(block2)

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

@pytest.mark.parametrize("block_header_hex,parent_hash,ommers_hash,coinbase,state_root,transactions_root,receipts_root,logs_bloom_hex,difficulty,block_number_hex,\
    gas_limit_hex,gas_used_hex,timestamp_hex,extra_data_hex,mix_hash,nonce_hex,should_pass", [
    # Valid test list
    ('f9025ca089eb91c78eb54e038c62bdd6340b0fd4e982202ad46284dd5309b997b99bf893a01dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d4934794\
        0000000000000000000000000000000000000000a0de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517a066beb9243c8901affb8e93fdd4619920\
            dd535e9ffacf7f3950707723c6503575a0bab1248cb2f851544996d3a6962c8736146c262665a68650cc24269fecf2f5ceb901000400000000000000000000000000000400\
                0002000000040000000000000040000000000010000000000000000000000000000200000400004000000000200001000000000000000000000028020000000080000000\
                    00000008000000000000000000000000000000000001100000000000000000080000000000001000004008000000040000000000000000000000000000000008000000\
                        00000180000000000200000100000000000001000100000000020000000001000000000c000000080000000200000000040000000000108004000000100000000000\
                            000000000000001010000000000000000000200000000000000000800000000006000000000002831e8481837a1200830b469d845e1df5a8b86100000000000000\
                                0000000000000000000000000000000000000000000000000007246dd875b0e3b053471143338268c67331ad2529823a73db6cc731c8314f8b768eb6a4c8756c\
                                    fcafa9185c5f69c13959e01c388b63a414d6693fc29944b41e01a00000000000000000000000000000000000000000000000000000000000000000880000000000000000',
    '89eb91c78eb54e038c62bdd6340b0fd4e982202ad46284dd5309b997b99bf893',
    '1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
    '0000000000000000000000000000000000000000',
    'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517',
    '66beb9243c8901affb8e93fdd4619920dd535e9ffacf7f3950707723c6503575',
    'bab1248cb2f851544996d3a6962c8736146c262665a68650cc24269fecf2f5ce',
    '0400000000000000000000000000000400000200000004000000000000004000000000001000000000000000000000000000020000040000400000000020000100000000000000000000002802\
        000000008000000000000008000000000000000000000000000000000001100000000000000000080000000000001000004008000000040000000000000000000000000000000008000000000001\
            80000000000200000100000000000001000100000000020000000001000000000C000000080000000200000000040000000000108004000000100000000000000000000000001010000000000000\
                0000002000000000000000008000000000060000000000',
    2,
    '1e8481',
    '7a1200',
    '0b469d',
    '5e1df5a8',
    '000000000000000000000000000000000000000000000000000000000000000007246dd875b0e3b053471143338268c67331ad2529823a73db6cc731c8314f8b768eb6a4c8756cfcafa9185c5f69c13959e01c\
        388b63a414d6693fc29944b41e01',
    '0000000000000000000000000000000000000000000000000000000000000000',
    '0000000000000000',
    True),

    # Invalid test list
    ('',
    '89eb91c78eb54e038c62bdd6340b0fd4e982202ad46284dd5309b997b99bf893',
    '1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
    '0000000000000000000000000000000000000000',
    'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517',
    '66beb9243c8901affb8e93fdd4619920dd535e9ffacf7f3950707723c6503575',
    'bab1248cb2f851544996d3a6962c8736146c262665a68650cc24269fecf2f5ce',
    '0400000000000000000000000000000400000200000004000000000000004000000000001000000000000000000000000000020000040000400000000020000100000000000000000000002802\
        000000008000000000000008000000000000000000000000000000000001100000000000000000080000000000001000004008000000040000000000000000000000000000000008000000000001\
            80000000000200000100000000000001000100000000020000000001000000000C000000080000000200000000040000000000108004000000100000000000000000000000001010000000000000\
                0000002000000000000000008000000000060000000000',
    2,
    '1e8481',
    '7a1200',
    '0b469d',
    '5e1df5a8',
    '000000000000000000000000000000000000000000000000000000000000000007246dd875b0e3b053471143338268c67331ad2529823a73db6cc731c8314f8b768eb6a4c8756cfcafa9185c5f69c13959e01c\
        388b63a414d6693fc29944b41e01',
    '0000000000000000000000000000000000000000000000000000000000000000',
    '0000000000000000',
    False),
    ('d9025ca089eb91c78eb54e038c62bdd6340b0fd4e982202ad46284dd5309b997b99bf893a01dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d4934794\
        0000000000000000000000000000000000000000a0de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517a066beb9243c8901affb8e93fdd4619920\
            dd535e9ffacf7f3950707723c6503575a0bab1248cb2f851544996d3a6962c8736146c262665a68650cc24269fecf2f5ceb901000400000000000000000000000000000400\
                0002000000040000000000000040000000000010000000000000000000000000000200000400004000000000200001000000000000000000000028020000000080000000\
                    00000008000000000000000000000000000000000001100000000000000000080000000000001000004008000000040000000000000000000000000000000008000000\
                        00000180000000000200000100000000000001000100000000020000000001000000000c000000080000000200000000040000000000108004000000100000000000\
                            000000000000001010000000000000000000200000000000000000800000000006000000000002831e8481837a1200830b469d845e1df5a8b86100000000000000\
                                0000000000000000000000000000000000000000000000000007246dd875b0e3b053471143338268c67331ad2529823a73db6cc731c8314f8b768eb6a4c8756c\
                                    fcafa9185c5f69c13959e01c388b63a414d6693fc29944b41e01a00000000000000000000000000000000000000000000000000000000000000000880000000000000000',
    '89eb91c78eb54e038c62bdd6340b0fd4e982202ad46284dd5309b997b99bf893',
    '1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
    '0000000000000000000000000000000000000000',
    'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517',
    '66beb9243c8901affb8e93fdd4619920dd535e9ffacf7f3950707723c6503575',
    'bab1248cb2f851544996d3a6962c8736146c262665a68650cc24269fecf2f5ce',
    '0400000000000000000000000000000400000200000004000000000000004000000000001000000000000000000000000000020000040000400000000020000100000000000000000000002802\
        000000008000000000000008000000000000000000000000000000000001100000000000000000080000000000001000004008000000040000000000000000000000000000000008000000000001\
            80000000000200000100000000000001000100000000020000000001000000000C000000080000000200000000040000000000108004000000100000000000000000000000001010000000000000\
                0000002000000000000000008000000000060000000000',
    2,
    '1e8481',
    '7a1200',
    '0b469d',
    '5e1df5a8',
    '000000000000000000000000000000000000000000000000000000000000000007246dd875b0e3b053471143338268c67331ad2529823a73db6cc731c8314f8b768eb6a4c8756cfcafa9185c5f69c13959e01c\
        388b63a414d6693fc29944b41e01',
    '0000000000000000000000000000000000000000000000000000000000000000',
    '0000000000000000',
    False),
])
def test_decode_block_header(block_header_hex: str, parent_hash: str, ommers_hash: str, coinbase: str, state_root: str, transactions_root: str,\
    receipts_root: str, logs_bloom_hex: str, difficulty: int, block_number_hex: str, gas_limit_hex: str, gas_used_hex: str, timestamp_hex: str,\
        extra_data_hex: str, mix_hash: str, nonce_hex: str, should_pass: bool):
    """ Unit test for decode_block_header function. """
    block_header_bytes = bytes.fromhex(block_header_hex) if block_header_hex else None
    logs_bloom_bytes = bytes.fromhex(logs_bloom_hex) if logs_bloom_hex else None
    block_number_bytes = bytes.fromhex(block_number_hex) if block_number_hex else None
    gas_limit_bytes = bytes.fromhex(gas_limit_hex) if gas_limit_hex else None
    gas_used_bytes = bytes.fromhex(gas_used_hex) if gas_used_hex else None
    timestamp_bytes = bytes.fromhex(timestamp_hex) if timestamp_hex else None
    extra_data_bytes = bytes.fromhex(extra_data_hex) if extra_data_hex else None
    nonce_bytes = bytes.fromhex(nonce_hex) if nonce_hex else None
    if should_pass:
        block_header = sedes.decode_block_header(block_header_bytes)
        assert block_header.parent_hash.hex() == parent_hash
        assert block_header.ommers_hash.hex() == ommers_hash
        assert block_header.coinbase.hex() == coinbase
        assert block_header.state_root.hex() == state_root
        assert block_header.transactions_root.hex() == transactions_root
        assert block_header.receipts_root.hex() == receipts_root
        assert block_header.logs_bloom == int.from_bytes(logs_bloom_bytes, 'big')
        assert block_header.difficulty == difficulty
        assert block_header.block_number == int.from_bytes(block_number_bytes, 'big')
        assert block_header.gas_limit == int.from_bytes(gas_limit_bytes, 'big')
        assert block_header.gas_used == int.from_bytes(gas_used_bytes, 'big')
        assert block_header.timestamp == int.from_bytes(timestamp_bytes, 'big')
        assert block_header.extra_data == extra_data_bytes
        assert block_header.mix_hash.hex() == mix_hash
        assert block_header.nonce == nonce_bytes
    else:
        with pytest.raises((rlp.exceptions.DecodingError)):
            sedes.decode_block_header(block_header_bytes)

@pytest.mark.parametrize("block_key_hex,transactions,ommers,should_pass", [
    # Valid test list
    ('f9048cf90488f8a801841bb9071582dfa29462083c80353df771426d209ef578619ee68d5c7a80b844095ea7b3000000000000000000000000da1fbc048f503635950058953f5c60fc1f564e\
    e60000000000000000000000000000000000000000000000000de0b6b3a76400001ba0ceb15bf1bea9606c5b8c903f2ac0d8899730c072d80dfb59751620fd100e66c9a02f1dafd87d74ee60e6\
    417a989b82ed49d6853c031f741eb661dfc4ecefb9cc87f9024d83021e0e843b9aca00830256f6940919717f260c1b65a97acdab9ff4cfb819d62db980b901e4b6fa6d946469726563746f722d\
    3100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000\
    000000000000000001617b2261726368223a20223634626974222c20226d616368223a20227838365f3634222c2022686f73746e616d65223a20226469726563746f722d656467652d35376334\
    3835383735382d76627a3773222c20226370755f636f756e74223a20322c202273797374656d223a20224c696e7578222c20226c6f61645f6176675f31223a2022302e3230222c20226c6f6164\
    5f6176675f35223a2022302e3238222c20226c6f61645f6176675f3135223a2022302e3237222c20226d656d5f746f74616c223a202234303137353732206b42222c20226d656d5f6672656522\
    3a2022313438313038206b42222c2022757074696d655f686f757273223a203834372c202273746f726167655f746f74616c5f6762223a2039362c202273746f726167655f757365645f676222\
    3a2032352c202273746f726167655f667265655f6762223a2037312c202269705f61646472223a202231302e3234342e302e313332227d00000000000000000000000000000000000000000000\
    0000000000000000002ea0303bf9987100f2fccfd643bc2a2625964588484945ed29c01f1e9b73ce1bfa1da04c11cb135d804f5176f708b116ab7e78b42d2c401c0fd12857f038f01f9f60adf9\
    018b028502540be400830b6b9d943158a2785200d254599edbd0bf01c4ced12f499d80b9012460c627be0000000000000000000000000000000000000000000000000000000000000001000000\
    0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000\
    000000000000000000000000000000000000000000000000000000001de009ce130d6bf200e6deb062f02c8912673cd300000000000000000000000033ee33fc3e1aacdb75a1ad362489ac54f0\
    2d6d6300000000000000000000000000000000000000000000000000000000fffff831000000000000000000000000000000000000000000000000000000000000000200000000000000000000\
    000000000000000000000000000000000000000000002ea0f5ec4827c404320a1f9121b125202109a1144f898c6384f6bdc2f0eb65e2356aa0121fae673f2802f88c9a1d54afd597a347f219ae\
    ff74e8178343352958e50327c0',
    [
        (),
        (),
        (),
    ],
    [],
    True),

    # Invalid test list
    ('', [], [], False),
    (None, [], [], False),
])
def test_decode_block_body(block_key_hex: str, transactions: list, ommers: list, should_pass: bool):
    """ Unit test for decode_block_body function. """
    block_key_bytes = bytes.fromhex(block_key_hex) if block_key_hex else None
    if should_pass:
        decoded_block_body = sedes.decode_block_body(block_key_bytes)
        assert len(decoded_block_body.transactions) == len(transactions)
        assert len(decoded_block_body.ommer_block_headers) == len(ommers)
    else:
        with pytest.raises((rlp.exceptions.DecodingError)):
            sedes.decode_block_body(block_key_bytes)

@pytest.mark.parametrize("total_difficulty_hex,result,should_pass", [
    # Valid test list
    ('832e0fe2', 3018722, True),

    # Invalid test list
    (None, 0, False),
    ('', 0, False),
])
def test_decode_block_total_difficulty(total_difficulty_hex: bytes, result: int, should_pass: bool):
    """ Unit test for decode_block_total_difficulty function. """
    total_difficulty_bytes = bytes.fromhex(total_difficulty_hex) if total_difficulty_hex else None
    if should_pass:
        decoded_total_difficulty = sedes.decode_block_total_difficulty(total_difficulty_bytes)
        assert decoded_total_difficulty == result
    else:
        with pytest.raises((rlp.exceptions.DecodingError)):
            sedes.decode_block_total_difficulty(total_difficulty_bytes)
