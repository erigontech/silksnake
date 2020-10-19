# -*- coding: utf-8 -*-
"""The reader of chain state."""

import rlp

from ..core import kvstore
from ..helpers.dbutils import tables
from ..rlp import sedes

class Blockchain:
    """ Blockchain """
    def __init__(self, database: kvstore.KV):
        if database is None:
            raise ValueError('database is null')
        self.database = database

    def read_block_by_number(self, block_number: int) -> sedes.Block:
        """ read_block_by_number """
        block_hash_bytes = self.read_canonical_block_hash(block_number)
        if not block_hash_bytes:
            return None
        return self.read_block(block_number, block_hash_bytes)

    def read_block_by_hash(self, block_hash_bytes: bytes) -> sedes.Block:
        """ read_block_by_hash """
        block_number = self.read_canonical_block_number(block_hash_bytes)
        if block_number is None:
            return None
        return self.read_block(block_number, block_hash_bytes)

    def read_canonical_block_hash(self, block_number: int) -> bytes:
        """ read_canonical_hash """
        canonical_block_number = sedes.encode_canonical_block_number(block_number)
        key, block_hash_bytes = self.database.view().get(tables.BLOCK_HEADERS_LABEL, canonical_block_number)
        if key != canonical_block_number:
            return None
        return block_hash_bytes

    def read_canonical_block_number(self, block_hash_bytes: bytes) -> bytes:
        """ read_canonical_block_number """
        key, block_number_bytes = self.database.view().get(tables.BLOCK_HEADER_NUMBERS_LABEL, block_hash_bytes)
        if key != block_hash_bytes:
            return None
        try:
            return sedes.decode_block_number(block_number_bytes)
        except rlp.exceptions.DeserializationError:
            return None

    def read_block(self, block_number: int, block_hash_bytes: bytes) -> sedes.Block:
        """ read_block """
        block_header = self.read_block_header(block_number, block_hash_bytes)
        if not block_header:
            return None
        block_body = self.read_block_body(block_number, block_hash_bytes)
        if not block_body:
            return None
        return sedes.Block(block_header, block_body)

    def read_block_header(self, block_number: int, block_hash_bytes: bytes) -> sedes.BlockHeader:
        """ read_block_header """
        encoded_block_key = sedes.encode_block_key(block_number, block_hash_bytes)
        key, block_header_bytes = self.database.view().get(tables.BLOCK_HEADERS_LABEL, encoded_block_key)
        if key != encoded_block_key:
            return None
        try:
            return sedes.decode_block_header(block_header_bytes)
        except rlp.exceptions.DecodingError:
            return None

    def read_block_body(self, block_number: int, block_hash_bytes: bytes) -> sedes.BlockBody:
        """ read_block_body """
        encoded_block_key = sedes.encode_block_key(block_number, block_hash_bytes)
        key, block_body_bytes = self.database.view().get(tables.BLOCK_BODIES_LABEL, encoded_block_key)
        if key != encoded_block_key:
            return None
        try:
            return sedes.decode_block_body(block_body_bytes)
        except rlp.exceptions.DecodingError:
            return None
