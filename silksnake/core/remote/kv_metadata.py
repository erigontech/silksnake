# -*- coding: utf-8 -*-
"""The turbo-geth/silkworm KV application protocol metadata."""

BLOCK_BODIES_LABEL: str = 'b'
BLOCK_HEADERS_LABEL: str = 'h'
BLOCK_RECEIPTS_LABEL: str = 'r'

BLOCK_BODIES_NAME: str = 'Block Bodies'
BLOCK_HEADERS_NAME: str = 'Headers'
BLOCK_RECEIPTS_NAME: str = 'Receipts'

bucketLabels = [
    BLOCK_BODIES_LABEL,
    BLOCK_HEADERS_LABEL,
    BLOCK_RECEIPTS_LABEL,
]

bucketDescriptors: [str] = {
    BLOCK_BODIES_LABEL: BLOCK_BODIES_NAME,
    BLOCK_HEADERS_LABEL: BLOCK_HEADERS_NAME,
    BLOCK_RECEIPTS_LABEL: BLOCK_RECEIPTS_NAME,
}

def encode_block_number(block_number: int) -> bytes:
    """ Encode the given block number as 8-byte BigEndian.
    """
    return block_number.to_bytes(8, 'big')

def decode_block_number(block_number_bytes: bytes) -> int:
    """ Decode the given 8-byte BigEndian as block number.
    """
    return int.from_bytes(block_number_bytes, 'big')
