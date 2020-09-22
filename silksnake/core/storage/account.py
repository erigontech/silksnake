# -*- coding: utf-8 -*-
"""The storage encoding/decoding for accounts."""

class Account:
    """ This class represents the blockchain account.
    """
    NONCE_FIELD_MASK = 1
    BALANCE_FIELD_MASK = 2
    INCARNATION_FIELD_MASK = 4
    CODE_HASH_FIELD_MASK = 8
    STORAGE_ROOT_FIELD_MASK = 16

    @classmethod
    def from_bytes(cls, account_bytes: bytes):
        """ Create an account from serialized account_bytes."""
        if len(account_bytes) == 0:
            raise ValueError('zero length account_bytes')

        def read_next(pos: int, length: int) -> (int, bytes):
            value_bytes = account_bytes[pos + 1 : pos + length + 1]
            return pos + length + 1, value_bytes

        fieldset = account_bytes[0]
        pos = 1

        nonce = 0
        if fieldset & cls.NONCE_FIELD_MASK:
            pos, nonce_bytes = read_next(pos, account_bytes[pos])
            nonce = int.from_bytes(nonce_bytes, 'big')

        balance = 0
        if fieldset & cls.BALANCE_FIELD_MASK:
            pos, balance_bytes = read_next(pos, account_bytes[pos])
            balance = int.from_bytes(balance_bytes, 'big')

        incarnation = 0
        if fieldset & cls.INCARNATION_FIELD_MASK:
            pos, incarnation_bytes = read_next(pos, account_bytes[pos])
            incarnation = int.from_bytes(incarnation_bytes, 'big')

        storage_root = ''
        if fieldset & cls.STORAGE_ROOT_FIELD_MASK:
            pos, storage_root_bytes = read_next(pos, account_bytes[pos])
            storage_root = storage_root_bytes.hex()

        code_hash = ''
        if fieldset & cls.CODE_HASH_FIELD_MASK:
            pos, code_hash_bytes = read_next(pos, account_bytes[pos])
            code_hash = code_hash_bytes.hex()

        return Account(nonce, balance, incarnation, code_hash, storage_root)

    def __init__(self, nonce, balance, incarnation, code_hash, storage_root):
        self.nonce = nonce
        self.balance = balance
        self.incarnation = incarnation
        self.storage_root = storage_root
        self.code_hash = code_hash

    def __str__(self):
        beautify = (lambda v: v.hex() if isinstance(v, bytes) else v)
        fields = tuple('{}={!r}'.format(k, beautify(v)) for k, v in self.__dict__.items())
        return '({})'.format(", ".join(fields))
