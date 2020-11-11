# -*- coding: utf-8 -*-
"""The unit test for tables module."""

# pylint: disable=wildcard-import

from silksnake.helpers.dbutils.tables import *

def test_table_labels():
    """ The unit test for table labels. """
    assert ACCOUNTS_HISTORY_LABEL
    assert BLOCK_BODIES_LABEL
    assert BLOCK_HEADERS_LABEL
    assert BLOCK_HEADER_NUMBERS_LABEL
    assert BLOCK_RECEIPTS_LABEL
    assert CODE_LABEL
    assert ETH_SUPPLY_LABEL
    assert PLAIN_STATE_LABEL
    assert PLAIN_ACCOUNTS_CHANGE_SET_LABEL
    assert PLAIN_CONTRACT_CODE_LABEL
    assert PLAIN_STORAGE_CHANGE_SET_LABEL
    assert SYNC_STAGE_PROGRESS_LABEL
    assert STORAGE_HISTORY_LABEL
    assert TRANSACTION_LOOKUP_LABEL
    assert TRANSACTION_SENDERS_LABEL
    assert ACCOUNTS_HISTORY_LABEL in tableLabels
    assert BLOCK_BODIES_LABEL in tableLabels
    assert BLOCK_HEADERS_LABEL in tableLabels
    assert BLOCK_HEADER_NUMBERS_LABEL in tableLabels
    assert BLOCK_RECEIPTS_LABEL in tableLabels
    assert CODE_LABEL in tableLabels
    assert ETH_SUPPLY_LABEL in tableLabels
    assert PLAIN_STATE_LABEL in tableLabels
    assert PLAIN_ACCOUNTS_CHANGE_SET_LABEL in tableLabels
    assert PLAIN_CONTRACT_CODE_LABEL in tableLabels
    assert PLAIN_STORAGE_CHANGE_SET_LABEL in tableLabels
    assert SYNC_STAGE_PROGRESS_LABEL in tableLabels
    assert STORAGE_HISTORY_LABEL in tableLabels
    assert TRANSACTION_LOOKUP_LABEL in tableLabels
    assert TRANSACTION_SENDERS_LABEL in tableLabels
