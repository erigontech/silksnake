# -*- coding: utf-8 -*-
"""The kv_utils module contains utilities for accessing the turbo-geth/silkworm KV gRPC."""

from silksnake.remote import kv_remote

DEFAULT_TARGET = 'localhost:9090'

def kv_seek(bucket, seek_key, target):
    """ Get the key-value pair for given seek_key from bucket of turbo-geth/silkworm running at target.
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

def kv_seek_func(func, target, *args):
    """ Execute the provided seek function on the KV interface of turbo-geth/silkworm running at target.
    """
    remote_kv_client = kv_remote.new_remote_kv_client()
    remote_kv = remote_kv_client.with_target(target).open()
    try:
        return func(remote_kv.view(), *args)
    finally:
        remote_kv.close()
