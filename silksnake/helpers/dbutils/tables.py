# -*- coding: utf-8 -*-
"""The Turbo-Geth/Silkworm database metadata."""

ACCOUNTS_HISTORY_LABEL: str = 'hAT'                              # 'History Of Accounts'
BLOCK_BODIES_LABEL: str = 'b'                                    # 'Block Bodies'
BLOCK_HEADERS_LABEL: str = 'h'                                   # 'Headers'
BLOCK_HEADER_NUMBERS_LABEL: str = 'H'                            # 'Header Numbers'
BLOCK_RECEIPTS_LABEL: str = 'r'                                  # 'Receipts'
ETH_SUPPLY_LABEL: str = 'org.ffconsulting.tg.db.ETH_SUPPLY.v2'   # 'History of ETH Supply'
PLAIN_STATE_LABEL: str = 'PLAIN-CST2'                            # 'Plain State'
PLAIN_ACCOUNTS_CHANGE_SET_LABEL: str = 'PLAIN-ACS'               # 'Account Changes'
PLAIN_CONTRACT_CODE_LABEL: str = 'PLAIN-contractCode'            # 'Plain Code Hash'
PLAIN_STORAGE_CHANGE_SET_LABEL: str = 'PLAIN-SCS'                # 'Storage Changes'
STORAGE_HISTORY_LABEL: str = 'hST'                               # 'History Of Storage'
SYNC_STAGE_PROGRESS_LABEL: str = 'SSP2'                          # 'Sync Stage Progress'
TRANSACTION_LOOKUP_LABEL: str = 'l'                              # 'Transaction Index'
TRANSACTION_SENDERS_LABEL: str = 'txSenders'                     # 'Senders'

bucketLabels: [str] = [
    ACCOUNTS_HISTORY_LABEL,
    BLOCK_BODIES_LABEL,
    BLOCK_HEADERS_LABEL,
    BLOCK_HEADER_NUMBERS_LABEL,
    BLOCK_RECEIPTS_LABEL,
    ETH_SUPPLY_LABEL,
    PLAIN_STATE_LABEL,
    PLAIN_ACCOUNTS_CHANGE_SET_LABEL,
    PLAIN_CONTRACT_CODE_LABEL,
    PLAIN_STORAGE_CHANGE_SET_LABEL,
    STORAGE_HISTORY_LABEL,
    TRANSACTION_LOOKUP_LABEL,
    TRANSACTION_SENDERS_LABEL,
]
