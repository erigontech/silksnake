# -*- coding: utf-8 -*-
"""The abstract data type for Ethereum addresses."""

from ..core.constants import ADDRESS_SIZE # define SIZE here and import Address.SIZE there

class Address:
    """ Address"""

    @classmethod
    def from_hex(cls, hex_string: str):
        """ from_str """
        hex_string = hex_string[2:] if hex_string.startswith('0x') else hex_string
        return Address(bytes.fromhex(hex_string))

    def __init__(self, address_bytes: bytes(ADDRESS_SIZE)):
        if len(address_bytes) > ADDRESS_SIZE:
            address_bytes = address_bytes[len(address_bytes)-ADDRESS_SIZE:]

        self.bytes = address_bytes
