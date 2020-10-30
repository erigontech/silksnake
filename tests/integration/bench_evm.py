#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The bench_evm bench."""

import logging
import os
import signal
import sys

# pylint: disable=unused-argument,invalid-name

import context # pylint: disable=unused-import
import silkworm

def terminate_process(signal_number: int, frame):
    """ terminate_process """
    print()
    logging.info('%s: signal %d, terminating...', __file__, signal_number)
    sys.exit()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGQUIT, terminate_process)

    logging.info('%s: START - PID is %d', __file__, os.getpid())

    parent_hash = silkworm.EvmBytes32(bytes.fromhex('27d6b0139674635cf51d82c9bfbc6536954ff8f03650c1ee97b56dbc1fd16807'))
    print(parent_hash)
    ommers_hash = silkworm.EvmBytes32(bytes.fromhex('1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347'))
    print(ommers_hash)
    beneficiary = silkworm.EvmAddress(b'\x00\x01')
    #beneficiary.bytes = b'\x00\x01'
    print(beneficiary)
    state_root = silkworm.EvmBytes32(bytes.fromhex('474b3fb6f3e5675d1a0a9f915d13930bb3943b61cbd5c1b96115a36cf5e0f204'))
    print(state_root)
    transactions_root = silkworm.EvmBytes32(bytes.fromhex('864aa5398f5cdb95b349b004c1a60c22062d11aed4bb4c841bfebd947f184eba'))
    print(transactions_root)
    receipts_root = silkworm.EvmBytes32(bytes.fromhex('8a9a2b3a9ce4ef8523b6318bb7e84d8c348b0ceab391a7e98211c6b191f32443'))
    print(receipts_root)
    logs_bloom = [0 for i in range(256)]
    difficulty = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    difficulty = 340282367920938463463374607431768211456
    number = int(os.getpid())
    gas_limit = 8000000
    gas_used = 2100000
    timestamp = 0
    mix_hash = silkworm.EvmBytes32(bytes.fromhex('0000000000000000000000000000000000000000000771c4fa448f21a1478809'))
    nonce = [0 for i in range(8)]
    header = silkworm.BlockHeader(
        parent_hash,
        ommers_hash,
        beneficiary,
        state_root,
        transactions_root,
        receipts_root,
        logs_bloom,
        difficulty,
        number,
        gas_limit,
        gas_used,
        timestamp,
        mix_hash,
        nonce
    )
    print(header)
    body = silkworm.BlockBody([], [])
    print(body)
    block = silkworm.Block([], [], silkworm.BlockHeader())
    print(block)

    txn = silkworm.Transaction(0, 10000, 21000, None, 0, '', 1, 1, 1, None)
    print(txn)

    logging.info('%s: END', __file__)
