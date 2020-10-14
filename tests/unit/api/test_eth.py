# -*- coding: utf-8 -*-
"""The unit test for eth module."""

from typing import Any

import pytest
import pytest_mock

from silksnake.api import eth
from silksnake.core import account
from silksnake.core import chain
from silksnake.core import reader
from silksnake.remote import kv_remote
from silksnake.stagedsync import stages

# pylint: disable=line-too-long,no-self-use,unused-argument

@pytest.fixture
def mock_get_stage_progress(mocker: pytest_mock.MockerFixture, block_number: int) -> None:
    """ mock_state_reader """
    mock_stage_progress = mocker.patch.object(stages, 'get_stage_progress')
    if block_number < 0:
        mock_stage_progress.side_effect = ValueError()
    mock_stage_progress.return_value = block_number, bytes(0)

@pytest.fixture
def mock_staged_sync(mocker: pytest_mock.MockerFixture, highest_block: int, current_block: int) -> None:
    """ mock_state_reader """
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
def mock_read_block_by_number(mocker: pytest_mock.MockerFixture, expected_number: int) -> None:
    """ mock_read_block_by_number """
    header_mock = mocker.Mock()
    header_mock.block_number = expected_number
    block_mock = mocker.Mock()
    block_mock.header = header_mock
    mock_block_by_number = mocker.patch.object(chain.Blockchain, 'read_block_by_number')
    mock_block_by_number.return_value = block_mock if expected_number is not None else None

@pytest.fixture
def mock_read_block_by_hash(mocker: pytest_mock.MockerFixture, expected_hash: str) -> None:
    """ mock_read_block_by_hash """
    header_mock = mocker.Mock()
    header_mock.hash = bytes.fromhex(expected_hash) if expected_hash else None
    block_mock = mocker.Mock()
    block_mock.header = header_mock
    mock_block_by_number = mocker.patch.object(chain.Blockchain, 'read_block_by_hash')
    mock_block_by_number.return_value = block_mock if expected_hash is not None else None

@pytest.fixture
def mock_transaction_count_by_number(mocker: pytest_mock.MockerFixture, block_number: int, transaction_count: int) -> None:
    """ mock_read_block_by_number """
    body_mock = mocker.Mock()
    body_mock.transactions = [None]*transaction_count
    block_mock = mocker.Mock()
    block_mock.body = body_mock
    mock_block_by_number = mocker.patch.object(chain.Blockchain, 'read_block_by_number')
    mock_block_by_number.return_value = block_mock if block_number is not None else None

@pytest.fixture
def mock_transaction_count_by_hash(mocker: pytest_mock.MockerFixture, block_hash: str, transaction_count: int) -> None:
    """ mock_read_block_by_hash """
    body_mock = mocker.Mock()
    body_mock.transactions = [None]*transaction_count
    block_mock = mocker.Mock()
    block_mock.body = body_mock
    mock_block_by_number = mocker.patch.object(chain.Blockchain, 'read_block_by_hash')
    mock_block_by_number.return_value = block_mock if block_hash is not None else None

