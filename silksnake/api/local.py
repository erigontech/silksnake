# -*- coding: utf-8 -*-
"""The Ethereum+Turbo JSON RPC API available locally."""

import contextlib
from typing import Tuple, Union

from .eth import EthereumAPI
from .turbo import TurboAPI

# pylint: disable=invalid-name

def eth_blockNumber() -> int:
    """ See EthereumAPI#block_number. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.block_number()

def eth_getBlockByNumber(block_number: int):
    """ See EthereumAPI#block_by_number. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.get_block_by_number(block_number)

def eth_getBlockByHash(block_hash: str):
    """ See EthereumAPI#block_by_hash. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.get_block_by_hash(block_hash)

def eth_getBlockTransactionCountByNumber(block_number: int) -> int:
    """ See EthereumAPI#get_block_transaction_count_by_number. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.get_block_transaction_count_by_number(block_number)

def eth_getBlockTransactionCountByHash(block_hash: str) -> int:
    """ See EthereumAPI#get_block_transaction_count_by_hash. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.get_block_transaction_count_by_hash(block_hash)

def eth_getStorageAt(address: str, index: str, block_number_or_hash: Union[int, str]) -> str:
    """ See EthereumAPI#get_storage_at. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.get_storage_at(address, index, block_number_or_hash)

def eth_getTransactionByHash(transaction_hash: str):
    """ See EthereumAPI#get_transaction_by_hash """
    with contextlib.closing(EthereumAPI()) as api:
        return api.get_transaction_by_hash(transaction_hash)

def eth_syncing() -> Union[bool, Tuple[int ,int]]:
    """ See EthereumAPI#eth_syncing. """
    with contextlib.closing(EthereumAPI()) as api:
        return api.syncing()

def turbo_getSupply(block_number_or_hash: str) -> int:
    """ See TurboAPI#turbo_getSupply. """
    with contextlib.closing(TurboAPI()) as api:
        return api.get_eth_supply(block_number_or_hash)
