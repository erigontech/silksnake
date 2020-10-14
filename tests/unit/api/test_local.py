# -*- coding: utf-8 -*-
"""The unit test for local module."""

from typing import Any

import pytest
import pytest_mock

from silksnake.api import local
from silksnake.core import account
from silksnake.core import reader
from silksnake.stagedsync import stages
from silksnake.state import supply

from .test_eth import mock_read_block_by_number, mock_read_block_by_hash, mock_transaction_count_by_number, mock_transaction_count_by_hash

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
def mock_get_supply(mocker: pytest_mock.MockerFixture, block_number_or_hash: str, value: int) -> None:
    """ mock_get_supply """
    mock_read_eth_supply = mocker.patch.object(reader.StateReader, 'read_eth_supply')
    mock_read_eth_supply.return_value = value

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

@pytest.mark.usefixtures(mock_read_block_by_number.__name__)
@pytest.mark.parametrize("block_number,expected_number", [
    # Valid test list
    (0, 0),
    (100000000, 100000000),

    # Invalid test list
    (-1, None),
])
def test_eth_getBlockByNumber(block_number: int, expected_number: int):
    """ Unit test for eth_getBlockByNumber. """
    if block_number < 0:
        assert local.eth_getBlockByNumber(block_number) == expected_number
    else:
        assert local.eth_getBlockByNumber(block_number).header.block_number == block_number

@pytest.mark.usefixtures(mock_read_block_by_hash.__name__)
@pytest.mark.parametrize("block_hash,expected_hash", [
    # Valid test list
    ('ec5f83325a31120741a5bb6ee5e238cc3984ccfad4465a098a555bc61526899a', 'ec5f83325a31120741a5bb6ee5e238cc3984ccfad4465a098a555bc61526899a'),

    # Invalid test list
    ('', None),
    (None, None),
])
def test_eth_getBlockByHash(block_hash: str, expected_hash: str):
    """ Unit test for eth_getBlockByHash. """
    if expected_hash is None:
        assert local.eth_getBlockByHash(block_hash) == expected_hash
    else:
        assert local.eth_getBlockByHash(block_hash).header.hash.hex() == expected_hash

@pytest.mark.usefixtures(mock_transaction_count_by_number.__name__)
@pytest.mark.parametrize("block_number,transaction_count", [
    # Valid test list
    (0, 0),
    (100000000, 18),

    # Invalid test list
    (None, -1),
])
def test_eth_getBlockTransactionCountByNumber(block_number: int, transaction_count: int):
    """ Unit test for eth_getBlockTransactionCountByNumber. """
    assert local.eth_getBlockTransactionCountByNumber(block_number) == transaction_count

@pytest.mark.usefixtures(mock_transaction_count_by_hash.__name__)
@pytest.mark.parametrize("block_hash,transaction_count", [
    # Valid test list
    ('', 0),
    ('ec5f83325a31120741a5bb6ee5e238cc3984ccfad4465a098a555bc61526899a', 18),

    # Invalid test list
    (None, -1),
])
def test_eth_getBlockTransactionCountByHash(block_hash: str, transaction_count: int):
    """ Unit test for eth_getBlockTransactionCountByHash. """
    block_hash_bytes = bytes.fromhex(block_hash) if block_hash else None
    assert local.eth_getBlockTransactionCountByHash(block_hash_bytes) == transaction_count

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
@pytest.mark.parametrize("block_number_or_hash,value", [
    # Valid test list
    ('0', 0),
    ('2000001', 1780454672837),

    # Invalid test list
    ('-1', supply.ETH_SUPPLY_NOT_AVAILABLE),
])
def test_turbo_getSupply(block_number_or_hash: str, value: int):
    """ Unit test for turbo_getSupply. """
    supply_value = local.turbo_getSupply(block_number_or_hash)
    assert supply_value == value
