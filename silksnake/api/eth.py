# -*- coding: utf-8 -*-
"""The API equivalent to Ethereum JSON RPC."""

from ..core.constants import HASH_SIZE
from ..core import reader
from ..helpers import hashing
from ..remote import kv_remote

class EthereumAPI:
    """ EthereumAPI"""
    def __init__(self, target: str = kv_remote.DEFAULT_TARGET):
        remote_kv_client = kv_remote.RemoteClient(target)
        self.remote_kv = remote_kv_client.open()

    def close(self):
        """ close"""
        self.remote_kv.close()

    def get_storage_at(self, address: str, index: str, block_number_or_hash: str) -> str:
        """ Returns a 32-byte long, zero-left-padded value at index storage location of address or '0x' if no value."""
        try:
            state_reader = reader.StateReader(self.remote_kv, int(block_number_or_hash)) # just block number for now
            account = state_reader.read_account_data(address)
            location_hash = hashing.hex_as_hash(str(index))
            value = state_reader.read_account_storage(address, account.incarnation, location_hash)
            return '0x' + value.hex().zfill(2*HASH_SIZE)
        except ValueError:
            return '0x'
