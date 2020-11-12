#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The silksnake_execute_block command allows to replay a historical block."""

import argparse
import logging
import signal
import sys

# pylint: disable=unused-argument,invalid-name,line-too-long,too-many-locals

import context # pylint: disable=unused-import
import silksnake
import silkworm

def terminate_process(signal_number: int, frame):
    """ terminate_process """
    print()
    logging.info('%s: signal %d, terminating...', __file__, signal_number)
    sys.exit()

def execute_block(network: str, block_number: str):
    """ execute_block """
    logging.info('%s: START - network: %s block number: %d', __file__, network, block_number)

    eth_api = silksnake.EthereumAPI()
    block = eth_api.get_block_by_number(block_number)
    if not block:
        raise ValueError(f'unknown block {block_number}')
    logging.info('block number: %d', block_number)
    gas_limit = block.header.gas_limit
    logging.info('block gas limit: %d', gas_limit)

    sw_transaction_list = []
    for transaction in block.body.transactions:
        sw_transaction = silkworm.Transaction(
            transaction.nonce,
            transaction.gas_price,
            transaction.gas_limit,
            silkworm.EvmAddress(transaction.to),
            transaction.value,
            transaction.data,
            transaction.v,
            transaction.r,
            transaction.s,
            silkworm.EvmAddress(transaction.sender)
        )
        sw_transaction_list.append(sw_transaction)

    sw_block = silkworm.Block(block_number, gas_limit)
    sw_block.transactions = sw_transaction_list
    state_reader = silksnake.StateReader(eth_api.remote_kv, block_number)
    buffer = silkworm.RemoteBuffer(state_reader)
    intra_block_state = silkworm.IntraBlockState(buffer)
    blockchain = silksnake.Blockchain(eth_api.remote_kv)
    blockchain_config = blockchain.read_config(network)
    chain_config = silkworm.ChainConfig(blockchain_config['chainId'])
    logging.info('chain_config: %s', chain_config)
    processor = silkworm.ExecutionProcessor(sw_block, intra_block_state, chain_config)
    logging.info('processor: %s', processor)
    receipt_list = processor.execute_block()
    logging.info('receipt list: %s', receipt_list)

    logging.info('%s: END', __file__)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGQUIT, terminate_process)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('network', help='the network name')
    parser.add_argument('block_number', help='the block number')
    parser.add_argument('-t', '--target', default=silksnake.DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    args.block_number = int(args.block_number)

    if args.block_number >= 0:
        execute_block(args.network, args.block_number)
    else:
        block_heigth_list = [
            '',
        ]
        for block_heigth in block_heigth_list:
            execute_block(args.network, block_heigth)
