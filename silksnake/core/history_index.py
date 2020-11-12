# -*- coding: utf-8 -*-
"""Some useful indeces of the chain data history."""

from ..helpers import algo
from .constants import ADDRESS_SIZE, BLOCK_NUMBER_SIZE, HASH_SIZE

def index_chunck_key(key: bytes, block_number: int) -> bytes:
    """ current_chunck_key"""
    key_length = len(key)

    if key_length == ADDRESS_SIZE: # Plain State, accounts
        chunck_key_bytes = bytearray(ADDRESS_SIZE + BLOCK_NUMBER_SIZE)
        chunck_key_bytes[:ADDRESS_SIZE] = key
        chunck_key_bytes[ADDRESS_SIZE:] = block_number.to_bytes(8, 'big')
    elif key_length == HASH_SIZE: # Hashed State, accounts
        chunck_key_bytes = bytearray(HASH_SIZE + BLOCK_NUMBER_SIZE)
        chunck_key_bytes[:HASH_SIZE] = key
        chunck_key_bytes[HASH_SIZE:] = block_number.to_bytes(8, 'big')
    elif key_length == HASH_SIZE*2 + BLOCK_NUMBER_SIZE: # Hashed State, storage
        chunck_key_bytes = bytearray(HASH_SIZE*2 + BLOCK_NUMBER_SIZE)
        chunck_key_bytes[:HASH_SIZE] = key[:HASH_SIZE]
        chunck_key_bytes[HASH_SIZE:] = key[HASH_SIZE+BLOCK_NUMBER_SIZE:]
        chunck_key_bytes[HASH_SIZE*2:] = block_number.to_bytes(8, 'big')
    elif key_length == ADDRESS_SIZE + HASH_SIZE + BLOCK_NUMBER_SIZE: # Plain State, storage
        chunck_key_bytes = bytearray(ADDRESS_SIZE + HASH_SIZE + BLOCK_NUMBER_SIZE)
        chunck_key_bytes[:ADDRESS_SIZE] = key[:ADDRESS_SIZE]
        chunck_key_bytes[ADDRESS_SIZE:] = key[ADDRESS_SIZE+BLOCK_NUMBER_SIZE:]
        chunck_key_bytes[ADDRESS_SIZE+HASH_SIZE:] = block_number.to_bytes(8, 'big')
    else:
        raise ValueError('invalid key length {}'.format(key_length))

    return bytes(chunck_key_bytes)

def current_chunck_key(key: bytes) -> bytes:
    """ current_chunck_key"""
    return index_chunck_key(key, ~int(0))

ITEM_LENGTH = 3
MIN_CHUNCK_SIZE = 8
MAX_CHUNCK_SIZE = 1000

class HistoryIndex:
    """ HistoryIndex."""
    def __init__(self, buffer: bytes = bytearray(8)):
        self.buffer = buffer
        assert len(self.buffer) >= MIN_CHUNCK_SIZE, 'length is too small'
        assert (len(self.buffer) - MIN_CHUNCK_SIZE) % ITEM_LENGTH == 0, 'length is not 8 mod ITEM_LENGTH'

    def length(self) -> int:
        """ length"""
        return (len(self.buffer) - MIN_CHUNCK_SIZE) // ITEM_LENGTH

    def truncate_greater(self, lower: int) -> bytes:
        """ truncateGreater"""
        assert len(self.buffer) >= MIN_CHUNCK_SIZE, 'length is too small'
        assert (len(self.buffer) - MIN_CHUNCK_SIZE) % ITEM_LENGTH == 0, 'length is not 8 mod ITEM_LENGTH'

        num_elements = (len(self.buffer) - MIN_CHUNCK_SIZE) // ITEM_LENGTH
        min_element = int.from_bytes(self.buffer[:MIN_CHUNCK_SIZE], 'big')
        elements = self.buffer[MIN_CHUNCK_SIZE:]
        def greater_than_lower(i: int) -> bool:
            offset = i * ITEM_LENGTH
            return lower < min_element + (int(elements[offset]&0x7f)<<16) + (int(elements[offset+1])<<8) + int(elements[offset+2])

        truncation_point = algo.binary_search(0, num_elements, greater_than_lower)

        return self.buffer[:MIN_CHUNCK_SIZE + truncation_point*ITEM_LENGTH]

    def search(self, value: int) -> (int, bool, bool):
        """ Search looks for the element which is equal or greater of given value. """
        assert len(self.buffer) >= MIN_CHUNCK_SIZE, 'length is too small'
        assert (len(self.buffer) - MIN_CHUNCK_SIZE) % ITEM_LENGTH == 0, 'length is not 8 mod ITEM_LENGTH'

        num_elements = (len(self.buffer) - MIN_CHUNCK_SIZE) // ITEM_LENGTH
        min_element = int.from_bytes(self.buffer[:MIN_CHUNCK_SIZE], 'big')
        elements = self.buffer[MIN_CHUNCK_SIZE:]

        def greater_than_or_equal_value(i: int) -> bool:
            offset = i * ITEM_LENGTH
            return value <= min_element + (int(elements[offset]&0x7f)<<16) + (int(elements[offset+1])<<8) + int(elements[offset+2])
        idx = algo.binary_search(0, num_elements, greater_than_or_equal_value) * ITEM_LENGTH
        if idx == len(elements):
            return 0, False, False

        found_element = min_element + (int(elements[idx]&0x7f)<<16) + (int(elements[idx+1])<<8) + int(elements[idx+2])
        return found_element, (elements[idx]&0x80) != 0, True

    def element(self, i: int) -> (int, bool, bool):
        """ last_element"""
        num_elements = (len(self.buffer) - MIN_CHUNCK_SIZE) // ITEM_LENGTH
        if i < 0 or i >= num_elements:
            return 0, False, False
        min_element = int.from_bytes(self.buffer[:MIN_CHUNCK_SIZE], 'big')
        elements = self.buffer
        idx = MIN_CHUNCK_SIZE + i * ITEM_LENGTH
        ith_element = min_element + (int(elements[idx]&0x7f)<<16) + (int(elements[idx+1])<<8) + int(elements[idx+2])
        return ith_element, (elements[idx]&0x80) != 0, True

    def last_element(self) -> (int, bool, bool):
        """ last_element"""
        num_elements = (len(self.buffer) - MIN_CHUNCK_SIZE) // ITEM_LENGTH
        if num_elements == 0:
            return 0, False, False
        min_element = int.from_bytes(self.buffer[:MIN_CHUNCK_SIZE], 'big')
        elements = self.buffer
        idx = MIN_CHUNCK_SIZE + (num_elements-1) * ITEM_LENGTH
        found_element = min_element + (int(elements[idx]&0x7f)<<16) + (int(elements[idx+1])<<8) + int(elements[idx+2])
        return found_element, (elements[idx]&0x80) != 0, True

    def chunck_key(self, key: bytes):
        """ chunck_key"""
        block_number = self.last_element()
        return index_chunck_key(key, block_number) if block_number is not None else None
