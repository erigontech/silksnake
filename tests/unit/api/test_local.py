# -*- coding: utf-8 -*-
"""The unit test for local module."""

from typing import Any

import pytest
import pytest_mock

from silksnake.api import local
from silksnake.core import account
from silksnake.core import reader
from silksnake.stagedsync import stages

# pylint: disable=line-too-long,no-self-use,unused-argument,invalid-name

@pytest.fixture
def mock_get_stage_progress(mocker: pytest_mock.MockerFixture, block_number: int) -> None:
    """ mock_get_stage_progress """
    mock_stage_progress = mocker.patch.object(stages, 'get_stage_progress')
    if block_number < 0:
        mock_stage_progress.side_effect = ValueError()
    mock_stage_progress.return_value = block_number, bytes(0)

@pytest.fixture
def mock_staged_sync(mocker: pytest_mock.MockerFixture, highest_block: int, current_block: int) -> None:
    """ mock_staged_sync """
    mock_stage_progress = mocker.patch.object(stages, 'get_stage_progress')
    mock_stage_progress.return_value = highest_block, bytes(0)
    mock_stage_progress.side_effect = ValueError if highest_block is None else [(highest_block, bytes(0)), (current_block, bytes(0))]

@pytest.fixture
def mock_state_reader(mocker: pytest_mock.MockerFixture, incarnation: int, value: bytes, should_pass: bool) -> None:
    """ mock_state_reader """
    mock_read_account_data = mocker.patch.object(reader.StateReader, 'read_account_data')
    mock_read_account_storage = mocker.patch.object(reader.StateReader, 'read_account_storage')
    if should_pass:
        mock_read_account_data.return_value = account.Account(0, 0, incarnation, '', '')
        mock_read_account_storage.return_value = value
    else:
        mock_read_account_data.side_effect = ValueError

@pytest.fixture
def mock_get_supply(mocker: pytest_mock.MockerFixture, block_number_or_hash: str, value: int, should_pass: bool) -> None:
    """ mock_get_supply """
    mock_read_eth_supply = mocker.patch.object(reader.StateReader, 'read_eth_supply')
    if should_pass:
        mock_read_eth_supply.return_value = value
    else:
        mock_read_eth_supply.side_effect = ValueError

@pytest.mark.usefixtures('mock_get_stage_progress')
@pytest.mark.parametrize("block_number,should_pass", [
    # Valid test list
    (0, True),
    (100000000, True),

    # Invalid test list
    (-1, False),
])
def test_eth_blockNumber(block_number: int, should_pass: bool):
    """ Unit test for eth_blockNumber. """
    latest_block_number = local.eth_blockNumber()
    if should_pass:
        assert latest_block_number == block_number
    else:
        assert latest_block_number == 0

@pytest.mark.usefixtures('mock_state_reader')
@pytest.mark.parametrize("address,index,block_number_or_hash,expected_value,incarnation,value,should_pass", [
    # Valid test list
    ('0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', '0x00', '2000001', '0x00000000000000000000000000000000000000000000003635c9adc5dea00000', 1, b'65\xc9\xad\xc5\xde\xa0\x00\x00', True),

    # Invalid test list
    ('0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d64', '0x00', '2000001', '0x', 1, b'', False),
])
def test_eth_getStorageAt(address: str, index: str, block_number_or_hash: str, expected_value: str, incarnation: int, value: bytes, should_pass: bool):
    """ Unit test for eth_getStorageAt. """
    storage_location = local.eth_getStorageAt(address, index, block_number_or_hash)
    assert storage_location == expected_value

@pytest.mark.usefixtures('mock_staged_sync')
@pytest.mark.parametrize("highest_block,current_block,result,should_pass", [
    # Valid test list
    (0, 0, False, True),
    (1000, 100, (1000, 100), True),
    #(1000, 1000, False, True),

    # Invalid test list
    (None, 100, False, False),
])
def test_eth_syncing(highest_block: int, current_block: int, result: Any, should_pass: bool):
    """ Unit test for eth_syncing. """
    syncing = local.eth_syncing()
    if should_pass:
        assert syncing == bool(result) or syncing == result
    else:
        assert syncing == 0

@pytest.mark.usefixtures('mock_get_supply')
@pytest.mark.parametrize("block_number_or_hash,value,should_pass", [
    # Valid test list
    ('0', 0, True),
    ('2000001', 1780454672837, True),

    # Invalid test list
    ('-1', 0, False),
])
def test_turbo_getSupply(block_number_or_hash: str, value: int, should_pass: bool):
    """ Unit test for turbo_getSupply. """
    supply_value = local.turbo_getSupply(block_number_or_hash)
    assert supply_value == value
