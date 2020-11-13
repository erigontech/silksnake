# -*- coding: utf-8 -*-
"""The unit test for reader module."""

import pytest
import pytest_mock

from silksnake.core import history, reader
from silksnake.state import supply

# pylint: disable=no-self-use,redefined-outer-name,unused-argument

@pytest.fixture
def get_as_of(mocker: pytest_mock.MockerFixture, value: str):
    """ get_as_of """
    get_as_of_mock = mocker.patch.object(history, 'get_as_of')
    get_as_of_mock.return_value = bytes.fromhex(value) if value is not None else None

@pytest.fixture
def database_view_get(mocker: pytest_mock.MockerFixture, result_key: str, result_value: str):
    """ get_as_of """
    result_key_bytes = bytes.fromhex(result_key) if result_key is not None else None
    result_value_bytes = bytes.fromhex(result_value) if result_value is not None else None
    database_mock = pytest_mock.mock.Mock()
    database_mock.view.return_value.get.return_value = (result_key_bytes, result_value_bytes)
    return database_mock

class TestStateReader:
    """Test case for StateReader."""

    @pytest.mark.parametrize("database_mock,block_number,should_pass", [
        # Valid test list
        (pytest_mock.mock.Mock(), 0, True),
        (pytest_mock.mock.Mock(), 1000000, True),

        # Invalid test list
        (pytest_mock.mock.Mock(), None, False),
        (None, 1000000, False),
    ])
    def test__init__(self, database_mock: object, block_number: int, should_pass: bool):
        """Unit test for __init__."""
        if should_pass:
            state_reader = reader.StateReader(database_mock, block_number)
            assert state_reader.database == database_mock
            assert state_reader.block_number == block_number
        else:
            with pytest.raises(ValueError):
                reader.StateReader(database_mock, block_number)

    @pytest.mark.parametrize("address,value,should_pass", [
        # Valid test list
        ('de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '07010104017f4abe0101', True),

        # Invalid test list
        (None, '07010104017f4abe0101', False),
    ])
    def test_read_account_data(self, get_as_of, address: str, value: str, should_pass: bool):
        """Unit test for read_account_data."""
        state_reader = reader.StateReader(pytest_mock.mock.Mock(), 1234567)
        if should_pass:
            account = state_reader.read_account_data(address)
            data = bytearray(account.length_for_storage())
            account.to_storage(data)
            assert bytes(data) == bytes.fromhex(value)
        else:
            with pytest.raises(ValueError):
                state_reader.read_account_data(address)

    @pytest.mark.parametrize("address,incarnation,location,value,should_pass", [
        # Valid test list
        ('de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', 1, '00', '07010104017f4abe0101', True),

        # Invalid test list
        (None, 1, '00', '07010104017f4abe0101', False),
    ])
    def test_read_account_storage(self, get_as_of, address: str, incarnation: int, location: str, value: str, should_pass: bool):
        """Unit test for read_account_storage."""
        location_hash = bytes.fromhex(location) if location is not None else None
        state_reader = reader.StateReader(pytest_mock.mock.Mock(), 1234567)
        if should_pass:
            location_value = state_reader.read_account_storage(address, incarnation, location_hash)
            assert location_value == bytes.fromhex(value)
        else:
            with pytest.raises(ValueError):
                state_reader.read_account_storage(address, incarnation, location_hash)

    @pytest.mark.parametrize("code_hash_hex,result_key,result_value,should_pass", [
        # Valid test list
        (
            'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517',
            'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517',
            '07010104017f4abe0101',
            True
        ),

        # Invalid test list
        (
            None,
            'de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517',
            '07010104017f4abe0101',
            False
        ),
    ])
    def test_read_code(self, database_view_get, code_hash_hex: str, result_key: str, result_value: str, should_pass: bool):
        """Unit test for read_code."""
        result_value_bytes = bytes.fromhex(result_value) if result_value is not None else None
        state_reader = reader.StateReader(database_view_get, 1234567)
        if should_pass:
            code_bytes = state_reader.read_code(code_hash_hex)
            assert code_bytes == result_value_bytes
        else:
            with pytest.raises(TypeError):
                state_reader.read_code(code_hash_hex)

    @pytest.mark.parametrize("block_number,result_key,result_value,should_pass", [
        # Valid test list
        (0, '0000000000000000', '0000000000000001', True),
        (1000000, '00000000000f4240', '', True),

        # Invalid test list
        (0, '', '', False),
        (1000000, '', '', False),
    ])
    def test_read_eth_supply(self, database_view_get, block_number: int, result_key: str, result_value: str, should_pass: bool):
        """ Unit test for read_eth_supply. """
        result_value_bytes = bytes.fromhex(result_value) if result_value is not None else None
        state_reader = reader.StateReader(database_view_get, block_number)
        if should_pass:
            assert state_reader.read_eth_supply() == int.from_bytes(result_value_bytes, 'big')
        else:
            assert state_reader.read_eth_supply() == supply.ETH_SUPPLY_NOT_AVAILABLE
