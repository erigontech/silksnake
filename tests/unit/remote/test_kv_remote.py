# -*- coding: utf-8 -*-
"""The unit test for remote module."""

import grpc

import pytest
import pytest_mock

from silksnake.remote.proto import kv_pb2
from silksnake.remote.kv_remote import RemoteClient, RemoteCursor, RemoteKV, RemoteView, SecurityOptions, DEFAULT_PREFIX, DEFAULT_TARGET

# pylint: disable=no-self-use,redefined-outer-name,unused-argument,protected-access

@pytest.fixture(scope='module')
def basic_cursor():
    """ basic_cursor """
    return RemoteCursor(pytest_mock.mock.Mock(), 'T')

@pytest.fixture
def cursor(mocker: pytest_mock.MockerFixture, key_out: str, value: str):
    """ cursor """
    key_out_bytes = bytes.fromhex(key_out) if key_out is not None else None
    value_bytes = bytes.fromhex(value) if value is not None else None
    mock_kvstub = mocker.Mock()
    type(mock_kvstub).Seek = lambda k, p: iter([kv_pb2.Pair(key=key_out_bytes, value=value_bytes)])
    return RemoteCursor(mock_kvstub, 'T')

@pytest.fixture
def file_open(mocker: pytest_mock.MockerFixture, should_pass: bool):
    """ open """
    open_name = 'builtins.open'
    mock_file_open = mocker.patch(open_name, mocker.mock_open(read_data=b'\x00'))
    if not should_pass:
        mock_file_open.side_effect = FileNotFoundError
    return mock_file_open

class TestRemoteCursor:
    """ Unit test for RemoteCursor. """
    def test_init(self):
        """ Unit test for __init__. """
        with pytest.raises(ValueError):
            RemoteCursor(None, 'b')
        with pytest.raises(ValueError):
            RemoteCursor(pytest_mock.mock.Mock(), None)

        bucket_name = 'T'
        mock_kv_stub = pytest_mock.mock.Mock()
        cursor = RemoteCursor(mock_kv_stub, bucket_name)
        assert cursor.kv_stub == mock_kv_stub
        assert cursor.bucket_name == bucket_name
        assert cursor.prefix == DEFAULT_PREFIX
        assert cursor.streaming is False

    @pytest.mark.parametrize("prefix,should_pass", [
        # Valid test list
        (DEFAULT_PREFIX, True),
        (b'\x00\x01\x02', True),

        # Invalid test list
        (None, False),
    ])
    def test_with_prefix(self, basic_cursor, prefix: str, should_pass: bool):
        """ Unit test for with_prefix. """
        prefix = prefix if prefix is not None else None
        if should_pass:
            assert basic_cursor.with_prefix(prefix).prefix == prefix
        else:
            with pytest.raises(ValueError):
                basic_cursor.with_prefix(prefix)

    @pytest.mark.parametrize("streaming,should_pass", [
        # Valid test list
        (True, True),
        (False, True),

        # Invalid test list
        (None, False),
    ])
    def test_enable_streaming(self, basic_cursor, streaming: bool, should_pass: bool):
        """ Unit test for enable_streaming. """
        streaming = streaming if streaming is not None else None
        if should_pass:
            assert basic_cursor.enable_streaming(streaming).streaming == streaming
        else:
            with pytest.raises(ValueError):
                basic_cursor.enable_streaming(streaming)

    @pytest.mark.parametrize("key_in,key_out,value,should_pass", [
        # Valid test list
        ('', '', '', True),
        ('00000000000000006e', '', '', True),
        ('00000000000000006e', '00000000000000006e', '', True),
        ('00000000000000006e', '00000000000000006e', 'c2c0c0', True),

        # Invalid test list
        (None, '', '', False),
    ])
    def test_seek(self, cursor, key_in: str, key_out: str, value: str, should_pass: bool):
        """ Unit test for seek. """
        key_in_bytes = bytes.fromhex(key_in) if key_in is not None else None
        key_out_bytes = bytes.fromhex(key_out) if key_out is not None else None
        value_bytes = bytes.fromhex(value) if value is not None else None

        if should_pass:
            assert cursor.seek(key_in_bytes) == (key_out_bytes, value_bytes)
        else:
            with pytest.raises(ValueError):
                cursor.seek(key_in_bytes)

    @pytest.mark.parametrize("key_in,key_out,value,should_pass", [
        # Valid test list
        ('', '', '', True),
        ('00000000000000006e', '', None, True),
        ('00000000000000006e', '00000000000000006e', '', True),
        ('00000000000000006e', '00000000000000006e', 'c2c0c0', True),

        # Invalid test list
        (None, '', '', False),
    ])
    def test_seek_exact(self, cursor, key_in: str, value: str, should_pass: bool):
        """ Unit test for seek_exact. """
        key_in_bytes = bytes.fromhex(key_in) if key_in is not None else None
        value_bytes = bytes.fromhex(value) if value is not None else None

        if should_pass:
            assert cursor.seek_exact(key_in_bytes) == value_bytes
        else:
            with pytest.raises(ValueError):
                cursor.seek_exact(key_in_bytes)

    @pytest.mark.parametrize("prefix,key_out,value,should_pass", [
        # Valid test list
        ('', '', '', True),
        ('00000000000000006e', '', None, True),
        ('00000000000000006e', '00000000000000006e', '', True),
        ('00000000000000006e', '00000000000000006e', 'c2c0c0', True),

        # Invalid test list
    ])
    def test_next(self, prefix: str, key_out: str, value: str, should_pass: bool):
        """ Unit test for next. """
        prefix_bytes = bytes.fromhex(prefix) if prefix is not None else None
        key_out_bytes = bytes.fromhex(key_out) if key_out is not None else None
        value_bytes = bytes.fromhex(value) if value is not None else None

        mock_kvstub = pytest_mock.mock.Mock()
        pair_iterator = iter([kv_pb2.Pair(key=key_out_bytes, value=value_bytes)])
        type(mock_kvstub).Seek = lambda k, p: pair_iterator
        cursor = RemoteCursor(mock_kvstub, 'T').with_prefix(prefix_bytes)

        if should_pass:
            assert cursor.next() == pair_iterator
            with pytest.raises(StopIteration):
                next(cursor.next())
                next(cursor.next())
        else:
            with pytest.raises(ValueError):
                cursor.next()

