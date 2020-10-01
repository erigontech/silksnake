# -*- coding: utf-8 -*-
"""The chain change sets."""

from ..helpers import algo
from .constants import ADDRESS_SIZE, INCARNATION_SIZE, HASH_SIZE

# pylint: disable=cell-var-from-loop,too-many-locals,too-many-return-statements

class Change:
    """ Represents a single value change. """
    def __init__(self, key: bytes, value: bytes):
        if len(key) == 0:
            raise ValueError('non-empty key is required')

        self.key = key
        self.value = value

    def __str__(self):
        return 'key: ' + self.key.hex() + ' value: ' + self.value.hex()

class ChangeSet:
    """ Represents a set of value changes. """
    def __init__(self):
        self.changes = set()

    def add(self, change: Change):
        """ Add given change to the set. """
        self.changes.add(change)

    def __iter__(self):
        for change in self.changes:
            yield change

    def __str__(self):
        return 'changeset(' + str(len(self.changes)) + ') '\
            + str(['key: ' + change.key.hex() + ' value: ' + change.value.hex() for change in self.changes])

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

def find_storage_value(buffer: bytes, index: int) -> bytes:
    """ find_value """
    num_of_unit8 = int.from_bytes(buffer[0 : 4], 'big')
    num_of_unit16 = int.from_bytes(buffer[4 : 8], 'big')
    num_of_unit32 = int.from_bytes(buffer[8 : 12], 'big')
    len_of_vals_start_pointer = 12
    vals_pointer = len_of_vals_start_pointer + num_of_unit8 + num_of_unit16*2 + num_of_unit32*4

    len_of_val_start = 0
    len_of_val_end = 0
    if index < num_of_unit8:
        len_of_val_end = int(buffer[len_of_vals_start_pointer+index])
        if index > 0:
            one = len_of_vals_start_pointer+index-1
            len_of_val_start = int(buffer[len_of_vals_start_pointer+index-1])
    elif index < num_of_unit8+num_of_unit16:
        one = len_of_vals_start_pointer + (index-num_of_unit8) * 2 + num_of_unit8
        len_of_val_end = int.from_bytes(buffer[one : one+2], 'big')
        if index-1 < num_of_unit8:
            len_of_val_start = int(buffer[len_of_vals_start_pointer+index-1])
        else:
            one = len_of_vals_start_pointer + (index-1)*2 - num_of_unit8
            len_of_val_start = int.from_bytes(buffer[one : one+2], 'big')
    elif index < num_of_unit8+num_of_unit16+num_of_unit32:
        one = len_of_vals_start_pointer + num_of_unit8 + num_of_unit16*2 + (index-num_of_unit8-num_of_unit16)*4
        len_of_val_end = int.from_bytes(buffer[one : one+4], 'big')
        if index-1 < num_of_unit8+num_of_unit16:
            one = len_of_vals_start_pointer + (index-1)*2 - num_of_unit8
            len_of_val_start = int.from_bytes(buffer[one : one+2], 'big')
        else:
            one = len_of_vals_start_pointer + num_of_unit8 + num_of_unit16*2 + (index-1-num_of_unit8-num_of_unit16)*4
            len_of_val_start = int.from_bytes(buffer[one : one+4], 'big')

    return buffer[vals_pointer+len_of_val_start : vals_pointer+len_of_val_end]

