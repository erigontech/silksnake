# -*- coding: utf-8 -*-

"""The unit tests for turbo-geth/silkworm KV gRPC client."""
import unittest
import grpc
import grpc_testing

from silksnake.core.remote.proto import kv_pb2
from silksnake.core.remote.proto import kv_pb2_grpc

class KVServicerMock(kv_pb2_grpc.KVServicer):
    """The KVServicerMock class is a trivial KVServicer mock
    """
    def __init__(self):
        self.key = ''
        self.value = ''

    def set_key(self, key):
        """Sets the query key."""
        self.key = key

    def set_value(self, value):
        """Sets the query value."""
        self.value = value

    def Seek(self, request_iterator, context):
        """ The seek method under test."""
        assert request_iterator.bucketName is not None, 'bucketName is None'
        assert request_iterator.seekKey is not None, 'seekKey is None'
        assert request_iterator.prefix is not None, 'prefix is None'
        return kv_pb2.Pair(key=self.key, value=self.value)

class TestCaseKVpb2(unittest.TestCase):
    """The TestCaseKVpb2 class is the unit test case for KV gRPC interface.
    """
    def setUp(self):
        """ Setup the test env. """
        self.kv_servicer = KVServicerMock()
        desc2svc = {
            kv_pb2.DESCRIPTOR.services_by_name['KV']: self.kv_servicer
        }
        self.server = grpc_testing.server_from_dictionary(desc2svc, grpc_testing.strict_real_time())

    def test_seek(self):
        """ Unit test for seek method. """
        bucket = 'g'
        seek_key = b'\x18\x02'
        prefix = b''
        request = kv_pb2.SeekRequest(bucketName=bucket, seekKey=seek_key, prefix=prefix)

        expected_value = b'\xFF\x00\xFF'
        self.kv_servicer.set_key(seek_key)
        self.kv_servicer.set_value(expected_value)

        seek_method = self.server.invoke_unary_unary(
            method_descriptor=(
                kv_pb2.DESCRIPTOR.services_by_name['KV'].methods_by_name['Seek']
            ),
            invocation_metadata={},
            request=request,
            timeout=1
        )
        response, _, code, _ = seek_method.termination()

        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(response.key, seek_key)
        self.assertEqual(response.value, expected_value)

if __name__ == '__main__':
    unittest.main()
