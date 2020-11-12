# -*- coding: utf-8 -*-
"""The reader of chain state."""

from typing import List ,Tuple
import json

import rlp

from ..core import config, kvstore
from ..helpers.dbutils import tables
from ..remote import kv_metadata
from ..rlp import sedes

class Blockchain:
    """ Blockchain """
    def __init__(self, database: kvstore.KV):
        if database is None:
            raise ValueError('database is null')
        self.database = database

    def read_config(self, chain: str) -> Tuple[int, str]:
        """ read_config """
        if not chain in config.CHAIN_TABLE:
            raise ValueError(f'unknown chain {chain}')
        chain_genesis_hash = config.CHAIN_TABLE[chain]
        key, config_json = self.database.view().get(tables.CONFIG_PREFIX, chain_genesis_hash)
        if key != chain_genesis_hash:
            raise ValueError(f'invalid genesis hash for chain {chain}, key is {key}')
        return json.loads(config_json)

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
            block_body = sedes.decode_block_body(block_body_bytes)
            transaction_sender_list = self.read_block_senders(block_number, block_hash_bytes)
            for index, transaction in enumerate(block_body.transactions):
                transaction.sender = transaction_sender_list[index]
            return block_body
        except rlp.exceptions.DecodingError:
            return None

    def read_block_senders(self, block_number: int, block_hash_bytes: bytes) -> List[bytes]:
        """ read_block_senders """
        encoded_block_key = sedes.encode_block_key(block_number, block_hash_bytes)
        key, txn_senders_bytes = self.database.view().get(tables.TRANSACTION_SENDERS_LABEL, encoded_block_key)
        if key != encoded_block_key:
            return None
        return kv_metadata.decode_account_address_list(txn_senders_bytes)

    def read_transaction_by_hash(self, transaction_hash_bytes: bytes) -> Tuple[sedes.Transaction, int, bytes, int]:
        """ read_transaction_by_hash """
        block_number = self.read_transaction_lookup_entry(transaction_hash_bytes)
        if not block_number:
            return None, -1, b'', -1
        block_hash_bytes = self.read_canonical_block_hash(block_number)
        if not block_hash_bytes:
            return None, -1, b'', -1
        block_body = self.read_block_body(block_number, block_hash_bytes)
        if not block_body:
            return None, -1, b'', -1
        for index, transaction in enumerate(block_body.transactions):
            if transaction.hash == transaction_hash_bytes:
                return transaction, block_number, block_hash_bytes, index
        return None, -1, b'', -1

    def read_transaction_lookup_entry(self, transaction_hash_bytes: bytes) -> int:
        """ read_transaction_lookup_entry """
        key, block_number_bytes = self.database.view().get(tables.TRANSACTION_LOOKUP_LABEL, transaction_hash_bytes)
        if key != transaction_hash_bytes:
            return None
        block_number = int.from_bytes(block_number_bytes, 'big')
        return block_number
