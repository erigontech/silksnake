# -*- coding: utf-8 -*-
"""The additional API available in Turbo-Geth/Silkworm."""

from ..core import reader
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
        try:
            state_reader = reader.StateReader(self.remote_kv, int(block_number_or_hash)) # just block number for now
            eth_supply = state_reader.read_eth_supply()
            return eth_supply
        except ValueError:
            return 0
