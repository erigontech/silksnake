# -*- coding: utf-8 -*-
"""The Recursive Length Prefix (RLP) encoding/decoding for receipts."""

import rlp

from .log import Log
from .sedes import RlpSerializable

class TransactionReceipt(RlpSerializable):
    """ RLP sedes for transaction receipt.
    """
    STATUS_OK = 1
    STATUS_KO = 0

    fields = [
        ('status', rlp.sedes.big_endian_int),
        ('cumulative_gas_used', rlp.sedes.big_endian_int),
        ('logs', rlp.sedes.CountableList(Log)),
    ]

block_receipt_list = rlp.sedes.CountableList(TransactionReceipt)

def decode_block_receipt(block_receipt_bytes: bytes) -> block_receipt_list:
    """ Decode the given bytes as block receipt."""
    return rlp.decode(block_receipt_bytes, block_receipt_list)
