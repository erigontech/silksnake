# -*- coding: utf-8 -*-
"""The Concise Binary Object Representation (CBOR) encoding/decoding for receipts."""

from typing import List

import cbor2

from ..cbor import log

# pylint: disable=too-many-locals

class TransactionReceipt:
    """ Transaction receipt present in block.
    """
    STATUS_OK = 1
    STATUS_KO = 0

    @classmethod
    def from_bytes(cls, block_receipt_bytes: bytes):
        """ Decode the given bytes as list of block receipts. """
        transaction_receipt_list = []
        trn_receipt_list = cbor2.loads(block_receipt_bytes)
        for trn_receipt in trn_receipt_list:
            post_state, status, cumulative_gas_used, trn_logs = trn_receipt
            log_list = []
            for trn_log in trn_logs:
                address, topics, data = trn_log
                log_instance = log.Log(address, topics, data)
                log_list.append(log_instance)
            transaction_receipt = TransactionReceipt(post_state, status, cumulative_gas_used, log_list)
            transaction_receipt_list.append(transaction_receipt)
        return transaction_receipt_list

    def __init__(self, post_state: bytes, status: int, cumulative_gas_used: int, logs: List[log.Log]):
        self.post_state = post_state
        self.status = status
        self.cumulative_gas_used = cumulative_gas_used
        self.logs = logs

    def __str__(self) -> str:
        status_str = 'SUCCESS' if self.status == TransactionReceipt.STATUS_OK else 'FAILED'
        return f'status: {status_str} cumulative_gas_used: {self.cumulative_gas_used} logs: {self.logs}'

    def __repr__(self) -> str:
        return str(self)
