# -*- coding: utf-8 -*-
"""The unit test for eth module."""

import pytest
import pytest_mock

from silksnake.api import eth
from silksnake.core import account
from silksnake.core import reader
from silksnake.remote import kv_remote

# pylint: disable=line-too-long,no-self-use,unused-argument

@pytest.fixture
def mock_state_reader(mocker: pytest_mock.MockerFixture, incarnation: int, value: bytes, should_pass: bool) -> None:
    """ mock_state_reader """
    mock_read_account_data = mocker.patch.object(reader.StateReader, 'read_account_data')
    mock_read_account_storage = mocker.patch.object(reader.StateReader, 'read_account_storage')
    if should_pass:
        mock_read_account_data.return_value = account.Account(0, 0, incarnation, '', '')
        mock_read_account_storage.return_value = value

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

    @pytest.mark.usefixtures('mock_state_reader')
    @pytest.mark.parametrize("address,index,block_number_or_hash,expected_value,incarnation,value,should_pass", [
        # Valid test list
        ('0x33ee33fc3e1aacdb75a1ad362489ac54f02d6d63', '0x00', '2000001', '0x00000000000000000000000000000000000000000000003635c9adc5dea00000', 1, b'65\xc9\xad\xc5\xde\xa0\x00\x00', True),

        # Invalid test list
        #('', None, '2000000', '', '', '', False),
        #('', '0x00', '2000000', '', '', '', False),
    ])
    def test_get_storage_at(self, address: str, index: str, block_number_or_hash: str, expected_value: str, incarnation: int, value: bytes, should_pass: bool):
        """ Unit test for get_storage_at. """
        api = eth.EthereumAPI()
        if should_pass:
            storage_value = api.get_storage_at(address, index, block_number_or_hash)
            assert storage_value == expected_value
        else:
            with pytest.raises((ValueError)):
                api.get_storage_at(address, index, block_number_or_hash)
