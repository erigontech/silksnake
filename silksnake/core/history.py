# -*- coding: utf-8 -*-
"""The chain data history."""

# pylint: disable=too-many-branches,too-many-locals

from . import account
from . import changeset
from . import kvstore
from . import history_index
from ..helpers.dbutils import composite_keys, tables, timestamp

from .constants import ADDRESS_SIZE, BLOCK_NUMBER_SIZE, HASH_SIZE

def get_as_of(database: kvstore.KV, storage: bool, key: bytes, block_number: int) -> bytes:
    """get_as_of"""
    view = database.view()

    # First, search key in state history by block...
    value = find_by_history(view, storage, key, block_number)
    if value is None:
        # ... if not found, search key in current state
        _, value = view.get(tables.PLAIN_STATE_LABEL, key)
    return value

def find_by_history(view: kvstore.View, storage: bool, key: bytes, block_number: int) -> (bytes, bytes):
    """find_by_history"""
    if storage:
        bucket = tables.STORAGE_HISTORY_LABEL
    else:
        bucket = tables.ACCOUNTS_HISTORY_LABEL

    index_chunck_key = history_index.index_chunck_key(key, block_number)

    k, value = view.cursor(bucket).seek(index_chunck_key)
    if storage:
        if not k[:ADDRESS_SIZE] == key[:ADDRESS_SIZE] or not k[ADDRESS_SIZE:ADDRESS_SIZE+HASH_SIZE] == key[ADDRESS_SIZE+BLOCK_NUMBER_SIZE:]:
            return None
    else:
        if not k.startswith(key):
            return None

    change_set_block, is_set, found = history_index.HistoryIndex(value).search(block_number)
    if found:
        if is_set and not storage:
            return None
        change_set_bucket = tables.PLAIN_STORAGE_CHANGE_SET_LABEL if storage else tables.PLAIN_ACCOUNTS_CHANGE_SET_LABEL
        change_set_key = timestamp.encode_timestamp(change_set_block)
        _, change_set_data = view.get(change_set_bucket, change_set_key)

        if storage:
            data = changeset.PlainStorageChangeSet(change_set_data).find(key)
        else:
            data = changeset.PlainAccountChangeSet(change_set_data).find(key)
    else:
        return None

    if not storage:
        acc = account.Account.from_storage(data)
        if acc.incarnation > 0 and not acc.code_hash:
            _, code_hash = view.get(tables.PLAIN_CONTRACT_CODE_LABEL, composite_keys.create_storage_prefix(key, acc.incarnation))
            if not code_hash:
                return None
            if len(code_hash) > 0:
                acc.code_hash = code_hash.hex()
            data = bytearray(acc.length_for_storage())
            acc.to_storage(data)
            data = bytes(data)

    return data
