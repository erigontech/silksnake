# -*- coding: utf-8 -*-
"""The additional API available in Turbo-Geth/Silkworm."""

from ..core import chain, reader
from ..helpers import hashing
from ..remote import kv_remote

class TurboAPI:
    """ TurboAPI"""
    def __init__(self, target: str = kv_remote.DEFAULT_TARGET):
        remote_kv_client = kv_remote.RemoteClient(target)
        self.remote_kv = remote_kv_client.open()

    def close(self):
        """ close"""
        self.remote_kv.close()

    def get_eth_supply(self, block_number_or_hash: str) -> str:
        """ Returns the 64-byte total supply of ETH currency at specified block_number_or_hash."""
        if isinstance(block_number_or_hash, int):
            block_number = int(block_number_or_hash)
        else:
            block_hash = str(block_number_or_hash)
            block_hash_bytes = hashing.hex_as_hash(block_hash)
            block_number = chain.Blockchain(self.remote_kv).read_canonical_block_number(block_hash_bytes)
        state_reader = reader.StateReader(self.remote_kv, block_number)
        eth_supply = state_reader.read_eth_supply()
        return eth_supply
