# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from silksnake.remote.proto import kv_pb2 as silksnake_dot_remote_dot_proto_dot_kv__pb2


class KVStub(object):
    """Provides methods to access key-value data
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Seek = channel.stream_stream(
                '/remote.KV/Seek',
                request_serializer=silksnake_dot_remote_dot_proto_dot_kv__pb2.SeekRequest.SerializeToString,
                response_deserializer=silksnake_dot_remote_dot_proto_dot_kv__pb2.Pair.FromString,
                )


class KVServicer(object):
    """Provides methods to access key-value data
    """

    def Seek(self, request_iterator, context):
        """open a cursor on given position of given bucket
        if streaming requested - streams all data: stops if client's buffer is full, resumes when client read enough from buffer
        if streaming not requested - streams next data only when clients sends message to bi-directional channel
        no full consistency guarantee - server implementation can close/open underlying db transaction at any time
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KVServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Seek': grpc.stream_stream_rpc_method_handler(
                    servicer.Seek,
                    request_deserializer=silksnake_dot_remote_dot_proto_dot_kv__pb2.SeekRequest.FromString,
                    response_serializer=silksnake_dot_remote_dot_proto_dot_kv__pb2.Pair.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'remote.KV', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KV(object):
    """Provides methods to access key-value data
    """

    @staticmethod
    def Seek(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/remote.KV/Seek',
            silksnake_dot_remote_dot_proto_dot_kv__pb2.SeekRequest.SerializeToString,
            silksnake_dot_remote_dot_proto_dot_kv__pb2.Pair.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)