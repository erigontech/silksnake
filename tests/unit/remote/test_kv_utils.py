# -*- coding: utf-8 -*-
"""The unit test for kv_utils module."""

from typing import NamedTuple

import pytest
import pytest_mock

from silksnake.remote import kv_remote
from silksnake.remote import kv_utils

# pylint: disable=line-too-long,no-self-use,unnecessary-lambda

@pytest.fixture
def mock_kv_seek(mocker: pytest_mock.MockerFixture, result_key: str, result_value: str, should_pass: bool) -> None:
    """ mock_kv_seek """
    mock_get = mocker.patch.object(kv_remote.RemoteView, 'get')
    if should_pass:
        mock_get.return_value = bytes.fromhex(result_key), bytes.fromhex(result_value)

@pytest.mark.usefixtures('mock_kv_seek')
@pytest.mark.parametrize('bucket,seek_key_hex,target,result_key,result_value,should_pass', [
    # Valid test list
    ('b', '000000000033a2db', '', '000000000033a2db05d7db38db2cecdc2a195159a02530b69b47d0ec970d5275352870769d94a618', 'c2c0c0', True),
    ('b', '', '', '', '', True),

    # Invalid test list
    (None, '000000000033a2db', '', '000000000033a2db05d7db38db2cecdc2a195159a02530b69b47d0ec970d5275352870769d94a618', 'c2c0c0', False),
    ('b', None, '', '000000000033a2db05d7db38db2cecdc2a195159a02530b69b47d0ec970d5275352870769d94a618', 'c2c0c0', False),
])
def test_kv_seek(bucket: str, seek_key_hex: str, target: str, result_key: str, result_value: str, should_pass: bool) -> None:
    """ Unit test for kv_seek. """
    seek_key = bytes.fromhex(seek_key_hex) if seek_key_hex is not None else None
    result = (bytes.fromhex(result_key), bytes.fromhex(result_value))
    if should_pass:
        assert kv_utils.kv_seek(bucket, seek_key, target) == result
    else:
        with pytest.raises((ValueError)):
            kv_utils.kv_seek(bucket, seek_key, target)

class Result(NamedTuple):
    """ Result """
    key: str
    value: str

class ResultBytes(NamedTuple):
    """ ResultBytes """
    key: bytes
    value: bytes

ResultListType = [Result]

@pytest.fixture
def mock_kv_walk(mocker: pytest_mock.MockerFixture, result_list: ResultListType, should_pass: bool) -> None:
    """ mock_kv_walk """
    mock_next = mocker.patch.object(kv_remote.RemoteCursor, 'next')
    if should_pass:
        mock_next.return_value = [ResultBytes(bytes.fromhex(result.key), bytes.fromhex(result.value)) for result in result_list]

PREFIX_1 = 'fffdbdc275633f1cbe08af0f5d132e72f0d853a0'
KEY_1 = 'fffdbdc275633f1cbe08af0f5d132e72f0d853a0ffffffffffffffff'
VALUE_1 = '000000000031ba8c800000'

@pytest.mark.usefixtures('mock_kv_walk')
@pytest.mark.parametrize('bucket,prefix_hex,target,result_list,expected_list,stop_after,should_pass', [
    # Valid test list
    ('b', '', '', [], [], -1, True),
    ('b', '', '', [], [], 0, True),
    ('b', '', '', [Result('', '')], [], -1, True),
    ('b', '', '', [Result('01', '01')], [Result('01', '01')], -1, True),
    ('b', '', '', [Result('01', '01')], [Result('01', '01')], 0, True),
    ('b', '000000000033a2db', '', [Result('01', '01')], [Result('01', '01')], -1, True),
    ('b', '000000000033a2db', '', [Result('01', '01')], [Result('01', '01')], 0, True),
    ('b', PREFIX_1, '', [Result(KEY_1, VALUE_1)], [Result(KEY_1, VALUE_1)], -1, True),
    ('b', PREFIX_1, '', [Result(KEY_1, VALUE_1)], [Result(KEY_1, VALUE_1)], 0, True),
    ('b', '', '', [Result('01', '01'), Result('02', '02')], [Result('01', '01'), Result('02', '02')], -1, True),
    ('b', '', '', [Result('01', '01'), Result('02', '02')], [Result('01', '01')], 0, True),

    # Invalid test list
    (None, '000000000033a2db', '', [Result('01', '01')], [Result('01', '01')], -1, False),
    ('b', None, '', [Result('01', '01')], [Result('01', '01')], -1, False),
])
def test_kv_walk(bucket: str, prefix_hex: str, target: str, result_list: ResultListType, expected_list: ResultListType, stop_after: int, should_pass: bool) -> None:
    """ Unit test for kv_walk. """
    assert len(result_list) >= len(expected_list), 'invalid test parameter: result_list < expected_list'
    prefix = bytes.fromhex(prefix_hex) if prefix_hex is not None else None
    mock_walker = pytest_mock.mock.Mock()
    if should_pass:
        mock_walker.return_value = stop_after >= 0
        expected_bytes_list = [ResultBytes(bytes.fromhex(expected.key), bytes.fromhex(expected.value)) for expected in expected_list]
        kv_utils.kv_walk(target, bucket, prefix, mock_walker)
        calls = [pytest_mock.mock.call(expected_bytes.key, expected_bytes.value) for expected_bytes in expected_bytes_list]
        mock_walker.assert_has_calls(calls)
    else:
        with pytest.raises((ValueError)):
            kv_utils.kv_walk(target, bucket, prefix, mock_walker)

@pytest.mark.parametrize('target,should_pass,args', [
    # Valid test list
    ('', True, {}),

    # Invalid test list
    ('', False, {}),
])
def test_kv_func(target: str, should_pass: bool, args: dict) -> None:
    """ Unit test for kv_func. """
    mock_func = pytest_mock.mock.Mock()
    if should_pass:
        kv_utils.kv_func(target, mock_func, *args)
        mock_func.assert_called_once()
    else:
        mock_func.side_effect = ValueError('')
        with pytest.raises((ValueError)):
            kv_utils.kv_func(target, mock_func, *args)
