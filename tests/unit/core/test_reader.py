# -*- coding: utf-8 -*-
"""The unit test for reader module."""

import pytest
import pytest_mock

from silksnake.core import history, reader

# pylint: disable=no-self-use,redefined-outer-name,unused-argument

@pytest.fixture
def get_as_of(mocker: pytest_mock.MockerFixture, account_hex: str):
    """ get_as_of """
    get_as_of_mock = mocker.patch.object(history, 'get_as_of')
    get_as_of_mock.return_value = bytes.fromhex(account_hex) if account_hex is not None else None

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

    @pytest.mark.parametrize("address,account_hex,should_pass", [
        # Valid test list
        ('de06e68660429b198612e4b73919395799f9ad87bcaa80dc873e37b281060517', '07010104017f4abe0101', True),

        # Invalid test list
        (None, '07010104017f4abe0101', False),
    ])
    def test_read_account_data(self, get_as_of, address: str, account_hex:str, should_pass: bool):
        """Unit test for read_account_data."""
        state_reader = reader.StateReader(pytest_mock.mock.Mock(), 1234567)
        if should_pass:
            account = state_reader.read_account_data(address)
            data = bytearray(account.length_for_storage())
            account.to_storage(data)
            assert bytes(data) == bytes.fromhex(account_hex)
        else:
            with pytest.raises(ValueError):
                state_reader.read_account_data(address)
