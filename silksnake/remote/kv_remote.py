# -*- coding: utf-8 -*-
"""The TurboGeth/Silkworm KV gRPC remote client."""

from typing import Iterator, NamedTuple

import grpc

from .proto import kv_pb2, kv_pb2_grpc

DEFAULT_TARGET: str = 'localhost:9090'
DEFAULT_PREFIX: str = b''

class RemoteCursor:
    """ This class represents a remote read-only cursor on the KV.
    """
    def __init__(self, kv_stub: kv_pb2_grpc.KVStub, bucket_name: str):
        if kv_stub is None:
            raise ValueError('kv_stub is null')
        if bucket_name is None:
            raise ValueError('bucket_name is null')
        self.kv_stub = kv_stub
        self.bucket_name = bucket_name
        self.prefix = DEFAULT_PREFIX
        self.streaming = False

    def with_prefix(self, prefix: bytes):
        """ Configure the cursor with the specified prefix."""
        if prefix is None:
            raise ValueError('prefix is null')
        self.prefix = prefix
        return self

    def enable_streaming(self, streaming: bool):
        """ Configure the cursor with the specified streaming flag."""
        if streaming is None:
            raise ValueError('streaming is null')
        self.streaming = streaming
        return self

    def seek(self, key: bytes) -> (bytes, bytes):
        """ Seek the value in the bucket associated to the specified key."""
        if key is None:
            raise ValueError('key is null')
        request = kv_pb2.SeekRequest(bucketName=self.bucket_name, seekKey=key, prefix=self.prefix)
        request_iterator = iter([request])
        response_iterator = self.kv_stub.Seek(request_iterator)
        response = next(response_iterator)
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
        if kv_stub is None:
            raise ValueError('kv_stub is null')
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
        if not channel:
            raise ValueError('channel is null')
        if not kv_stub:
            raise ValueError('kv_stub is null')
        self.channel = channel
        self.kv_stub = kv_stub

    def view(self) -> RemoteView:
        """ Get a read-only view on the KV."""
        return RemoteView(self.kv_stub)

    def close(self) -> None:
        """ Close the remove KV."""
        self.channel.close()

class SecurityOptions:
    """ This class represents the channel security options.
    """
    def __init__(self, server_cert: str = None, client_cert: str = None, client_key: str = None):
        if server_cert == '':
            raise ValueError('server_cert is empty')
        if client_cert == '':
            raise ValueError('client_cert is empty')
        if client_key == '':
            raise ValueError('client_key is empty')
        self.server_cert = server_cert
        self.client_cert = client_cert
        self.client_key = client_key

class RemoteClient:
    """ This class represents the remote KV client.
    """
    def __init__(self, target: str = DEFAULT_TARGET, options: SecurityOptions = SecurityOptions()):
        if not target:
            raise ValueError('target is null')
        self.target = target
        self.options = options

    def with_target(self, target: str):
        """ Configure the client to use the specified server (address:port) end point.
        """
        if target is None:
            raise ValueError('target is null')
        self.target = target
        return self

    def open(self) -> RemoteKV:
        """ Open a new remote KV store instance.
        """
        if self.options.server_cert:
            cert_chain = None
            private_key = None
            if self.options.client_cert:
                with open(self.options.client_cert, 'rb') as file:
                    cert_chain = file.read()
                with open(self.options.client_key, 'rb') as file:
                    private_key = file.read()

            with open(self.options.server_cert, 'rb') as file:
                root_cert = file.read()
            credentials = grpc.ssl_channel_credentials(root_cert, private_key, cert_chain)
            channel = grpc.secure_channel(self.target, credentials)
        else:
            channel = grpc.insecure_channel(self.target)

        kv_stub = kv_pb2_grpc.KVStub(channel)
        return RemoteKV(channel, kv_stub)
