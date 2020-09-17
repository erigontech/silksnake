# -*- coding: utf-8 -*-
"""The Recursive Length Prefix (RLP) encoding/decoding."""

import rlp

ADDRESS_SIZE = 20
HASH_SIZE = 32
TRIE_ROOT_SIZE = 32
UINT8_SIZE = 8
UINT256_SIZE = 256

address = rlp.sedes.Binary.fixed_length(ADDRESS_SIZE, allow_empty=True)
hash32 = rlp.sedes.Binary.fixed_length(HASH_SIZE)
trie_root = rlp.sedes.Binary.fixed_length(TRIE_ROOT_SIZE, allow_empty=True)
uint8 = rlp.sedes.BigEndianInt(UINT8_SIZE)
uint256 = rlp.sedes.BigEndianInt(UINT256_SIZE)

class RlpSerializable(rlp.Serializable):
    """ Basic RLP sedes.
    """
    def __str__(self):
        beautify = (lambda v: v.hex() if isinstance(v, bytes) else v)
        keyword_args = tuple("{}={!r}".format(k, beautify(v)) for k, v in self.as_dict().items())
        return "({})".format(", ".join(keyword_args),
        )

class BlockKey(RlpSerializable):
    """ RLP sedes for block keys as couple (number, hash).
    """
    fields = [
        ('block_number', uint8),
        ('block_hash', hash32)
    ]

class Transaction(RlpSerializable):
    """ RLP sedes for block transactions.
    """
    fields = [
        ('nonce', rlp.sedes.big_endian_int),
        ('gas_price', rlp.sedes.big_endian_int),
        ('gas_limit', rlp.sedes.big_endian_int),
        ('to', address),
        ('value', rlp.sedes.big_endian_int),
        ('data', rlp.sedes.binary),
        ('v', rlp.sedes.big_endian_int),
        ('r', rlp.sedes.big_endian_int),
        ('s', rlp.sedes.big_endian_int),
    ]

class Uncle(RlpSerializable):
    """ RLP sedes for uncle blocks.
    """
    fields = [
        ('a', rlp.sedes.binary),
    ]

class BlockHeader(RlpSerializable):
    """ RLP sedes for block headers.
    """
    fields = [
        ('parent_hash', hash32),
        ('uncles_hash', hash32),
        ('coinbase', address),
        ('state_root', trie_root),
        ('transaction_root', trie_root),
        ('receipt_root', trie_root),
        ('bloom', uint256),
        ('difficulty', rlp.sedes.big_endian_int),
        ('block_number', rlp.sedes.big_endian_int),
        ('gas_limit', rlp.sedes.big_endian_int),
        ('gas_used', rlp.sedes.big_endian_int),
        ('timestamp', rlp.sedes.big_endian_int),
        ('extra_data', rlp.sedes.binary),
        ('mix_hash', rlp.sedes.binary),
        ('nonce', rlp.sedes.Binary(UINT8_SIZE, allow_empty=True))
    ]

transaction_list = rlp.sedes.CountableList(Transaction)
uncle_list = rlp.sedes.CountableList(Uncle)
block_body = rlp.sedes.List([transaction_list, uncle_list])

def encode_block_number(block_number: int) -> bytes:
    """ Encode the given block number as 8-byte BigEndian.
    """
    return uint8.serialize(block_number)

def decode_block_number(block_number_bytes: bytes) -> int:
    """ Decode the given 8-byte BigEndian as block number."""
    return uint8.deserialize(block_number_bytes)

def decode_block_hash(block_hash_bytes: bytes) -> bytes:
    """ Decode the given 32-byte as block hash."""
    return hash32.deserialize(block_hash_bytes)

def decode_block_key(block_key_bytes: bytes) -> (int, str):
    """ Decode the given 40-byte as block number and hash concatenated."""
    # The block_key RLP format slightly uncommon requires splitting the input bytes in 2 chuncks.
    return BlockKey.deserialize([block_key_bytes[:UINT8_SIZE], block_key_bytes[UINT8_SIZE:]])

def decode_block_header(block_header_bytes: bytes) -> BlockHeader:
    """ Decode the given -byte as block header."""
    return rlp.decode(block_header_bytes, BlockHeader)

def decode_block_body(block_body_bytes: bytes):
    """ Decode the given bytes as block body composed by: (transactions, uncles)."""
    return rlp.decode(block_body_bytes, block_body)
