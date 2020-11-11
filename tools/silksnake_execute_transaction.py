#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The silksnake_execute_transaction command allows to replay a transaction."""

import argparse
import logging
import signal
import sys

# pylint: disable=unused-argument,invalid-name,line-too-long

import context # pylint: disable=unused-import
import silksnake
import silkworm

def terminate_process(signal_number: int, frame):
    """ terminate_process """
    print()
    logging.info('%s: signal %d, terminating...', __file__, signal_number)
    sys.exit()

def execute_transaction(transaction_hash: str):
    """ execute_transaction """
    logging.info('%s: START - transaction hash: %s', __file__, transaction_hash)

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
    chain_config = silkworm.ChainConfig(5) # read Goerli chain id from config
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
    parser.add_argument('transaction_hash', help='the transaction hash w or w/o leading 0x')
    parser.add_argument('-t', '--target', default=silksnake.DEFAULT_TARGET, help='the server location as string <address>:<port>')
    args = parser.parse_args()

    if args.transaction_hash != '0x':
        execute_transaction(args.transaction_hash)
    else:
        transaction_hash_list = [
            '0x2bc0dd89423d726a02f1f5cf18a3eea9db68c1abd7239ef5ca62477818c85675',
            '0x5a2724495ddddd755f41bf88b23d13e942bd7e00953e507348ddd0f6f3d85f21',
            '0x32ac38d399e06e2dbe19b93e11c2ae58616e27473806b16149be42ad0a393362',
            '0xb77244b337a9bf57e74690d8678aad2999c2b70cfcefa525446b593e7a19afeb',
            '0x39d4db2e4e42351131c8bcc2f9c3c0867ca96359ffd7a5c66e74ee19dce0a8c5',
            '0xa17fefad767e352ce9fd45e77c59608fbd8d5c9ac1ed3d870dd8ead115afc552',
            '0x203256a92ce53f6b11bc6cfa630e230a6097b245e182817cc53296f93be4e17d',
            '0x252f12c04194b096edf5ae2c88ffe7adb3fac85ae4a4c49220741652e5a9d4c4',
            '0xb4a948438d0297e361855b7834951147b8be625c1fbccbed33f41e1be3125762',
            '0x76e0942d3f10147839e3665daad72e8e185fa36bf60c8c6f5fbb638df4d42987',
            '0x9138df213f7dfbba3459f07590329d5672b9526d4cf1ffbffda7e4896b267830',
        ]
        for txn_hash in transaction_hash_list:
            execute_transaction(txn_hash)
