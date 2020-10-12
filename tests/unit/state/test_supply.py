# -*- coding: utf-8 -*-
"""The unit test for hashing module."""

import pytest
import pytest_mock

from silksnake.state import supply

@pytest.mark.parametrize("block_number,result_key,result_value,should_pass", [
    # Valid test list
    (0, '0000000000000000', '0000000000000001', True),
    (1000000, '00000000000f4240', '', True),

    # Invalid test list
    (0, '', '', False),
    (1000000, '', '', False),
])
def test_read_eth_supply(block_number: int, result_key: str, result_value: str, should_pass: bool):
    """ Unit test for read_eth_supply. """
    result_key_bytes = bytes.fromhex(result_key) if result_key is not None else None
    result_value_bytes = bytes.fromhex(result_value) if result_value is not None else None
    mock_view = pytest_mock.mock.Mock()
    mock_view.get.return_value = result_key_bytes, result_value_bytes
    if should_pass:
        assert supply.read_eth_supply(mock_view, block_number) == int.from_bytes(result_value_bytes, 'big')
    else:
        assert supply.read_eth_supply(mock_view, block_number) == supply.ETH_SUPPLY_NOT_AVAILABLE
