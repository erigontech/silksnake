# -*- coding: utf-8 -*-
"""The unit test for kv_utils module."""

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
    """ Unit test for binary_search. """
    seek_key = bytes.fromhex(seek_key_hex) if seek_key_hex else None
    result = (bytes.fromhex(result_key), bytes.fromhex(result_value))
    if should_pass:
        assert kv_utils.kv_seek(bucket, seek_key, target) == result
    else:
        with pytest.raises((ValueError)):
            kv_utils.kv_seek(bucket, seek_key, target)
