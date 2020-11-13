# -*- coding: utf-8 -*-
"""The unit test for receipt module."""

from typing import List

import cbor2

import pytest

from silksnake.db.cbor import log, receipt

# pylint: disable=line-too-long,no-self-use

class TestTransactionReceipt:
    """TestTransactionReceipt"""

    @pytest.mark.parametrize("post_state,status,cumulative_gas_used,logs,should_pass", [
        # Valid test list
        ('', 0, 1000, [], True),
        ('dd808203e8d8d79412b731d23993eb97ba19e7c48ea6428edfd3e3e1c080', 0, 1000, (('12b731d23993eb97ba19e7c48ea6428edfd3e3e1', [], ''),), True),

        # Invalid test list
        #('10', 0, 1000, [], False),
    ])
    def test_init(self, post_state: str, status: int, cumulative_gas_used: int, logs: List[log.Log], should_pass: bool):
        """Unit test for __init__. """
        post_state_bytes = bytes.fromhex(post_state) if post_state is not None else None
        if should_pass:
            receipt_instance = receipt.TransactionReceipt(post_state_bytes, status, cumulative_gas_used, logs)
            assert receipt_instance.post_state == post_state_bytes
            assert receipt_instance.status == status
            assert receipt_instance.cumulative_gas_used == cumulative_gas_used
            assert receipt_instance.logs == logs
            assert len(str(receipt_instance)) > 0
            assert len(repr(receipt_instance)) > 0
        else:
            with pytest.raises((ValueError)):
                receipt.TransactionReceipt(post_state_bytes, status, cumulative_gas_used, logs)

    @pytest.mark.parametrize("buffer,should_pass", [
        # Valid test list
        ('8184f6011a00036d1681835412b731d23993eb97ba19e7c48ea6428edfd3e3e1845820ba5de06d22af2685c6c7765f60067f7d\
            2b08c2d29f53cdf14d67f6d1c9bfb5275820000000000000000000000000485afa8808deb85c07c1dcbc896623f67e2e76365820000000\
                00000000000000000000000000000000000000000000000000016f4770582000000000000000000000000000000000000000000000\
                    044664c7bf6451f00000586000000000000000000000000000000000000000000000000000000000000965360000000000000000\
                        000000000000000000000000000000000000000000096635c00fdd12a308538d70ee5ab0afef1e99d2281829f4063e767db281a28e601c92'
        , True),
        ('f6', True),
        ('8184f60019a05ff6', True),

        # Invalid test list
        (None, False),
        ('', False),
        ('c480', False),
    ])
    def test_from_bytes(self, buffer: str, should_pass: bool):
        """ Unit test for decode_block_receipt. """
        buffer_bytes = bytes.fromhex(buffer) if buffer is not None else None
        if should_pass:
            brl_instance = receipt.TransactionReceipt.from_bytes(buffer_bytes)
            assert brl_instance is not None
        else:
            with pytest.raises((cbor2.CBORDecodeError, SystemError)):
                receipt.TransactionReceipt.from_bytes(buffer_bytes)
