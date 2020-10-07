# -*- coding: utf-8 -*-
"""The unit test for receipt module."""

import rlp

import pytest

from silksnake.rlp import receipt

# pylint: disable=line-too-long

@pytest.mark.parametrize("buffer,status,cumulative_gas_used,logs,should_pass", [
    # Valid test list
    ('c5808203e8c0', 0, 1000, (), True),
    #('dd808203e8d8d79412b731d23993eb97ba19e7c48ea6428edfd3e3e1c080', 0, 1000, (('12b731d23993eb97ba19e7c48ea6428edfd3e3e1', (), ''),), True),

    # Invalid test list
    ('c4808203e8c0', 0, 1000, (), False),
])
def test_transaction_receipt(buffer: str, status: int, cumulative_gas_used: int, logs: tuple, should_pass: bool):
    """ Unit test for receipt module. """
    buffer_bytes = bytes.fromhex(buffer) if buffer is not None else None
    if should_pass:
        receipt_instance = rlp.decode(buffer_bytes, receipt.TransactionReceipt)
        assert receipt_instance.status == status
        assert receipt_instance.cumulative_gas_used == cumulative_gas_used
        assert receipt_instance.logs == logs
    else:
        with pytest.raises((rlp.exceptions.DecodingError)):
            rlp.decode(buffer_bytes, receipt.TransactionReceipt)

@pytest.mark.parametrize("buffer,should_pass", [
    # Valid test list
    ('f90109f901060183036d16f8fff8fd9412b731d23993eb97ba19e7c48ea6428edfd3e3e1f884a0ba5de06d22af2685c6c7765f60067f7d2b08c2d29f53cdf14d67f6d1c9bfb527a0000000000000000000000000485afa8808deb85c07c1dcbc896623f67e2e7636a000000000000000000000000000000000000000000000000000000000016f4770a000000000000000000000000000000000000000000000044664c7bf6451f00000b86000000000000000000000000000000000000000000000000000000000000965360000000000000000000000000000000000000000000000000000000000096635c00fdd12a308538d70ee5ab0afef1e99d2281829f4063e767db281a28e601c92', True),

    # Invalid test list
    ('c4808203e8c0', False),
])
def test_decode_block_receipt(buffer: str, should_pass: bool):
    """ Unit test for decode_block_receipt. """
    buffer_bytes = bytes.fromhex(buffer) if buffer is not None else None
    if should_pass:
        brl_instance = receipt.decode_block_receipt(buffer_bytes)
        assert brl_instance
    else:
        with pytest.raises((rlp.exceptions.DecodingError)):
            receipt.decode_block_receipt(buffer_bytes)
