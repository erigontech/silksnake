# -*- coding: utf-8 -*-
"""The kv_utils module contains utilities for accessing the turbo-geth/silkworm KV gRPC."""

from silksnake.core.remote import kv_remote

DEFAULT_TARGET = 'localhost:9090'

def kv_seek(bucket, seek_key, target):
    """ Execute
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
