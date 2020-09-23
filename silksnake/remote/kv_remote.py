# -*- coding: utf-8 -*-
"""The TurboGeth/Silkworm KV gRPC remote client."""

import grpc

from silksnake.remote import kv_lmdb
from silksnake.remote.proto import kv_pb2, kv_pb2_grpc

def new_remote_kv_client():
    """ Create a new remote KV client.
    """
    return RemoteClient(kv_lmdb.DefaultBucketConfigsFunc)

class RemoteClient:
    """ This class represents the remote KV client.
    """
    def __init__(self, bucket_configs_func):
        self.target = 'localhost:9090'
        self.bucket_configs_func = bucket_configs_func

    def with_bucket_configs_func(self, bucket_configs_func):
        """ Configure the client to use the specified bucket configuration functor.
        """
        self.bucket_configs_func = bucket_configs_func

    def with_target(self, target):
        """ Configure the client to use the specified server (address:port) end point.
        """
        self.target = target
        return self

    def open(self):
        """ Open a new remote KV store instance.
        """
        channel = grpc.insecure_channel(self.target)
        kv_stub = kv_pb2_grpc.KVStub(channel)
        return RemoteKV(self, channel, kv_stub)

class RemoteKV:
    """ This class represents the remote KV store.
    """
    def __init__(self, opts, channel, kv_stub):
        self.opts = opts
        self.channel = channel
        self.kv_stub = kv_stub

    def view(self):
        """ Get a read-only view on the KV."""
        return RemoteView(self)

    def close(self):
        """ Close the remove KV."""
        self.channel.close()

class RemoteView:
    """ This class represents a remote read-only view on the KV.
    """
    def __init__(self, remote_kv_store):
        self.remote_kv_store = remote_kv_store

    def cursor(self, bucket_name):
        """ Create a new remote cursor on the KV."""
        return RemoteCursor(self.remote_kv_store, bucket_name)

    def get(self, bucket_name, key):
        """ Get the value associated to the key in specified bucket."""
        return self.cursor(bucket_name).seek(key)

    def get_exact(self, bucket_name, key):
        """ Get the value associated to the key in specified bucket, checking exact key match."""
        return self.cursor(bucket_name).seek_exact(key)

class RemoteCursor:
    """ This class represents a remote read-only cursor on the KV.
    """
    def __init__(self, remote_kv_store, bucket_name):
        self.remote_kv_store = remote_kv_store
        self.bucket_name = bucket_name
        self.prefix = b''
        self.streaming = False

    def with_prefix(self, prefix):
        """ Configure the cursor with the specified prefix."""
        self.prefix = prefix
        return self

    def enable_streaming(self, streaming):
        """ Configure the cursor with the specified streaming flag."""
        self.streaming = streaming
        return self

    def seek(self, key):
        """ Seek the value in the bucket associated to the specified key."""
        request = kv_pb2.SeekRequest(bucketName=self.bucket_name, seekKey=key, prefix=self.prefix)
        request_iterator = iter([request])
        response_iterator = self.remote_kv_store.kv_stub.Seek(request_iterator)
        response = response_iterator.next()
        return response.key, response.value

    def seek_exact(self, key):
        """ Seek the value in the bucket associated to the specified key, matching key exactly."""
        rsp_key, rsp_value = self.seek(key)
        if rsp_key == key:
            value = rsp_value
        else:
            value = None
        return value

    def next(self):
        """ Get key-value streaming iterator for the bucket bound to prefix."""
        request = kv_pb2.SeekRequest(bucketName=self.bucket_name, seekKey=self.prefix, prefix=self.prefix, startSreaming=self.streaming)
        request_iterator = iter([request])
        response_iterator = self.remote_kv_store.kv_stub.Seek(request_iterator)
        return response_iterator