@pytest.fixture
def basic_view(mocker: pytest_mock.MockerFixture, key_out: str, value: str):
    """ basic_view """
    key_out_bytes = bytes.fromhex(key_out) if key_out is not None else None
    value_bytes = bytes.fromhex(value) if value is not None else None
    mock_kvstub = mocker.Mock()
    type(mock_kvstub).Seek = lambda k, p: iter([kv_pb2.Pair(key=key_out_bytes, value=value_bytes)])
    return RemoteView(mock_kvstub)

class TestRemoteView:
    """ Unit test for RemoteView. """
    def test_init(self):
        """ Unit test for __init__. """
        with pytest.raises(ValueError):
            RemoteView(None)

        mock_kv_stub = pytest_mock.mock.Mock()
        view = RemoteView(mock_kv_stub)
        assert view.kv_stub == mock_kv_stub

    @pytest.mark.parametrize("bucket_name,should_pass", [
        # Valid test list
        ('', True),
        ('T', True),

        # Invalid test list
        (None, False),
    ])
    def test_cursor(self, bucket_name: str, should_pass: bool):
        """ Unit test for cursor. """
        mock_kv_stub = pytest_mock.mock.Mock()
        view = RemoteView(mock_kv_stub)
        if should_pass:
            cursor = view.cursor(bucket_name)
            assert cursor is not None
            assert cursor.kv_stub == mock_kv_stub
            assert cursor.bucket_name == bucket_name
            assert cursor.prefix == DEFAULT_PREFIX
            assert cursor.streaming is False
        else:
            with pytest.raises(ValueError):
                view.cursor(bucket_name)

    @pytest.mark.parametrize("bucket_name,key_in,key_out,value,should_pass", [
        # Valid test list
        # ('T', '', '', '', True),
        ('T', '00000000000000006e', '', '', True),
        ('T', '00000000000000006e', '00000000000000006e', '', True),
        ('T', '00000000000000006e', '00000000000000006e', 'c2c0c0', True),

        # Invalid test list
        (None, '', '', '', False),
    ])
    def test_get(self, basic_view, bucket_name: str, key_in: str, key_out: str, value: str, should_pass: bool):
        """ Unit test for get. """
        key_in_bytes = bytes.fromhex(key_in) if key_in is not None else None
        key_out_bytes = bytes.fromhex(key_out) if key_out is not None else None
        value_bytes = bytes.fromhex(value) if value is not None else None

        if should_pass:
            assert basic_view.get(bucket_name, key_in_bytes) == (key_out_bytes, value_bytes)
        else:
            with pytest.raises(ValueError):
                basic_view.get(bucket_name, key_in_bytes)

    @pytest.mark.parametrize("bucket_name,key_in,key_out,value,should_pass", [
        # Valid test list
        ('T', '', '', '', True),
        ('T', '00000000000000006e', '00000000000000006e', '', True),
        ('T', '00000000000000006e', '00000000000000006e', 'c2c0c0', True),

        # Invalid test list
        (None, '', '', '', False),
    ])
    def test_get_exact(self, basic_view, bucket_name: str, key_in: str, key_out: str, value: str, should_pass: bool):
        """ Unit test for get_exact. """
        key_in_bytes = bytes.fromhex(key_in) if key_in is not None else None
        value_bytes = bytes.fromhex(value) if value is not None else None

        if should_pass:
            assert basic_view.get_exact(bucket_name, key_in_bytes) == value_bytes
        else:
            with pytest.raises(ValueError):
                basic_view.get_exact(bucket_name, key_in_bytes)

