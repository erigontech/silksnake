# -*- coding: utf-8 -*-
"""The Ethereum+Turbo JSON RPC API available locally."""

import contextlib

from .eth import EthereumAPI
from .turbo import TurboAPI

# pylint: disable=invalid-name

def eth_getStorageAt(address: str, index: str, block_number_or_hash: str) -> str:
    """ See EthereumAPI#get_storage_at. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.get_storage_at(address, index, block_number_or_hash)

def turbo_getSupply(block_number_or_hash: str) -> int:
    """ See TurboAPI#turbo_getSupply. """
    with contextlib.closing(TurboAPI()) as api:
        return api.get_eth_supply(block_number_or_hash)
