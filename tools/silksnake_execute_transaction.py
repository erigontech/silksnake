#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The silksnake_execute_transaction command allows to replay a transaction."""

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

def execute_transaction(network: str, transaction_hash: str):
    """ execute_transaction will run the transaction with given hash on target network.
        WARNING: if multiple transactions from the same sender were included in the block which this transaction
        belongs to, then this transaction *MUST* be the first one or will fail with 'invalid nonce'
    """
    logging.info('%s: START - network: %s transaction hash: %s', __file__, network, transaction_hash)

    eth_api = silksnake.EthereumAPI()
    transaction, block_number, _, _ = eth_api.get_transaction_info_by_hash(transaction_hash)
    logging.info('block number: %d', block_number)

    block = eth_api.get_block_by_number(block_number)
    gas_limit = block.header.gas_limit
    logging.info('block gas limit: %d', gas_limit)

    block = silkworm.Block(block_number, gas_limit)
    txn = silkworm.Transaction(
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
    logging.info('transaction: %s', txn)
    state_reader = silksnake.StateReader(eth_api.remote_kv, block_number)
    buffer = silkworm.RemoteBuffer(state_reader)
    intra_block_state = silkworm.IntraBlockState(buffer)
    blockchain = silksnake.Blockchain(eth_api.remote_kv)
    blockchain_config = blockchain.read_config(network)
    chain_config = silkworm.ChainConfig(blockchain_config['chainId'])
    logging.info('chain_config: %s', chain_config)
    processor = silkworm.ExecutionProcessor(block, intra_block_state, chain_config)
    logging.info('processor: %s', processor)
    receipt = processor.execute_transaction(txn)
    logging.info('receipt: %s', receipt)

    logging.info('%s: END', __file__)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)

    signal.signal(signal.SIGINT, terminate_process)
    signal.signal(signal.SIGQUIT, terminate_process)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('network', help='the network name')
    parser.add_argument('transaction_hash', help='the transaction hash w or w/o leading 0x')
    parser.add_argument('-t', '--target', default=silksnake.DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    execute_transaction(args.network, args.transaction_hash)
