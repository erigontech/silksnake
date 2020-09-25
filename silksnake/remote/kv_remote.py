# -*- coding: utf-8 -*-
"""The TurboGeth/Silkworm KV gRPC remote client."""

from typing import Iterator, NamedTuple

import grpc

from silksnake.remote.proto import kv_pb2, kv_pb2_grpc

DEFAULT_TARGET: str = 'localhost:9090'
DEFAULT_PREFIX: str = b''

class RemoteCursor:
    """ This class represents a remote read-only cursor on the KV.
    """
    def __init__(self, kv_stub: kv_pb2_grpc.KVStub, bucket_name: str):
        self.kv_stub = kv_stub
        self.bucket_name = bucket_name
        self.prefix = DEFAULT_PREFIX
        self.streaming = False

    def with_prefix(self, prefix: bytes):
        """ Configure the cursor with the specified prefix."""
        self.prefix = prefix
        return self

    def enable_streaming(self, streaming: bool):
        """ Configure the cursor with the specified streaming flag."""
        self.streaming = streaming
        return self

    def seek(self, key: bytes) -> (bytes, bytes):
        """ Seek the value in the bucket associated to the specified key."""
        request = kv_pb2.SeekRequest(bucketName=self.bucket_name, seekKey=key, prefix=self.prefix)
        request_iterator = iter([request])
        response_iterator = self.kv_stub.Seek(request_iterator)
        response = response_iterator.next()
        return response.key, response.value

    def seek_exact(self, key: bytes) -> bytes:
        """ Seek the value in the bucket associated to the specified key, matching key exactly."""
        rsp_key, rsp_value = self.seek(key)
        if rsp_key == key:
            value = rsp_value
        else:
            value = None
        return value

    def next(self) -> Iterator[NamedTuple('Pair', [('key', bytes), ('value', bytes)])]:
        """ Get key-value streaming iterator for the bucket bound to prefix."""
        request = kv_pb2.SeekRequest(bucketName=self.bucket_name, seekKey=self.prefix, prefix=self.prefix, startSreaming=self.streaming)
        request_iterator = iter([request])
        response_iterator = self.kv_stub.Seek(request_iterator)
        return response_iterator

class RemoteView:
    """ This class represents a remote read-only view on the KV.
    """
    def __init__(self, kv_stub: kv_pb2_grpc.KVStub):
        self.kv_stub = kv_stub

    def cursor(self, bucket_name: str) -> RemoteCursor:
        """ Create a new remote cursor on the KV."""
        return RemoteCursor(self.kv_stub, bucket_name)

    def get(self, bucket_name: str, key: bytes) -> (bytes, bytes):
        """ Get the value associated to the key in specified bucket."""
        return self.cursor(bucket_name).seek(key)

    def get_exact(self, bucket_name: str, key: bytes) -> bytes:
        """ Get the value associated to the key in specified bucket, checking exact key match."""
        return self.cursor(bucket_name).seek_exact(key)

class RemoteKV:
    """ This class represents the remote KV store.
    """
    def __init__(self, channel: grpc.Channel, kv_stub: kv_pb2_grpc.KVStub):
        self.channel = channel
        self.kv_stub = kv_stub

    def view(self) -> RemoteView:
        """ Get a read-only view on the KV."""
        return RemoteView(self.kv_stub)

    def close(self) -> None:
        """ Close the remove KV."""
        self.channel.close()

class RemoteClient:
    """ This class represents the remote KV client.
    """
    def __init__(self):
        self.target = DEFAULT_TARGET

    def with_target(self, target: str):
        """ Configure the client to use the specified server (address:port) end point.
        """
        self.target = target
        return self

    def open(self) -> RemoteKV:
        """ Open a new remote KV store instance.
        """
        channel = grpc.insecure_channel(self.target)
        kv_stub = kv_pb2_grpc.KVStub(channel)
        return RemoteKV(channel, kv_stub)
