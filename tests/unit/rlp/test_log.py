# -*- coding: utf-8 -*-
"""The unit test for hashing module."""

import rlp

import pytest

from silksnake.rlp import log

# pylint: disable=line-too-long

@pytest.mark.parametrize("buffer,address,topics,data,should_pass", [
    # Valid test list
    ('d79412b731d23993eb97ba19e7c48ea6428edfd3e3e1c080', '12b731d23993eb97ba19e7c48ea6428edfd3e3e1', (), '', True),
    ('f8389412b731d23993eb97ba19e7c48ea6428edfd3e3e1e1a0000000000000000000000000000000000000000000000000000000000001efb680', '12b731d23993eb97ba19e7c48ea6428edfd3e3e1', (126902,), '', True),
    ('f85a9412b731d23993eb97ba19e7c48ea6428edfd3e3e1f842a0000000000000000000000000000000000000000000000000000000000001efb6a0000000000000000000000000000000000000000000000000000000000000000280', '12b731d23993eb97ba19e7c48ea6428edfd3e3e1', (126902, 2), '', True),

    # Invalid test list
    (None, '', (), '', False),
    ('', '12b731d23993eb97ba19e7c48ea6428edfd3e3e1', (), '', False),
    ('9412b731d23993eb97ba19e7c48ea6428edfd3e3e1c080', '12b731d23993eb97ba19e7c48ea6428edfd3e3e1', (), '', False),
])
def test_log(buffer: str, address: str, topics: tuple, data: str, should_pass: bool):
    """ Unit test for log module. """
    buffer_bytes = bytes.fromhex(buffer) if buffer is not None else None
    address_bytes = bytes.fromhex(address) if address is not None else None
    data_bytes = bytes.fromhex(data) if data is not None else None
    if should_pass:
        log_instance = rlp.decode(buffer_bytes, log.Log)
        assert log_instance.address == address_bytes
        assert log_instance.topics == topics
        assert log_instance.data == data_bytes
    else:
        with pytest.raises((rlp.exceptions.DecodingError)):
            rlp.decode(buffer_bytes, log.Log)
