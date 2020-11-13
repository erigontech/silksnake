# -*- coding: utf-8 -*-
"""The unit test for kv_metadata module."""

from typing import List

import pytest

from silksnake.remote import kv_metadata

# pylint: disable=line-too-long,no-self-use,unnecessary-lambda

@pytest.mark.parametrize('account_address,encoded_account_address,should_pass', [
    # Valid test list
    ('0x0828D0386C1122E565f07DD28c7d1340eD5B3315', b'\x08(\xd08l\x11"\xe5e\xf0}\xd2\x8c}\x13@\xed[3\x15', True),
    ('0828D0386C1122E565f07DD28c7d1340eD5B3315', b'\x08(\xd08l\x11"\xe5e\xf0}\xd2\x8c}\x13@\xed[3\x15', True),

    # Invalid test list
    (None, b'\x08(\xd08l\x11"\xe5e\xf0}\xd2\x8c}\x13@\xed[3\x15', False),
    ('', b'\x08(\xd08l\x11"\xe5e\xf0}\xd2\x8c}\x13@\xed[3\x15', False),
    ('00828D0386C1122E565f07DD28c7d1340eD5B3315', b'\x08(\xd08l\x11"\xe5e\xf0}\xd2\x8c}\x13@\xed[3\x15', False),
    ('x0828D0386C1122E565f07DD28c7d1340eD5B3315', b'\x08(\xd08l\x11"\xe5e\xf0}\xd2\x8c}\x13@\xed[3\x15', False),
    ('828D0386C1122E565f07DD28c7d1340eD5B3315', b'\x08(\xd08l\x11"\xe5e\xf0}\xd2\x8c}\x13@\xed[3\x15', False),
])
def test_encode_account_address(account_address: str, encoded_account_address: bytes, should_pass: bool) -> None:
    """ Unit test for encode_account_address. """
    if should_pass:
        account_address_bytes = kv_metadata.encode_account_address(account_address)
        assert account_address_bytes == encoded_account_address
    else:
        with pytest.raises((AttributeError, ValueError)):
            kv_metadata.encode_account_address(account_address)

@pytest.mark.parametrize('account_address,block_number,account_history_key_hex,should_pass', [
    # Valid test list
    ('0x0828D0386C1122E565f07DD28c7d1340eD5B3315', 1034567, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', True),
    ('0828D0386C1122E565f07DD28c7d1340eD5B3315', 1034567, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', True),

    # Invalid test list
    (None, 1034567, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', False),
    ('', 1034567, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', False),
    ('00828D0386C1122E565f07DD28c7d1340eD5B3315', 1034567, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', False),
    ('x0828D0386C1122E565f07DD28c7d1340eD5B3315', 1034567, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', False),
    ('828D0386C1122E565f07DD28c7d1340eD5B3315', 1034567, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', False),

    ('0828D0386C1122E565f07DD28c7d1340eD5B3315', -1, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', False),
    ('0828D0386C1122E565f07DD28c7d1340eD5B3315', 1000000000000000000000000000000000000000, '0828d0386c1122e565f07dd28c7d1340ed5b331500000000000fc947', False),
])
def test_encode_account_history_key(account_address: str, block_number: int, account_history_key_hex: str, should_pass: bool) -> None:
    """ Unit test for encode_account_history_key. """
    account_history_key = bytes.fromhex(account_history_key_hex) if account_history_key_hex is not None else None
    if should_pass:
        account_address_bytes = kv_metadata.encode_account_history_key(account_address, block_number)
        assert account_address_bytes == account_history_key
    else:
        with pytest.raises((OverflowError, ValueError)):
            kv_metadata.encode_account_history_key(account_address, block_number)

@pytest.mark.parametrize('address_list_hex,address_list,should_pass', [
    # Valid test list
    ('', [], True),
    ('0828D0386C1122E565f07DD28c7d1340eD5B3315', ['0828D0386C1122E565f07DD28c7d1340eD5B3315'], True),
    ('0828D0386C1122E565f07DD28c7d1340eD5B3315A3Ce768F041d136E8d57fD24372E5fB510b797ec', ['0828D0386C1122E565f07DD28c7d1340eD5B3315', 'A3Ce768F041d136E8d57fD24372E5fB510b797ec'], True),

    # Invalid test list
    (None, [], False),
    ('28D0386C1122E565f07DD28c7d1340eD5B3315', ['0828D0386C1122E565f07DD28c7d1340eD5B3315'], False),
    ('0828D0386C1122E565f07DD28c7d1340eD5B3315A3Ce768F041d136E8d57fD24372E5fB510b797', ['0828D0386C1122E565f07DD28c7d1340eD5B3315', 'A3Ce768F041d136E8d57fD24372E5fB510b797ec'], False),
])
def test_decode_account_address_list(address_list_hex: str, address_list: List[str], should_pass: bool) -> None:
    """ Unit test for decode_account_address_list. """
    address_list_bytes = bytes.fromhex(address_list_hex) if address_list_hex is not None else None
    if should_pass:
        account_address_list = kv_metadata.decode_account_address_list(address_list_bytes)
        assert account_address_list == [bytes.fromhex(address) for address in address_list]
    else:
        with pytest.raises((TypeError, ValueError)):
            kv_metadata.decode_account_address_list(address_list_bytes)
