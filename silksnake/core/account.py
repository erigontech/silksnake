# -*- coding: utf-8 -*-
"""The storage encoding/decoding for accounts."""

import enum

class AccountFieldSet(enum.IntFlag):
    """ This class represents the account fields.
    """
    NONCE = 1
    BALANCE = 2
    INCARNATION = 4
    CODE_HASH = 8
    STORAGE_ROOT = 16

class Account:
    """ This class represents the blockchain account.
    """
    @classmethod
    def from_storage(cls, account_bytes: bytes):
        """ Create an account from serialized account_bytes."""
        if len(account_bytes) == 0:
            raise ValueError('zero length account_bytes')

        def read_next(pos: int, length: int) -> (int, bytes):
            value_bytes = account_bytes[pos + 1 : pos + length + 1]
            value_length = len(value_bytes)
            if value_length != length:
                raise ValueError('expected length ' + str(length) + ', actual ' + str(value_length))
            return pos + length + 1, value_bytes

        fieldset = AccountFieldSet(account_bytes[0])
        pos = 1

        nonce = 0
        if fieldset & AccountFieldSet.NONCE:
            pos, nonce_bytes = read_next(pos, account_bytes[pos])
            nonce = int.from_bytes(nonce_bytes, 'big')

        balance = 0
        if fieldset & AccountFieldSet.BALANCE:
            pos, balance_bytes = read_next(pos, account_bytes[pos])
            balance = int.from_bytes(balance_bytes, 'big')

        incarnation = 0
        if fieldset & AccountFieldSet.INCARNATION:
            pos, incarnation_bytes = read_next(pos, account_bytes[pos])
            incarnation = int.from_bytes(incarnation_bytes, 'big')

        storage_root = ''
        if fieldset & AccountFieldSet.STORAGE_ROOT:
            pos, storage_root_bytes = read_next(pos, account_bytes[pos])
            storage_root = storage_root_bytes.hex()

        code_hash = ''
        if fieldset & AccountFieldSet.CODE_HASH:
            pos, code_hash_bytes = read_next(pos, account_bytes[pos])
            code_hash = code_hash_bytes.hex()

        return Account(nonce, balance, incarnation, storage_root, code_hash)

    def __init__(self, nonce: int, balance: int, incarnation: int, storage_root: str, code_hash: str):
        self.nonce = nonce
        self.balance = balance
        self.incarnation = incarnation
        self.storage_root = storage_root
        self.code_hash = code_hash

    def __str__(self):
        beautify = (lambda v: v.hex() if isinstance(v, bytes) else v)
        fields = tuple('{}={!r}'.format(k, beautify(v)) for k, v in self.__dict__.items())
        return '({})'.format(", ".join(fields))
