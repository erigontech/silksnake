# -*- coding: utf-8 -*-
"""The unit test for turbo module."""

import pytest
import pytest_mock

from silksnake.api import turbo
from silksnake.core import reader
from silksnake.remote import kv_remote
from silksnake.state import supply

# pylint: disable=line-too-long,no-self-use,unused-argument

@pytest.fixture
def mock_get_supply(mocker: pytest_mock.MockerFixture, block_number_or_hash: str, value: int) -> None:
    """ mock_get_supply """
    mock_read_eth_supply = mocker.patch.object(reader.StateReader, 'read_eth_supply')
    mock_read_eth_supply.return_value = value

class TestTurboAPI:
    """ Unit test case for TurboAPI.
    """
    def test_default_init(self):
        """ Unit test for __init__. """
        api = turbo.TurboAPI()
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
            api = turbo.TurboAPI(target)
            assert isinstance(api.remote_kv, kv_remote.RemoteKV)
        else:
            with pytest.raises((AttributeError, ValueError)):
                turbo.TurboAPI(target)

    @pytest.mark.parametrize("target,should_pass", [
        # Valid test list
        ('localhost:9090', True),
        ('unknown:9090', True),

        # Invalid test list
    ])
    def test_close(self, target: str, should_pass: bool):
        """ Unit test for close. """
        if should_pass:
            api = turbo.TurboAPI(target)
            api.close()

    @pytest.mark.usefixtures('mock_get_supply')
    @pytest.mark.parametrize("block_number_or_hash,value", [
        # Valid test list
        ('0', 0),
        ('2000001', 1780454672837),

        # Invalid test list
        ('-1', supply.ETH_SUPPLY_NOT_AVAILABLE),
    ])
    def test_get_eth_supply(self, block_number_or_hash: str, value: int):
        """ Unit test for get_eth_supply. """
        supply_value = turbo.TurboAPI().get_eth_supply(block_number_or_hash)
        assert supply_value == value
