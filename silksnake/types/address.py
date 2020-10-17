# -*- coding: utf-8 -*-
"""The abstract data type for Ethereum addresses."""

class Address:
    """ Represents 20-bytes Ethereum addresses. """
    SIZE = 20

    @classmethod
    def from_hex(cls, hex_string: str):
        """ Create an Address from the given hex string w or w/o 0x prefix. """
        if hex_string is None:
            raise ValueError('hex_string is null')
        hex_string = hex_string[2:] if hex_string.startswith('0x') else hex_string
        return Address(bytes.fromhex(hex_string))

    def __init__(self, address_bytes: bytes(SIZE)):
        """ Create a new Address from the right-most SIZE bytes of given bytes.
        """
        if len(address_bytes) < Address.SIZE:
            raise ValueError('address too short: expected {0} bytes, got {1}'.format(Address.SIZE, len(address_bytes)))
        if len(address_bytes) > Address.SIZE:
            address_bytes = address_bytes[len(address_bytes)-Address.SIZE:]

        self.bytes = address_bytes
