# -*- coding: utf-8 -*-
"""The unit tests for Key-Value (KV) gRPC client."""

from typing import Iterator

import grpc
import pytest

from silksnake.remote.proto import kv_pb2
from silksnake.remote.proto import kv_pb2_grpc

# pylint: disable=redefined-outer-name

class KVServicerMock(kv_pb2_grpc.KVServicer):
    """The KVServicerMock class is a trivial KVServicer mock
    """
    def __init__(self):
        self.key = ''
        self.value = ''
        self.error = None

    def set_key(self, key: bytes):
        """Set the query key."""
        self.key = key

    def set_value(self, value: bytes):
        """Set the query value."""
        self.value = value

    def set_error(self, error: Exception):
        """Set the error to raise."""
        self.error = error

    def Seek(self, request_iterator: Iterator[kv_pb2.SeekRequest], context: grpc.ServicerContext):
        """ The seek method under test."""
        if self.error:
            raise self.error
        request = request_iterator.next()
        assert request.bucketName is not None, 'bucketName is None'
        assert request.seekKey is not None, 'seekKey is None'
        assert request.prefix is not None, 'prefix is None'
        return iter([kv_pb2.Pair(key=self.key, value=self.value)])

@pytest.fixture(scope='module')
def grpc_add_to_server():
    """ grpc_add_to_server """
    return kv_pb2_grpc.add_KVServicer_to_server

@pytest.fixture(scope='module')
def grpc_servicer():
    """ grpc_servicer """
    return KVServicerMock()

@pytest.fixture(scope='module')
def grpc_stub(grpc_channel):
    """ grpc_stub """
    return kv_pb2_grpc.KVStub(grpc_channel)

def test_seek(grpc_stub, grpc_servicer):
    """ Unit test for seek method. """
    bucket = 'g'
    seek_key = b'\x18\x02'
    prefix = b''
    request = kv_pb2.SeekRequest(bucketName=bucket, seekKey=seek_key, prefix=prefix)

    expected_value = b'\xFF\x00\xFF'
    grpc_servicer.set_key(seek_key)
    grpc_servicer.set_value(expected_value)

    response_iterator = grpc_stub.Seek(iter([request]))
    for response in response_iterator:
        assert response.key == seek_key
        assert response.value == expected_value

def test_seek_runtime_error(grpc_stub, grpc_servicer):
    """ Unit test for seek method. """
    bucket = 'g'
    seek_key = b'\x18\x02'
    prefix = b''
    request = kv_pb2.SeekRequest(bucketName=bucket, seekKey=seek_key, prefix=prefix)

    grpc_servicer.set_error(RuntimeError('error during seek'))

    try:
        response_iterator = grpc_stub.Seek(iter([request]))
        for response in response_iterator:
            dir(response)
        assert False
    except grpc.RpcError:
        assert response_iterator.code() == grpc.StatusCode.UNKNOWN
        assert response_iterator.details() == 'Exception calling application: error during seek'
