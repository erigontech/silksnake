# -*- coding: utf-8 -*-
"""The Concise Binary Object Representation (CBOR) encoding/decoding for logs."""

from typing import List

import cbor2

class Log:
    """ A log entry in the transaction receipt.
    """
    @classmethod
    def from_bytes(cls, log_bytes: bytes):
        """ Decode the given bytes as log entry. """
        deserialized_log = cbor2.loads(log_bytes)
        if not deserialized_log:
            raise ValueError(f'empty deserialized log: {deserialized_log}')
        address, topics, data = deserialized_log
        return Log(address, topics, data)

    def __init__(self, address: bytes, topics: List[bytes], data: bytes):
        self.address = address.hex()
        self.topics = topics
        self.data = data

    def __str__(self) -> str:
        return f'address: {self.address} topics: {[topic.hex() for topic in self.topics]} data: {self.data.hex()}'

    def __repr__(self) -> str:
        return str(self)
