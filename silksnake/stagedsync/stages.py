# -*- coding: utf-8 -*-
"""Turbo-Geth/Silkworm perform network synchronization in sequential stages."""

import enum

from ..core import kvstore
from ..helpers.dbutils import tables

SYNC_STAGE_HEADERS: bytes               = "Headers".encode()             # Downloads headers, verifying their POW validity and chaining
SYNC_STAGE_BLOCK_HASHES: bytes          = "BlockHashes".encode()         # Writes header numbers, fills blockHash => number table
SYNC_STAGE_BODIES: bytes                = "Bodies".encode()              # Downloads block bodies, TxHash and UncleHash are getting verified
SYNC_STAGE_SENDERS: bytes               = "Senders".encode()             # "From" recovered from signatures, bodies re-written
SYNC_STAGE_EXECUTION: bytes             = "Execution".encode()           # Executing each block w/o building a trie
SYNC_STAGE_INTERMEDIATE_HASHES: bytes   = "IntermediateHashes".encode()  # Generate intermediate hashes, calculate the state root hash
SYNC_STAGE_HASH_STATE: bytes            = "HashState".encode()           # Apply Keccak256 to all the keys in the state
SYNC_STAGE_ACCOUNT_HISTORY_INDEX: bytes = "AccountHistoryIndex".encode() # Generating history index for accounts
SYNC_STAGE_STORAGE_HISTORY_INDEX: bytes = "StorageHistoryIndex".encode() # Generating history index for storage
SYNC_STAGE_LOG_INDEX: bytes             = "LogIndex".encode()            # Generating logs index (from receipts)
SYNC_STAGE_TX_LOOKUP: bytes             = "TxLookup".encode()            # Generating transactions lookup index
SYNC_STAGE_TX_POOL: bytes               = "TxPool".encode()              # Starts Backend
SYNC_STAGE_FINISH: bytes                = "Finish".encode()              # Nominal stage after all other stages

class SyncStage(enum.Enum):
    """The synchronization stage."""
    HEADERS               = "Headers".encode()             # Downloads headers, verifying their POW validity and chaining
    BLOCK_HASHES          = "BlockHashes".encode()         # Writes header numbers, fills blockHash => number table
    BODIES                = "Bodies".encode()              # Downloads block bodies, TxHash and UncleHash are getting verified
    SENDERS               = "Senders".encode()             # "From" recovered from signatures, bodies re-written
    EXECUTION             = "Execution".encode()           # Executing each block w/o building a trie
    INTERMEDIATE_HASHES   = "IntermediateHashes".encode()  # Generate intermediate hashes, calculate the state root hash
    HASH_STATE            = "HashState".encode()           # Apply Keccak256 to all the keys in the state
    ACCOUNT_HISTORY_INDEX = "AccountHistoryIndex".encode() # Generating history index for accounts
    STORAGE_HISTORY_INDEX = "StorageHistoryIndex".encode() # Generating history index for storage
    LOG_INDEX             = "LogIndex".encode()            # Generating logs index (from receipts)
    TX_LOOKUP             = "TxLookup".encode()            # Generating transactions lookup index
    TX_POOL               = "TxPool".encode()              # Starts Backend
    FINISH                = "Finish".encode()              # Nominal stage after all other stages

def get_stage_progress(database: kvstore.KV, stage_key: SyncStage) -> (int, bytes):
    """ get_stage_progress """
    key, value = database.view().get(tables.SYNC_STAGE_PROGRESS_LABEL, stage_key.value)
    if key != stage_key.value:
        raise ValueError('stage key mismatch, expected {0} got {1}'.format(stage_key.value.hex(), key.hex()))
    return unmarshal_data(value)

def unmarshal_data(data: bytes) -> (int, bytes):
    """ unmarshal_data """
    if len(data) == 0:
        return (0, b'')
    if len(data) < 8:
        raise ValueError('data too short, expected {0} got {1}'.format(8, len(data)))

    return int.from_bytes(data[:8], 'big'), data[8:]
