# -*- coding: utf-8 -*-
"""The unit test for account module."""

import pytest

from silksnake.core.account import Account

# pylint: disable=line-too-long,no-self-use

PARAMETERS_STRING = 'account_hex,nonce,balance,incarnation,code_hash,storage_root,should_pass'
PARAMETERS_LIST = [
    # Valid test list
    # 0) empty
    ('00', 0, 0, 0, '', '', True),

    # 1) nonce
    #('0100', 0, 0, 0, '', '', True),
    #('010100', 0, 0, 0, '', '', True),
    ('010101', 1, 0, 0, '', '', True),

    # 2) balance
    #('0200', 0, 0, 0, '', '', True),
    #('020100', 0, 0, 0, '', '', True),
    ('020101', 0, 1, 0, '', '', True),
    ('0204017f4abe', 0, 25119422, 0, '', '', True),

    # 3) nonce+balance
    #('030000', 0, 0, 0, '', '', True),
    ('0301010101', 1, 1, 0, '', '', True),

    # 4) incarnation
    #('0400', 0, 0, 0, '', '', True),
    ('040101', 0, 0, 1, '', '', True),

    # 5) nonce+incarnation
    #('050000', 0, 0, 0, '', '', True),
    #('0501010100', 1, 0, 0, '', '', True),
    ('0501010101', 1, 0, 1, '', '', True),

    # 6) balance+incarnation
    #('060000', 0, 0, 0, '', '', True),
    #('0604017f4abe0100', 0, 25119422, 0, '', '', True),
    ('0604017f4abe0101', 0, 25119422, 1, '', '', True),

    # 7) nonce+balance+incarnation
    #('07000000', 0, 0, 0, '', '', True),
    #('07010104017f4abe0100', 1, 25119422, 0, '', '', True),
    ('07010104017f4abe0101', 1, 25119422, 1, '', '', True),

    # 8) code_hash
    #('0800', 0, 0, 0, '', '', True),
    ('0820de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 0, 0, 0, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),

    # 9) nonce+code_hash
    #('090000', 0, 0, 0, '', '', True),
    #('090020de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 0, 0, 0, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),
    ('09010120de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 1, 0, 0, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),

    # 10) balance+code_hash
    #('0a0000', 0, 0, 0, '', '', True),
    #('0a0020de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 0, 0, 0, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),
    ('0a04017f4abe20de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 0, 25119422, 0, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),

    # 11) nonce+balance+code_hash
    #('0b000000', 0, 0, 0, '', '', True),
    ('0b0101010120de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 1, 1, 0, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),

    # 12) incarnation+code_hash
    #('0c0000', 0, 0, 0, '', '', True),
    ('0c01012010b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', 0, 0, 1, '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', '', True),

    # 13) nonce+incarnation+code_hash
    #('0d000000', 0, 0, 0, '', '', True),
    #('0d010001012010b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', 0, 0, 1, '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', '', True),
    ('0d010101012010b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', 1, 0, 1, '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', '', True),

    # 14) balance+incarnation+code_hash
    #('0e000000', 0, 0, 0, '', '', True),
    #('0e00010120de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 0, 0, 1, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),
    ('0e04017f4abe010120de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 0, 25119422, 1, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),

    # 15) nonce+balance+incarnation+code_hash
    #('0f00000000', 0, 0, 0, '', '', True),
    #('0f010200010120de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 2, 0, 1, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),
    ('0f010304017f4abe010120de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 3, 25119422, 1, 'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '', True),

    # Invalid test list
    ('', 1, 0, 1, '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', '', False),
    ('0d', 1, 0, 1, '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', '', False),
    ('0d010101013010b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', 1, 0, 1, '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', '', False),
]

class TestAccount:
    """ Unit test case for Account.
    """
    @pytest.mark.parametrize(PARAMETERS_STRING, PARAMETERS_LIST)
    def test_from_storage(self, account_hex: str, nonce: int, balance: int, incarnation: int, code_hash: str, storage_root: str, should_pass: bool):
        """ Unit test for decode_from_storage method."""
        account_bytes = bytes.fromhex(account_hex)
        if should_pass:
            acc = Account.from_storage(account_bytes)
            assert acc.nonce == nonce
            assert acc.balance == balance
            assert acc.incarnation == incarnation
            assert acc.code_hash == code_hash
            assert acc.storage_root == storage_root
            assert str(acc)
        else:
            with pytest.raises((ValueError, IndexError)):
                acc = Account.from_storage(account_bytes)

    @pytest.mark.parametrize("nonce,balance,incarnation,code_hash,storage_root,should_pass", [
        # Valid test list
        (0, 0, 0, '', '', True),

        # Invalid test list
        # (None, 0, 0, '', '', False),
    ])
    def test_init(self, nonce: int, balance: int, incarnation: int, code_hash: str, storage_root: str, should_pass: bool):
        """ Unit test for __init__. """
        if should_pass:
            acc = Account(nonce, balance, incarnation, code_hash, storage_root)
            assert acc.nonce == nonce
            assert acc.balance == balance
            assert acc.incarnation == incarnation
            assert acc.code_hash == code_hash
            assert acc.storage_root == storage_root

    @pytest.mark.parametrize(PARAMETERS_STRING, PARAMETERS_LIST)
    def test_to_storage(self, account_hex: str, nonce: int, balance: int, incarnation: int, code_hash: str, storage_root: str, should_pass: bool):
        """ Unit test for to_storage method."""
        account_bytes = bytes.fromhex(account_hex)
        acc = Account(nonce, balance, incarnation, code_hash, storage_root)
        if should_pass:
            data = bytearray(acc.length_for_storage())
            assert len(data) == len(account_bytes)
            acc.to_storage(data)
            assert bytes(data) == account_bytes
        elif len(account_bytes) != acc.length_for_storage():
            data = bytearray(len(account_bytes))
            with pytest.raises((ValueError)):
                acc.to_storage(data)
