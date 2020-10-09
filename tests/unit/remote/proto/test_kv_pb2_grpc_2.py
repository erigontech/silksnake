# -*- coding: utf-8 -*-
"""The unit tests for Key-Value (KV) gRPC client."""

import grpc
import pytest

from silksnake.remote.proto import kv_pb2
from silksnake.remote.proto import kv_pb2_grpc

# pylint: disable=redefined-outer-name

@pytest.fixture(scope='module')
def grpc_add_to_server():
    """ grpc_add_to_server """
    return kv_pb2_grpc.add_KVServicer_to_server

@pytest.fixture(scope='module')
def grpc_servicer():
    """ grpc_servicer """
    return kv_pb2_grpc.KVServicer()

@pytest.fixture(scope='module')
def grpc_stub(grpc_channel):
    """ grpc_stub """
    return kv_pb2_grpc.KVStub(grpc_channel)

def test_seek_not_implemented(grpc_stub):
    """ Unit test for seek method. """
    bucket = 'g'
    seek_key = b'\x18\x02'
    prefix = b''
    request = kv_pb2.SeekRequest(bucketName=bucket, seekKey=seek_key, prefix=prefix)

    try:
        response_iterator = grpc_stub.Seek(iter([request]))
        for response in response_iterator:
            dir(response)
        assert False
    except grpc.RpcError:
        assert response_iterator.code() == grpc.StatusCode.UNIMPLEMENTED
        assert response_iterator.details() == 'Method not implemented!'

@pytest.mark.filterwarnings("ignore:'stream_stream' is an experimental API")
def test_seek_experimental():
    """ Unit test for seek method using gRPC experimental API. """
    bucket = 'g'
    seek_key = b'\x18\x02'
    prefix = b''
    request = kv_pb2.SeekRequest(bucketName=bucket, seekKey=seek_key, prefix=prefix)

    kv_pb2_grpc.KV.Seek(iter([request]), '')
