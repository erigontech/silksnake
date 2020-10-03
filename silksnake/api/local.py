# -*- coding: utf-8 -*-
"""The Ethereum JSON RPC API available locally."""

import contextlib

from .eth import EthereumAPI

def eth_getStorageAt(address: str, index: str, block_number_or_hash: str) -> str: # pylint: disable=invalid-name
    """ See EthereumAPI#get_storage_at. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.get_storage_at(address, index, block_number_or_hash)