class StorageChangeSet:
    """ This class represents a single change-set for storage. """
    DEFAULT_INCARNATION = 1

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
        self.num_of_not_default_incarnations = int.from_bytes(self.buffer[incarnations_info : incarnations_info + 4], 'big')
        self.incarnations_start = incarnations_info + 4
        self.keys_start = self.incarnations_start + self.num_of_not_default_incarnations * 12
        self.vals_info_start = self.keys_start + num_of_elements * HASH_SIZE

    def find(self, key: bytes) -> bytes:
        """ Find specified key in changeset buffer. """
        address_to_find = key[:self.key_prefix_length]
        key_to_find = key[self.key_prefix_length + INCARNATION_SIZE : self.key_prefix_length + INCARNATION_SIZE + HASH_SIZE]
        incarnation = ~int.from_bytes(key[self.key_prefix_length : self.key_prefix_length + INCARNATION_SIZE], 'big')

        find_addr = (lambda i:\
            self.buffer[4+i*(4+self.key_prefix_length) : 4+i*(4+self.key_prefix_length)+self.key_prefix_length] >= address_to_find)
        address_index = algo.binary_search(0, self.num_unique_elements, find_addr)

        if address_index > self.num_unique_elements:
            return None
        address_start = 4 + address_index * (4 + self.key_prefix_length)
        if address_to_find != self.buffer[address_start : address_start + self.key_prefix_length]:
            return None

        if incarnation > 0:
            find_incarnation = (lambda i: int.from_bytes(\
                self.buffer[self.incarnations_start + 12 * i : self.incarnations_start + 12 * i + 4], 'big') >= address_index)
            inc_index = algo.binary_search(0, self.num_of_not_default_incarnations, find_incarnation)

            if inc_index > self.num_of_not_default_incarnations:
                return None
            incarnation_start = self.incarnations_start + 12 * inc_index
            if incarnation != self.buffer[incarnation_start : incarnation_start + 4]:
                return None

        from_index = 0
        from_index_end = 4 + address_index * (self.key_prefix_length + 4)
        if address_index > 0:
            from_index = int.from_bytes(self.buffer[from_index_end - 4 : from_index_end], 'big')
        to_index_start = from_index_end + self.key_prefix_length
        to_index = int.from_bytes(self.buffer[to_index_start : to_index_start + 4], 'big')

        find_key = (lambda i:\
            self.buffer[self.keys_start + HASH_SIZE * (from_index + i) : self.keys_start + HASH_SIZE * (from_index + i) + HASH_SIZE] >=\
                key_to_find)
        key_index = algo.binary_search(0, to_index - from_index, find_key)
        index = from_index + key_index

        if index > to_index:
            return None
        key_start = self.keys_start + HASH_SIZE * index
        if key_to_find != self.buffer[key_start : key_start + HASH_SIZE]:
            return None

        return find_storage_value(self.buffer[self.vals_info_start:], index)

    def __iter__(self):
        for i in range(self.num_unique_elements):
            address = self.buffer[4+i*(4+self.key_prefix_length) : 4+i*(4+self.key_prefix_length)+self.key_prefix_length]

            find_incarnation = (lambda j: int.from_bytes(\
                self.buffer[self.incarnations_start + 12 * j : self.incarnations_start + 12 * j + 4], 'big') >= i)
            inc_index = algo.binary_search(0, self.num_of_not_default_incarnations, find_incarnation)
            if inc_index > self.num_of_not_default_incarnations:
                incarnation = StorageChangeSet.DEFAULT_INCARNATION
            else:
                incarnation_start = self.incarnations_start + 12 * inc_index
                incarnation = int.from_bytes(self.buffer[incarnation_start : incarnation_start + 4], 'big')

            from_index = 0
            from_index_end = 4 + i * (self.key_prefix_length + 4)
            if i > 0:
                from_index = int.from_bytes(self.buffer[from_index_end - 4 : from_index_end], 'big')
            to_index_start = from_index_end + self.key_prefix_length
            to_index = int.from_bytes(self.buffer[to_index_start : to_index_start + 4], 'big')

            change_set = ChangeSet()
            for k in range(to_index - from_index):
                index = from_index + k
                key = self.buffer[self.keys_start + HASH_SIZE * index : self.keys_start + HASH_SIZE * index + HASH_SIZE]
                value = find_storage_value(self.buffer[self.vals_info_start:], index)
                change_set.add(Change(key, value))

            yield address.hex(), incarnation, change_set

    def __str__(self):
        return 'change_set(' + str(self.num_unique_elements) + ')'

class PlainStorageChangeSet(StorageChangeSet):
    """ This class represents a single PLAIN change-set for storage. """
    def __init__(self, buffer: bytes):
        StorageChangeSet.__init__(self, buffer, ADDRESS_SIZE)