class TestEthereumAPI:
    """ Unit test case for EthereumAPI.
    """
    def test_default_init(self):
        """ Unit test for __init__. """
        api = eth.EthereumAPI()
        assert isinstance(api.remote_kv, kv_remote.RemoteKV)

    @pytest.mark.parametrize("target,should_pass", [
        # Valid test list
        ('localhost:9090', True),

        # Invalid test list
        (None, False),
        ('', False),
    ])
    def test_init(self, target: str, should_pass: bool):
        """ Unit test for __init__. """
        if should_pass:
            api = eth.EthereumAPI(target)
            assert isinstance(api.remote_kv, kv_remote.RemoteKV)
        else:
            with pytest.raises((AttributeError, ValueError)):
                eth.EthereumAPI(target)

    @pytest.mark.parametrize("target,should_pass", [
        # Valid test list
        ('localhost:9090', True),
        ('unknown:9090', True),

        # Invalid test list
    ])
    def test_close(self, target: str, should_pass: bool):
        """ Unit test for close. """
        if should_pass:
            api = eth.EthereumAPI(target)
            api.close()

    @pytest.mark.usefixtures('mock_get_stage_progress')
    @pytest.mark.parametrize("block_number,should_pass", [
        # Valid test list
        (0, True),
        (100000000, True),

        # Invalid test list
        (-1, False),
    ])
    def test_block_number(self, block_number: int, should_pass: bool):
        """ Unit test for block_number. """
        api = eth.EthereumAPI()
        if should_pass:
            assert api.block_number() == block_number
        else:
            assert api.block_number() == 0

    @pytest.mark.usefixtures('mock_read_block_by_number')
    @pytest.mark.parametrize("block_number,expected_number", [
        # Valid test list
        (0, 0),
        (100000000, 100000000),

        # Invalid test list
        (-1, None),
    ])
    def test_get_block_by_number(self, block_number: int, expected_number: int):
        """ Unit test for get_block_by_number. """
        api = eth.EthereumAPI()
        if block_number < 0:
            assert api.get_block_by_number(block_number) == expected_number
        else:
            assert api.get_block_by_number(block_number).header.block_number == expected_number

    @pytest.mark.usefixtures('mock_read_block_by_hash')
    @pytest.mark.parametrize("block_hash,expected_hash", [
        # Valid test list
        ('ec5f83325a31120741a5bb6ee5e238cc3984ccfad4465a098a555bc61526899a', 'ec5f83325a31120741a5bb6ee5e238cc3984ccfad4465a098a555bc61526899a'),

        # Invalid test list
        ('', None),
        (None, None),
    ])
    def test_get_block_by_hash(self, block_hash: str, expected_hash: str):
        """ Unit test for get_block_by_hash. """
        block_hash_bytes = bytes.fromhex(block_hash) if block_hash is not None else None
        expected_hash_bytes = bytes.fromhex(expected_hash) if expected_hash is not None else None
        api = eth.EthereumAPI()
        if expected_hash is None:
            assert api.get_block_by_hash(block_hash_bytes) == expected_hash
        else:
            assert api.get_block_by_hash(block_hash_bytes).header.hash == expected_hash_bytes

    @pytest.mark.usefixtures('mock_transaction_count_by_number')
    @pytest.mark.parametrize("block_number,transaction_count", [
        # Valid test list
        (0, 0),
        (100000000, 18),

        # Invalid test list
        (None, -1),
    ])
    def test_get_block_transaction_count_by_number(self, block_number: int, transaction_count: int):
        """ Unit test for get_block_transaction_count_by_number. """
        api = eth.EthereumAPI()
        assert api.get_block_transaction_count_by_number(block_number) == transaction_count

    @pytest.mark.usefixtures('mock_transaction_count_by_hash')
    @pytest.mark.parametrize("block_hash,transaction_count", [
        # Valid test list
        ('', 0),
        ('ec5f83325a31120741a5bb6ee5e238cc3984ccfad4465a098a555bc61526899a', 18),

        # Invalid test list
        (None, -1),
    ])
    def test_get_block_transaction_count_by_hash(self, block_hash: str, transaction_count: int):
        """ Unit test for get_block_transaction_count_by_hash. """
        block_hash_bytes = bytes.fromhex(block_hash) if block_hash else None
        api = eth.EthereumAPI()
        assert api.get_block_transaction_count_by_hash(block_hash_bytes) == transaction_count

    @pytest.mark.usefixtures('mock_state_reader')
    @pytest.mark.parametrize("address,index,block_number_or_hash,expected_value,incarnation,value,should_pass", [
        # Valid test list
        ('0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', '0x00', '2000001', '0x00000000000000000000000000000000000000000000003635c9adc5dea00000', 1, b'65\xc9\xad\xc5\xde\xa0\x00\x00', True),

        # Invalid test list
        ('0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d64', '0x00', '2000001', '0x', 1, b'', False),
    ])
    def test_get_storage_at(self, address: str, index: str, block_number_or_hash: str, expected_value: str, incarnation: int, value: bytes, should_pass: bool):
        """ Unit test for get_storage_at. """
        api = eth.EthereumAPI()
        assert api.get_storage_at(address, index, block_number_or_hash) == expected_value

    @pytest.mark.usefixtures('mock_staged_sync')
    @pytest.mark.parametrize("highest_block,current_block,result,should_pass", [
        # Valid test list
        (0, 0, False, True),
        (1000, 100, (1000, 100), True),
        #(1000, 1000, False, True),

        # Invalid test list
        (None, 100, False, False),
    ])
    def test_syncing(self, highest_block: int, current_block: int, result: Any, should_pass: bool):
        """ Unit test for syncing. """
        api = eth.EthereumAPI()
        syncing = api.syncing()
        if should_pass:
            assert syncing == bool(result) or syncing == result
        else:
            assert syncing == 0
