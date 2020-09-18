# -*- coding: utf-8 -*-
"""The kv_utils module contains utilities for accessing the turbo-geth/silkworm KV gRPC."""

from silksnake.core.remote import kv_remote

DEFAULT_TARGET = 'localhost:9090'

def kv_seek(bucket, seek_key, target):
    """ Get the key plus value pair from bucket associated to specified seek_key on target.
        bucket - the bucket tag as string
        seek_key - the seek key as bytes
        target - the server location as string <address>:<port>
    """
    remote_kv_client = kv_remote.new_remote_kv_client()
    remote_kv = remote_kv_client.with_target(target).open()
    try:
        key, value = remote_kv.view().get(bucket, seek_key)
    finally:
        remote_kv.close()
    return key, value

def kv_seek_func(seek_func, target):
    """ Execute the provided seek function on target.
    """
    remote_kv_client = kv_remote.new_remote_kv_client()
    remote_kv = remote_kv_client.with_target(target).open()
    try:
        return seek_func(remote_kv.view())
    finally:
        remote_kv.close()
