# -*- coding: utf-8 -*-
"""The API equivalent to Ethereum JSON RPC."""

from typing import Tuple, Union

from ..core.constants import HASH_SIZE
from ..core import chain, reader
from ..helpers import hashing
from ..remote import kv_remote
from ..rlp import sedes
from ..stagedsync import stages

# pylint: disable=broad-except

class EthereumAPI:
    """ EthereumAPI"""
    def __init__(self, target: str = kv_remote.DEFAULT_TARGET):
        remote_kv_client = kv_remote.RemoteClient(target)
        self.remote_kv = remote_kv_client.open()

    def close(self):
        """ close"""
        self.remote_kv.close()

    def block_number(self):
        """ Get the number of the latest block in the chain. """
        try:
            block_heigth, _ = stages.get_stage_progress(self.remote_kv, stages.SyncStage.FINISH)
            return block_heigth
        except Exception:
            return 0

    def get_block_by_number(self, block_number: int) -> sedes.Block:
        """ Get the block having the given number in the chain. """
        return chain.Blockchain(self.remote_kv).read_block_by_number(block_number)

    def get_block_by_hash(self, block_hash: str) -> sedes.Block:
        """ Get the block having the given hash in the chain. """
        try:
            block_hash_bytes = hashing.hex_as_hash(block_hash)
            return chain.Blockchain(self.remote_kv).read_block_by_hash(block_hash_bytes)
        except Exception:
            return None

    def get_block_transaction_count_by_number(self, block_number: int) -> int:
        """ Get the number of transactions included in block having the given number in the chain. """
        block = chain.Blockchain(self.remote_kv).read_block_by_number(block_number)
        return len(block.body.transactions) if block else -1

    def get_block_transaction_count_by_hash(self, block_hash: str) -> int:
        """ Get the number of transactions included in block having the given hash in the chain. """
        block = chain.Blockchain(self.remote_kv).read_block_by_hash(block_hash)
        return len(block.body.transactions) if block else -1

    def get_storage_at(self, address: str, index: str, block_number_or_hash: str) -> str:
        """ Returns a 32-byte long, zero-left-padded value at index storage location of address or '0x' if no value."""
        try:
            state_reader = reader.StateReader(self.remote_kv, int(block_number_or_hash)) # just block number for now
            account = state_reader.read_account_data(address)
            location_hash = hashing.hex_as_hash(str(index))
            value = state_reader.read_account_storage(address, account.incarnation, location_hash)
            return '0x' + value.hex().zfill(2*HASH_SIZE)
        except Exception:
            return '0x'

    def syncing(self) -> Union[bool, Tuple[int ,int]]:
        """Returns false is already sync'd, otherwise the (currentBlock, highestBlock) couple."""
        try:
            highest_block, _ = stages.get_stage_progress(self.remote_kv, stages.SyncStage.HEADERS)
            current_block, _ = stages.get_stage_progress(self.remote_kv, stages.SyncStage.FINISH)
            if current_block >= highest_block:
                return False
            return highest_block, current_block
        except Exception:
            return False