class TestSecurityOptions:
    """ Unit test for SecurityOptions. """
    @pytest.mark.parametrize("server_cert,client_cert,client_key,should_pass", [
        # Valid test list
        (None, None, None, True),
        ('env/ca-cert.pem', 'env/rpc.crt', 'env/rpc-key.pem', True),

        # Invalid test list
        ('', None, None, False),
        (None, '', None, False),
        (None, None, '', False),
        ('', '', '', False),
        ('', 'env/rpc.crt', 'env/rpc-key.pem', False),
        ('env/ca-cert.pem', '', 'env/rpc-key.pem', False),
        ('env/ca-cert.pem', 'env/rpc.crt', '', False),
    ])
    def test_init(self, server_cert: str, client_cert: str, client_key: str, should_pass: bool):
        """ Unit test for __init__. """
        if should_pass:
            options = SecurityOptions(server_cert, client_cert, client_key)
            assert options.server_cert == server_cert
            assert options.client_cert == client_cert
            assert options.client_key == client_key
        else:
            with pytest.raises(ValueError):
                SecurityOptions(server_cert, client_cert, client_key)

class TestRemoteKV:
    """ Unit test for RemoteKV. """
    def test_init(self):
        """ Unit test for __init__. """
        mock_channel = pytest_mock.mock.Mock()
        mock_kv_stub = pytest_mock.mock.Mock()
        remote_kv = RemoteKV(mock_channel, mock_kv_stub)
        assert remote_kv.channel == mock_channel
        assert remote_kv.kv_stub == mock_kv_stub

        with pytest.raises(ValueError):
            RemoteKV(None, mock_kv_stub)
        with pytest.raises(ValueError):
            RemoteKV(mock_channel, None)

@pytest.fixture
def basic_client():
    """ basic_client """
    return RemoteClient()

class TestRemoteClient:
    """ Unit test for RemoteClient. """
    def test_init(self):
        """ Unit test for __init__. """
        with pytest.raises(ValueError):
            RemoteClient(None, None)

        client = RemoteClient()
        assert client.target == DEFAULT_TARGET

        target = 'localhost:9090'
        client = RemoteClient(target)
        assert client.target == target

    @pytest.mark.parametrize("target,should_pass", [
        # Valid test list
        (DEFAULT_PREFIX, True),
        (b'\x00\x01\x02', True),

        # Invalid test list
        (None, False),
    ])
    def test_with_target(self, basic_client, target: str, should_pass: bool):
        """ Unit test for with_target. """
        if should_pass:
            assert basic_client.with_target(target).target == target
        else:
            with pytest.raises(ValueError):
                basic_client.with_target(target)

    def test_open_insecure(self, basic_client):
        """ Unit test for open. """
        remote_kv = basic_client.open()
        assert isinstance(remote_kv, RemoteKV)
        assert isinstance(remote_kv.channel, grpc._channel.Channel)

    @pytest.mark.parametrize("server_cert,client_cert,client_key,should_pass", [
        # Valid test list
        ('env/ca-cert.pem', 'env/rpc.crt', 'env/rpc-key.pem', True),
        ('env/ca-cert.pem', None, None, True),

        # Invalid test list
        ('env/non-existent.pem', 'env/rpc.crt', 'env/rpc-key.pem', False),
        ('env/ca-cert.pem', 'env/non-existent.crt', 'env/rpc-key.pem', False),
        ('env/ca-cert.pem', 'env/rpc.crt', 'env/non-existent.pem', False),
    ])
    def test_open_secure(self, file_open, server_cert: str, client_cert: str, client_key: str, should_pass: bool):
        """ Unit test for open. """
        if should_pass:
            client = RemoteClient(options=SecurityOptions(server_cert, client_cert, client_key))
            remote_kv = client.open()
            assert isinstance(remote_kv, RemoteKV)
            assert isinstance(remote_kv.channel, grpc._channel.Channel)
        else:
            with pytest.raises(FileNotFoundError):
                RemoteClient(options=SecurityOptions(server_cert, client_cert, client_key)).open()
