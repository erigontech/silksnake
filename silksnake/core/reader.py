# -*- coding: utf-8 -*-
"""The reader of chain state."""

from ..core import account
from ..core import kvstore
from ..core import history
from ..helpers.dbutils import composite_keys
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
        encoded_account_bytes = history.get_as_of(self.database, False, address_bytes, self.block_number+1)
        return account.Account.from_storage(encoded_account_bytes)

    def read_account_storage(self, address: str, incarnation: int, location_hash: bytes) -> bytes:
        """ read_account_storage """
        address_bytes = Address.from_hex(address).bytes
        storage_key = composite_keys.create_plain_composite_storage_key(address_bytes, incarnation, location_hash)
        encoded_location = history.get_as_of(self.database, True, storage_key, self.block_number+1)
        return encoded_location

    def read_eth_supply(self) -> int:
        """ read_eth_supply """
        return supply.read_eth_supply(self.database.view(), self.block_number)
