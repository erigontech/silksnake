# -*- coding: utf-8 -*-
"""The unit test for stages module."""

import pytest
import pytest_mock

from silksnake.core import kvstore

# pylint: disable=wildcard-import

from silksnake.stagedsync import stages

def test_stage_labels():
    """ The unit test for stage labels. """
    assert stages.SyncStage.HEADERS
    assert stages.SyncStage.BLOCK_HASHES
    assert stages.SyncStage.BODIES
    assert stages.SyncStage.SENDERS
    assert stages.SyncStage.EXECUTION
    assert stages.SyncStage.INTERMEDIATE_HASHES
    assert stages.SyncStage.HASH_STATE
    assert stages.SyncStage.ACCOUNT_HISTORY_INDEX
    assert stages.SyncStage.STORAGE_HISTORY_INDEX
    assert stages.SyncStage.LOG_INDEX
    assert stages.SyncStage.TX_LOOKUP
    assert stages.SyncStage.TX_POOL
    assert stages.SyncStage.FINISH

@pytest.fixture
def mock_sync_stage_progress(mocker: pytest_mock.MockerFixture, value: str) -> None:
    """ mock_state_reader """
    mock_get = mocker.patch.object(kvstore.View, 'get')
    if value is None:
        mock_get.side_effect = ValueError
    mock_get.return_value = bytes.fromhex(value)

@pytest.mark.usefixtures('mock_sync_stage_progress')
@pytest.mark.parametrize("stage,value,expected_value,should_pass", [
    # Valid test list
    (stages.SyncStage.EXECUTION, '0000000000000000', 0, True),

    # Invalid test list
    (None, '0000000000000000', 0, False),
])
def test_get_stage_progress(stage: stages.SyncStage, value: str, expected_value: int, should_pass: bool) -> None:
    """Unit test for test_get_stage_progress"""
    stage_key = stage.value if stage is not None else None
    mock_view = pytest_mock.mock.Mock()
    #mock_view.get.return_value = stage_key, bytes.fromhex(value)
    mock_database = pytest_mock.mock.Mock()
    mock_database.view.return_value = mock_view
    if should_pass:
        mock_view.get.return_value = stage_key, bytes.fromhex(value)
        assert stages.get_stage_progress(mock_database, stage) == (expected_value, bytes(0))
    else:
        mock_view.get.return_value = b'', bytes.fromhex(value)
        with pytest.raises((ValueError)):
            stages.get_stage_progress(mock_database, stage if stage else stages.SyncStage.EXECUTION)

@pytest.mark.parametrize("data_hex,block_number,rest,should_pass", [
    # Valid test list
    ('', 0, b'', True),

    # Invalid test list
    (None, 0, b'', False),
    ('0102', 0, b'', False),
])
def test_unmarshal_data(data_hex: str, block_number: int, rest: bytes, should_pass: bool) -> None:
    """Unit test for unmarshal_data"""
    data = bytes.fromhex(data_hex) if data_hex is not None else None
    if should_pass:
        assert stages.unmarshal_data(data) == (block_number, rest)
    else:
        with pytest.raises((TypeError, ValueError)):
            stages.unmarshal_data(data)
