# -*- coding: utf-8 -*-
"""The unit test for remote module."""

import pytest
import pytest_mock

from silksnake.remote.proto import kv_pb2
from silksnake.remote.kv_remote import RemoteCursor, DEFAULT_PREFIX

# pylint: disable=no-self-use,redefined-outer-name

@pytest.fixture(scope='module')
def basic_cursor():
    """ cursor """
    return RemoteCursor(pytest_mock.mock.Mock(), 'T')

@pytest.fixture
def cursor(mocker: pytest_mock.MockerFixture, key_out: str, value: str):
    """ cursor2 """
    key_out_bytes = bytes.fromhex(key_out) if key_out is not None else None
    value_bytes = bytes.fromhex(value) if value is not None else None
    mock_kvstub = mocker.Mock()
    type(mock_kvstub).Seek = lambda k, p: iter([kv_pb2.Pair(key=key_out_bytes, value=value_bytes)])
    return RemoteCursor(mock_kvstub, 'T')

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
