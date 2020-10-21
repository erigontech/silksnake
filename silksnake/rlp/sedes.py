# -*- coding: utf-8 -*-
"""The Recursive Length Prefix (RLP) encoding/decoding."""

from abc import ABC
import typing

import rlp

from ..core.constants import ADDRESS_SIZE, HASH_SIZE, TRIE_ROOT_SIZE, UINT8_SIZE, UINT32_SIZE, UINT256_SIZE, ZERO_ADDRESS, ZERO_HASH32
from ..helpers import hashing

# pylint: disable=too-many-arguments,too-many-instance-attributes,too-many-locals

address = rlp.sedes.Binary.fixed_length(ADDRESS_SIZE, allow_empty=True)
hash32 = rlp.sedes.Binary.fixed_length(HASH_SIZE)
trie_root = rlp.sedes.Binary.fixed_length(TRIE_ROOT_SIZE, allow_empty=True)
uint8 = rlp.sedes.BigEndianInt(UINT8_SIZE)
uint32 = rlp.sedes.BigEndianInt(UINT32_SIZE)
uint256 = rlp.sedes.BigEndianInt(UINT256_SIZE)

class RlpSerializable(rlp.Serializable):
    """ Basic RLP sedes.
    """
    _hash = None

    @property
    def hash(self) -> bytes:
        """ Return the hash of the RLP-serializable object. """
        if self._hash is None:
            self._hash = hashing.bytes_to_hash(rlp.encode(self))
        return self._hash

    def __repr__(self):
        beautify = (lambda v: v.hex() if isinstance(v, bytes) else v)
        keyword_args = tuple("{}={!r}".format(k, beautify(v)) for k, v in self.as_dict().items())
        return "({})".format(", ".join(keyword_args))

    def __str__(self):
        return repr(self)

class BlockKey(RlpSerializable):
    """ RLP sedes for block keys as couple (number, hash).
    """
    fields = [
        ('block_number', uint8),
        ('block_hash', hash32)
    ]

class TransactionFieldsAPI(ABC):
    """ All transaction fields. """
    nonce: int
    gas_price: int
    gas_limit: int
    to: bytes
    value: int
    data: bytes
    v: int
    r: int
    s: int

class Transaction(RlpSerializable, TransactionFieldsAPI):
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

class BlockHeaderFieldsAPI(ABC):
    """ All block header fields. """
    parent_hash: bytes
    ommers_hash: bytes
    coinbase: str
    state_root: bytes
    transactions_root: bytes
    receipts_root: bytes
    logs_bloom: int
    difficulty: int
    block_number: int
    gas_limit: int
    gas_used: int
    timestamp: int
    extra_data: bytes
    mix_hash: bytes
    nonce: int

class BlockHeader(RlpSerializable, BlockHeaderFieldsAPI):
    """ RLP sedes for block headers.
    """
    fields = [
        ('parent_hash', hash32),
        ('ommers_hash', hash32),
        ('coinbase', address),
        ('state_root', trie_root),
        ('transactions_root', trie_root),
        ('receipts_root', trie_root),
        ('logs_bloom', uint256),
        ('difficulty', rlp.sedes.big_endian_int),
        ('block_number', rlp.sedes.big_endian_int),
        ('gas_limit', rlp.sedes.big_endian_int),
        ('gas_used', rlp.sedes.big_endian_int),
        ('timestamp', rlp.sedes.big_endian_int),
        ('extra_data', rlp.sedes.binary),
        ('mix_hash', rlp.sedes.binary),
        ('nonce', rlp.sedes.Binary(UINT8_SIZE, allow_empty=True))
    ]

    def __init__(self,
        parent_hash: bytes = ZERO_HASH32,
        ommers_hash: bytes = ZERO_HASH32,
        coinbase: bytes = ZERO_ADDRESS,
        state_root: bytes = ZERO_HASH32,
        transactions_root: bytes = ZERO_HASH32,
        receipts_root: bytes = ZERO_HASH32,
        logs_bloom: int = 0,
        difficulty: int = 0,
        block_number: int = 0,
        gas_limit: int = 0,
        gas_used: int = 0,
        timestamp: int = 0,
        extra_data: bytes = b'',
        mix_hash: bytes = ZERO_HASH32,
        nonce: bytes = b''):
        """ __init__ """
        RlpSerializable.__init__(self,
            parent_hash,
            ommers_hash,
            coinbase,
            state_root,
            transactions_root,
            receipts_root,
            logs_bloom,
            difficulty,
            block_number,
            gas_limit,
            gas_used,
            timestamp,
            extra_data,
            mix_hash,
            nonce)
        self.parent_hash: parent_hash
        self.ommers_hash: ommers_hash
        self.coinbase: coinbase
        self.state_root: state_root
        self.transactions_root: transactions_root
        self.receipts_root: receipts_root
        self.logs_bloom: logs_bloom
        self.difficulty: difficulty
        self.block_number: block_number
        self.gas_limit: gas_limit
        self.gas_used: gas_used
        self.timestamp: timestamp
        self.extra_data: extra_data
        self.mix_hash: mix_hash
        self.nonce: nonce

    @property
    def block_hash_hex(self) -> str:
        """ Returns the 32-byte block hash as hex string. """
        return self.hash.hex()

    def __str__(self) -> str:
        return f'<BlockHeader #{self.block_number} 0x{self.hash.hex()}>'

