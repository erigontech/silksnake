# -*- coding: utf-8 -*-
"""The reader of chain state."""

from typing import Union

from ..core import account
from ..core import kvstore
from ..core import history
from ..helpers.dbutils import composite_keys, tables
from ..state import supply
from ..types.address import Address

class StateReader:
    """ StateReader """
    def __init__(self, database: kvstore.KV, block_number: int):
        if database is None:
            raise ValueError('database is null')
        if block_number is None:
            raise ValueError('block_number is null')
        self.database = database
        self.block_number = block_number

    def read_account_data(self, address: str) -> account.Account:
        """ read_account_data """
        address_bytes = Address.from_hex(address).bytes
        encoded_account_bytes = history.get_as_of(self.database, False, address_bytes, self.block_number)
        return account.Account.from_storage(encoded_account_bytes)

    def read_account_storage(self, address: str, incarnation: int, location_hash: Union[bytes, str]) -> bytes:
        """ read_account_storage """
        address_bytes = Address.from_hex(address).bytes
        location_hash_bytes = location_hash if isinstance(location_hash, bytes) else bytes.fromhex(location_hash)
        storage_key = composite_keys.create_plain_composite_storage_key(address_bytes, incarnation, location_hash_bytes)
        location_value = history.get_as_of(self.database, True, storage_key, self.block_number)
        return location_value

    def read_code(self, code_hash: str) -> bytes:
        """ read_code """
        code_hash_bytes = bytes.fromhex(code_hash)
        key, value = self.database.view().get(tables.CODE_LABEL, code_hash_bytes)
        return value if key == code_hash_bytes else bytes()

    def read_eth_supply(self) -> int:
        """ read_eth_supply """
        return supply.read_eth_supply(self.database.view(), self.block_number)
