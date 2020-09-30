# -*- coding: utf-8 -*-
"""The unit test for storage encoding/decoding of accounts."""

import pytest

from silksnake.core.account import Account

# pylint: disable=line-too-long,no-self-use

class TestAccount:
    """ Unit test case for Account.
    """
    @pytest.mark.parametrize("account_hex,nonce,balance,incarnation,storage_root,code_hash,should_pass", [
        # Valid test list
        ('0d010101012010b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', 1, 0, 1, '', '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', True),

        # Invalid test list
        ('', 1, 0, 1, '', '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', False),
        ('0d', 1, 0, 1, '', '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', False),
        ('0d010101013010b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', 1, 0, 1, '', '10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c', False),
    ])
    def test_from_storage(self, account_hex: str, nonce: int, balance: int, incarnation: int, storage_root: str, code_hash: str, should_pass: bool):
        """ Unit test for decode_for_storage method."""
        account_bytes = bytes.fromhex(account_hex)
        if should_pass:
            acc = Account.from_storage(account_bytes)
            assert acc.nonce == nonce
            assert acc.balance == balance
            assert acc.incarnation == incarnation
            assert acc.code_hash == code_hash
            assert acc.storage_root == storage_root
        else:
            with pytest.raises((ValueError, IndexError)):
                acc = Account.from_storage(account_bytes)

    @pytest.mark.parametrize("nonce,balance,incarnation,storage_root,code_hash,should_pass", [
        # Valid test list
        (0, 0, 0, '', '', True),

        # Invalid test list
        # (None, 0, 0, '', '', False),
    ])
    def test_init(self, nonce: int, balance: int, incarnation: int, storage_root: str, code_hash: str, should_pass: bool):
        """ Unit test for __init__."""
        if should_pass:
            acc = Account(nonce, balance, incarnation, storage_root, code_hash)
            assert acc.nonce == nonce
            assert acc.balance == balance
            assert acc.incarnation == incarnation
            assert acc.code_hash == code_hash
            assert acc.storage_root == storage_root
