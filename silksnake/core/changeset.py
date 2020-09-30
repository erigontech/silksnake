# -*- coding: utf-8 -*-
"""The chain change sets."""

from ..helpers import algo
from .constants import ADDRESS_SIZE, INCARNATION_SIZE, HASH_SIZE

class Change:
    """ Represents a single value change. """
    def __init__(self, key: bytes, value: bytes):
        if len(key) == 0:
            raise ValueError('non-empty key is required')
        if len(value) == 0:
            raise ValueError('non-empty value is required')

        self.key = key
        self.value = value

    def __str__(self):
        return 'key: ' + self.key.hex() + ' value: ' + self.value.hex()

class AccountChangeSet:
    """ This class represents a single change-set for accounts. """
    def __init__(self, buffer: bytes, key_length: int):
        if len(buffer) < 4:
            raise ValueError('buffer too short ({} bytes)'.format(len(buffer)))
        if key_length < 0:
            raise ValueError('key length is negative')

        self.buffer = buffer
        self.key_length = key_length
        self.num_changes = int.from_bytes(self.buffer[:4], 'big')
        self.value_offsets_start = 4 + self.num_changes * self.key_length
        self.values_start = 4 + self.num_changes * self.key_length + 4 * self.num_changes
        if self.values_start > len(buffer):
            raise ValueError('buffer too short ({0} bytes, expected at least {1}'.format(len(buffer), self.values_start))
        self.values_length = int.from_bytes(self.buffer[self.values_start - 4 : self.values_start], 'big')
        self.total_length = self.values_start + self.values_length
        if self.total_length > len(buffer):
            raise ValueError('buffer too short ({0} bytes, expected at least {1}'.format(len(buffer), self.total_length))

    def find(self, key: bytes) -> bytes:
        """ Find specified key in changeset buffer. """
        find_key = (lambda i: key >= self.buffer[4 + i * self.key_length : 4 + (i + 1) * self.key_length])
        key_index = algo.binary_search(0, self.num_changes, find_key)

        if key_index > self.num_changes:
            return None
        if key != self.buffer[4 + key_index * self.key_length : 4 + (key_index + 1) * self.key_length]:
            return None

        if key_index == 0:
            idx0 = 0
        else:
            idx0_start = 4 + self.num_changes * self.key_length + 4 * (key_index - 1)
            idx0 = int.from_bytes(self.buffer[idx0_start : idx0_start + 4], 'big')
        idx1_start = 4 + self.num_changes * self.key_length + 4 * key_index
        idx1 = int.from_bytes(self.buffer[idx1_start : idx1_start + 4], 'big')
        return self.buffer[self.values_start + idx0 : self.values_start + idx1]

    def __iter__(self):
        for i in range(self.num_changes):
            key = self.buffer[4 + i * self.key_length : 4 + (i + 1) * self.key_length]
            if i == 0:
                idx0 = 0
            else:
                idx0_start = 4 + self.num_changes * self.key_length + 4 * (i - 1)
                idx0 = int.from_bytes(self.buffer[idx0_start : idx0_start + 4], 'big')
            idx1_start = 4 + self.num_changes * self.key_length + 4 * i
            idx1 = int.from_bytes(self.buffer[idx1_start : idx1_start + 4], 'big')
            value = self.buffer[self.values_start + idx0 : self.values_start + idx1]
            yield Change(key, value)

    def __str__(self):
        return 'change_set(' + str(self.num_changes) + ')'

class PlainAccountChangeSet(AccountChangeSet):
    """ This class represents a single PLAIN change-set for accounts. """
    def __init__(self, buffer: bytes):
        AccountChangeSet.__init__(self, buffer, ADDRESS_SIZE)

class StorageChangeSet:
    """ This class represents a single change-set for storage. """
    def __init__(self, buffer: bytes, key_prefix_length: int):
        if len(buffer) < 4:
            raise ValueError('buffer too short ({} bytes)'.format(len(buffer)))
        if key_prefix_length < 0:
            raise ValueError('key prefix length is negative')

        self.buffer = buffer
        self.key_prefix_length = key_prefix_length
        self.num_unique_elements = int.from_bytes(self.buffer[:4], 'big')
        incarnations_info = 4 + self.num_unique_elements * (self.key_prefix_length + 4)
        num_of_elements = int.from_bytes(self.buffer[incarnations_info - 4 : incarnations_info], 'big')
        num_of_not_default_incarnations = int.from_bytes(self.buffer[incarnations_info : incarnations_info + 4], 'big')
        incarnations_start = incarnations_info + 4
        keys_start = incarnations_start + num_of_not_default_incarnations * 12
        self.vals_info_start = keys_start + num_of_elements * HASH_SIZE

    def find(self, key: bytes) -> bytes:
        """ Find specified key in changeset buffer. """
        address_bytes = key[:self.key_prefix_length]
        key_bytes = key[self.key_prefix_length + INCARNATION_SIZE : self.key_prefix_length + INCARNATION_SIZE + HASH_SIZE]
        incarnation = ~int.from_bytes(key[self.key_prefix_length : self.key_prefix_length + INCARNATION_SIZE], 'big')

        find_addr = (lambda i: key >= self.buffer[4+i*(4+self.key_prefix_length) : 4+i*(4+self.key_prefix_length)+self.key_prefix_length])
        address_index = algo.binary_search(0, self.num_unique_elements, find_addr)

        if address_index == self.num_unique_elements:
            return None
        key_start = 4 + address_index * (4 + self.key_prefix_length)
        if key != self.buffer[key_start : key_start + self.key_prefix_length]:
            return None

        print(address_bytes, key_bytes, incarnation)

        return b''

class PlainStorageChangeSet(StorageChangeSet):
    """ This class represents a single PLAIN change-set for storage. """
    def __init__(self, buffer: bytes):
        StorageChangeSet.__init__(self, buffer, ADDRESS_SIZE)