transaction_list = rlp.sedes.CountableList(Transaction)
ommer_block_header_list = rlp.sedes.CountableList(BlockHeader)
block_body = rlp.sedes.List([transaction_list, ommer_block_header_list])

class BlockBody:
    """ BlockBody """
    def __init__(self, transactions: typing.List[Transaction], ommer_block_headers: typing.List[BlockHeader]):
        self.transactions = transactions
        self.ommer_block_headers = ommer_block_headers

    def __str__(self) -> str:
        return f'<BlockBody #transactions: {len(self.transactions)} #ommers: {len(self.ommer_block_headers)}>'

class Block:
    """ Block """
    def __init__(self, header: BlockHeader = BlockHeader(), body: BlockBody = BlockBody([], [])):
        self.header = header
        self.body = body

    def __str__(self):
        return f'header: {self.header}, body: {self.body}'

    def __repr__(self):
        return str(self)

    @property
    def hash(self) -> bytes:
        """ Return the hash of the block. """
        return self.header.hash

CANONICAL_SUFFIX = b'\x6e'
CANONICAL_SUFFIX_INT = int.from_bytes(CANONICAL_SUFFIX, 'big')

DIFFICULTY_SUFFIX = b'\x74'
DIFFICULTY_SUFFIX_INT = int.from_bytes(DIFFICULTY_SUFFIX, 'big')

def encode_block_number(block_number: int) -> bytes:
    """ Encode the given block number as 8-byte BigEndian.
    """
    return uint8.serialize(block_number)

def encode_canonical_block_number(block_number: int) -> bytes:
    """ Encode the given block number as 8-byte BigEndian plus canonical suffix.
    """
    return uint8.serialize(block_number) + CANONICAL_SUFFIX

def encode_block_key(block_number: int, block_hash: bytes) -> bytes:
    """ Encode the given block number and hash as 40-byte block key.
    """
    return uint8.serialize(block_number) + hash32.serialize(block_hash)

def encode_difficulty_block_key(block_key: bytes) -> bytes:
    """ Encode the given block key plus difficulty suffix.
    """
    return block_key + DIFFICULTY_SUFFIX

def decode_block_number(block_number_bytes: bytes) -> int:
    """ Decode the given 8-byte BigEndian as block number."""
    return uint8.deserialize(block_number_bytes)

def decode_canonical_block_number(block_number_bytes: bytes) -> int:
    """ Decode the given 9-byte BigEndian as block number plus canonical suffix."""
    assert block_number_bytes[UINT8_SIZE] == CANONICAL_SUFFIX_INT, 'Invalid canonical block number suffix'
    return uint8.deserialize(block_number_bytes[:UINT8_SIZE])

def decode_block_key(block_key_bytes: bytes) -> (int, str):
    """ Decode the given 40-byte as block number and hash concatenated."""
    # The block_key RLP format slightly uncommon requires splitting the input bytes in 2 chuncks.
    return BlockKey.deserialize([block_key_bytes[:UINT8_SIZE], block_key_bytes[UINT8_SIZE:]])

def decode_difficulty_block_key(block_key_bytes: bytes) -> (int, str):
    """ Decode the given bytes as block key plus difficulty suffix."""
    assert block_key_bytes[UINT8_SIZE + HASH_SIZE] == DIFFICULTY_SUFFIX_INT, 'Invalid difficulty block key suffix'
    return decode_block_key(block_key_bytes[:UINT8_SIZE + HASH_SIZE])

def decode_block_header(block_header_bytes: bytes) -> BlockHeader:
    """ Decode the given bytes as block header."""
    return rlp.decode(block_header_bytes, BlockHeader)

def decode_block_body(block_body_bytes: bytes) -> BlockBody:
    """ Decode the given bytes as block body composed by: (transactions, uncles)."""
    return BlockBody(*rlp.decode(block_body_bytes, block_body))

def decode_block_total_difficulty(total_difficulty_bytes: bytes) -> int:
    """ Decode the given bytes as block total difficulty."""
    return rlp.decode(total_difficulty_bytes, rlp.sedes.big_endian_int)
