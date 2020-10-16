# -*- coding: utf-8 -*-
"""The unit test for timestamp module."""

import pytest

from silksnake.helpers.dbutils import timestamp

@pytest.mark.parametrize("value,suffix,should_pass", [
    # Valid test list
    (0, b' ', True),
    (1000000, b'oB@', True),
    (2000000, b'~\x84\x80', True),
    (123456789, b'\x87[\xcd\x15', True),

    # Invalid test list
    (-1, b'', False),
    (590295810358705651712, b'', False),
])
def test_encode_timestamp(value: int, suffix: bytes, should_pass: bool):
    """ Unit test for encode_timestamp. """
    if should_pass:
        print('value', value)
        assert timestamp.encode_timestamp(value) == suffix
    else:
        with pytest.raises(ValueError):
            timestamp.encode_timestamp(value)

@pytest.mark.parametrize("suffix,value,remaining,should_pass", [
    # Valid test list
    (b' ', 0, b'', True),
    (b'oB@', 1000000, b'', True),
    (b'~\x84\x80', 2000000, b'', True),
    (b'\x87[\xcd\x15', 123456789, b'', True),

    # Invalid test list
    (b'', -1, b'', False),
    (b'', 590295810358705651712, b'', False),
])
def test_decode_timestamp(suffix: bytes, value: int, remaining: bytes, should_pass: bool):
    """ Unit test for encode_timestamp. """
    if should_pass:
        assert timestamp.decode_timestamp(suffix) == (value, remaining)
    else:
        with pytest.raises(ValueError):
            timestamp.decode_timestamp(suffix)
