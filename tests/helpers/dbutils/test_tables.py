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
    assert ETH_SUPPLY_LABEL
    assert PLAIN_STATE_LABEL
    assert PLAIN_ACCOUNTS_CHANGE_SET_LABEL
    assert PLAIN_CONTRACT_CODE_LABEL
    assert PLAIN_STORAGE_CHANGE_SET_LABEL
    assert STORAGE_HISTORY_LABEL
    assert TRANSACTION_LOOKUP_LABEL
    assert TRANSACTION_SENDERS_LABEL
    assert bucketLabels

def test_table_names():
    """ The unit test for table names. """
    assert ACCOUNTS_HISTORY_NAME
    assert BLOCK_BODIES_NAME
    assert BLOCK_HEADERS_NAME
    assert BLOCK_HEADER_NUMBERS_NAME
    assert BLOCK_RECEIPTS_NAME
    assert ETH_SUPPLY_NAME
    assert PLAIN_STATE_NAME
    assert PLAIN_ACCOUNTS_CHANGE_SET_NAME
    assert PLAIN_CONTRACT_CODE_NAME
    assert PLAIN_STORAGE_CHANGE_SET_NAME
    assert STORAGE_HISTORY_NAME
    assert TRANSACTION_LOOKUP_NAME
    assert TRANSACTION_SENDERS_NAME
    assert bucketDescriptors
